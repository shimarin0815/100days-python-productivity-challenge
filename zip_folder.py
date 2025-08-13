# zip_folder.py
import argparse
import os
import sys
import time
import zipfile
from fnmatch import fnmatch

DEFAULT_EXCLUDES = ["__pycache__", ".DS_Store", ".git", "*.tmp", "*.log"]

def timestamp():
    return time.strftime("%Y%m%d_%H%M%S")

def make_unique(path_without_ext):
    """既存なら (1), (2)... と連番を付けて衝突回避"""
    n = 1
    candidate = path_without_ext
    while os.path.exists(candidate + ".zip"):
        n += 1
        candidate = f"{path_without_ext}({n})"
    return candidate + ".zip"

def should_exclude(name, exclude_patterns):
    """ファイル/フォルダ名が除外パターンに当てはまるか判定"""
    return any(fnmatch(name, pat) for pat in exclude_patterns)

def zip_directory(src_dir, out_name=None, exclude_patterns=None, quiet=False):
    if not os.path.isdir(src_dir):
        raise FileNotFoundError(f"フォルダが見つかりません: {src_dir}")

    exclude_patterns = (exclude_patterns or []) + DEFAULT_EXCLUDES

    # 出力ファイル名（拡張子除く）を決める
    src_dir = os.path.abspath(src_dir)
    base = out_name or (os.path.basename(src_dir) + "_" + timestamp())
    out_path_without_ext = os.path.join(os.getcwd(), base)

    # 同名があれば連番で回避
    zip_path = make_unique(out_path_without_ext)

    files_added = 0
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(src_dir):
            # 除外フォルダをスキップ
            dirs[:] = [d for d in dirs if not should_exclude(d, exclude_patterns)]
            # ファイルを追加
            for f in files:
                if should_exclude(f, exclude_patterns):
                    continue
                abs_path = os.path.join(root, f)
                arcname = os.path.relpath(abs_path, start=src_dir)
                zf.write(abs_path, arcname)
                files_added += 1
                if not quiet and files_added % 25 == 0:
                    print(f"追加中... {files_added} ファイル")

    size_mb = os.path.getsize(zip_path) / (1024 * 1024)
    if not quiet:
        print(f"\n✅ 完了: {zip_path}  ({files_added}ファイル, {size_mb:.2f} MB)")
    return zip_path

def parse_args():
    parser = argparse.ArgumentParser(
        description="指定フォルダをZIPに圧縮します。（余計なゴミを自動除外）"
    )
    parser.add_argument("folder", help="圧縮したいフォルダへのパス")
    parser.add_argument("-o", "--output", help="出力ZIP名（拡張子不要）")
    parser.add_argument(
        "-e", "--exclude", nargs="*", default=[], 
        help=f"除外パターン（スペース区切りで複数OK）。例: --exclude '*.png' 'node_modules'"
    )
    parser.add_argument("-q", "--quiet", action="store_true", help="進行状況を表示しない")
    return parser.parse_args()

def main():
    try:
        args = parse_args()
        zip_directory(args.folder, out_name=args.output, exclude_patterns=args.exclude, quiet=args.quiet)
    except Exception as e:
        print(f"❌ エラー: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
