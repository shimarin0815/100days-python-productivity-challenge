#!/usr/bin/env python3
"""
画像サイズレポーター（複数フォルダまとめ対応版）
- 指定した複数のフォルダから JPEG/PNG を集めて、幅/高さ/面積/サイズを一覧化
- 出力は CSV または Markdown。ソートや再帰検索も可能
- 各画像がどのフォルダ由来か分かるように 'root' と 'rel_path' を付ける

使い方（例）:
  1フォルダ:  python image_size_reporter.py --dir "./images"
  複数:       python image_size_reporter.py --dir "C:/A" "C:/B"
  再帰:       python image_size_reporter.py --dir "./A" "./B" --recursive
  MD出力:     python image_size_reporter.py --dir "./A" "./B" --format md --out report.md
  ソート:     python image_size_reporter.py --dir "./A" "./B" --sort area --reverse
"""
from __future__ import annotations
import argparse
import csv
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Tuple, Optional

from PIL import Image  # pip install pillow

VALID_EXTS = {".jpg", ".jpeg", ".png"}

@dataclass
class ImageInfo:
    root: Path        # スキャン起点のフォルダ
    path: Path        # 画像の絶対/相対パス（ここでは絶対推奨）
    rel_path: str     # root からの相対パス（レポートに使いやすい）
    width: int
    height: int
    size_kb: float
    format: str

    @property
    def area(self) -> int:
        return self.width * self.height


def find_images(root: Path, recursive: bool) -> Iterable[Path]:
    """root直下（または再帰）からJPEG/PNGを列挙"""
    if recursive:
        yield from (p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in VALID_EXTS)
    else:
        yield from (p for p in root.iterdir() if p.is_file() and p.suffix.lower() in VALID_EXTS)


def read_image_info(img_path: Path) -> Optional[Tuple[int, int, float, str]]:
    """画像の幅/高さ/サイズKB/形式を読む。失敗したらNone。"""
    try:
        with Image.open(img_path) as im:
            w, h = im.size
            fmt = im.format or img_path.suffix.upper().lstrip(".")
        size_kb = round(img_path.stat().st_size / 1024, 1)
        return w, h, size_kb, fmt
    except Exception as e:
        print(f"[warn] 読み込み失敗: {img_path} ({e})", file=sys.stderr)
        return None


def sort_key_fn(key: str):
    if key == "name":   return lambda it: (str(it.rel_path).lower(), str(it.path).lower())
    if key == "width":  return lambda it: it.width
    if key == "height": return lambda it: it.height
    if key == "area":   return lambda it: it.area
    if key == "size":   return lambda it: it.size_kb
    return lambda it: (str(it.rel_path).lower(), str(it.path).lower())


def write_csv(items: List[ImageInfo], out_path: Path) -> None:
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["root", "rel_path", "format", "width_px", "height_px", "area_px", "size_kb", "abs_path"])
        for it in items:
            writer.writerow([
                str(it.root),
                it.rel_path,
                it.format,
                it.width,
                it.height,
                it.area,
                it.size_kb,
                str(it.path.resolve())
            ])


def write_markdown(items: List[ImageInfo], out_path: Path) -> None:
    with out_path.open("w", encoding="utf-8") as f:
        f.write("| root | rel_path | format | width(px) | height(px) | area(px) | size(kb) |\n")
        f.write("|---|---|---:|---:|---:|---:|---:|\n")
        for it in items:
            f.write(f"| {it.root} | {it.rel_path} | {it.format} | {it.width} | {it.height} | {it.area} | {it.size_kb} |\n")


def main():
    parser = argparse.ArgumentParser(description="画像サイズレポーター（複数フォルダまとめ対応版）")
    parser.add_argument("--dir", nargs="+", required=True,
                        help="調べたいフォルダを1つ以上（スペース区切りで複数）")
    parser.add_argument("--recursive", action="store_true", help="サブフォルダも調べる")
    parser.add_argument("--format", choices=["csv", "md"], default="csv", help="出力形式")
    parser.add_argument("--out", help="出力ファイル名（例: report.csv / report.md）")
    parser.add_argument("--sort", choices=["name", "width", "height", "area", "size"], default="name",
                        help="並び順のキー")
    parser.add_argument("--reverse", action="store_true", help="降順にする")
    args = parser.parse_args()

    roots: List[Path] = [Path(p).expanduser() for p in args.dir]
    valid_roots: List[Path] = []
    for r in roots:
        if not r.exists() or not r.is_dir():
            print(f"[warn] フォルダが見つかりません: {r}", file=sys.stderr)
        else:
            valid_roots.append(r)

    if not valid_roots:
        print("[error] 有効なフォルダが1つもありません。--dir の指定を確認してください。")
        sys.exit(1)

    infos: List[ImageInfo] = []
    for root in valid_roots:
        for p in find_images(root, recursive=args.recursive):
            meta = read_image_info(p)
            if not meta:
                continue
            w, h, size_kb, fmt = meta
            try:
                rel = str(p.relative_to(root))
            except ValueError:
                # まれに別ドライブなどで relative_to が失敗したら、ファイル名のみを相対扱いに
                rel = p.name
            infos.append(ImageInfo(
                root=root.resolve(),
                path=p.resolve(),
                rel_path=rel,
                width=w,
                height=h,
                size_kb=size_kb,
                format=fmt
            ))

    if not infos:
        print("[info] 画像が見つかりませんでした。拡張子(JPG/JPEG/PNG)やフォルダを確認してください。")
        return

    # 並び替え
    infos.sort(key=sort_key_fn(args.sort), reverse=args.reverse)

    # 出力
    default_name = "image_report.csv" if args.format == "csv" else "image_report.md"
    out_path = Path(args.out) if args.out else Path(default_name)
    if args.format == "csv":
        write_csv(infos, out_path)
    else:
        write_markdown(infos, out_path)

    print(f"[done] {len(infos)} 件の画像を解析しました。出力: {out_path.resolve()}")


if __name__ == "__main__":
    main()
