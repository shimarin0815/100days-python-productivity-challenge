# phone_formatter.py
import argparse

def only_digits(s: str) -> str:
    """数字だけを取り出す（全角は想定外。基本は半角で入力してね）"""
    return "".join(ch for ch in s if ch.isdigit())

def add_hyphen_jp(raw: str) -> str:
    """
    日本の“よくある”型でハイフンを付ける簡易フォーマッタ。
    - 11桁: 3-4-4（090/080/070や050など）
    - 10桁:
        * 0120/0570: 4-3-3
        * 03/06:     2-4-4
        * それ以外:  3-3-4
    それ以外の桁数は、数字のみ返す（無理にハイフンを付けない）。
    """
    d = only_digits(raw)

    # 11桁（携帯・050など）
    if len(d) == 11:
        return f"{d[:3]}-{d[3:7]}-{d[7:]}"

    # 10桁（固定・フリーダイヤル等）
    if len(d) == 10:
        if d.startswith(("0120", "0570")):
            return f"{d[:4]}-{d[4:7]}-{d[7:]}"
        if d.startswith(("03", "06")):
            return f"{d[:2]}-{d[2:6]}-{d[6:]}"
        return f"{d[:3]}-{d[3:6]}-{d[6:]}"

    # それ以外は数字だけ返す（安全側）
    return d

def remove_hyphen(raw: str) -> str:
    """ハイフンをすべて取り除く"""
    return only_digits(raw)

def toggle_format(raw: str) -> str:
    """
    文字にハイフンが入っていれば削除、なければ付与（整形）する。
    すでにハイフンが入っていても、最終的に「付与」側なら整え直してくれる。
    """
    if "-" in raw:
        return remove_hyphen(raw)
    else:
        return add_hyphen_jp(raw)

def main():
    parser = argparse.ArgumentParser(
        description="電話番号フォーマッター（ハイフン入り↔なしを相互変換）"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-a", "--add", action="store_true", help="ハイフンを追加する")
    group.add_argument("-r", "--remove", action="store_true", help="ハイフンを削除する")
    group.add_argument("-t", "--toggle", action="store_true", help="ハイフン有無をトグル変換（既定）")

    parser.add_argument(
        "numbers",
        nargs="*",
        help="変換する電話番号（複数可）。未指定なら対話モードになります。",
    )

    args = parser.parse_args()
    mode = "toggle"
    if args.add:
        mode = "add"
    elif args.remove:
        mode = "remove"

    def convert_one(s: str) -> str:
        if mode == "add":
            return add_hyphen_jp(s)
        if mode == "remove":
            return remove_hyphen(s)
        return toggle_format(s)

    # 引数に番号がある → まとめて処理
    if args.numbers:
        for n in args.numbers:
            print(convert_one(n))
        return

    # 引数なし → 簡単な対話モード
    print("電話番号フォーマッター 対話モード（終了は Ctrl+C）")
    print(f"モード: {mode}（-a追加 / -r削除 / -tトグル）")
    while True:
        try:
            s = input("番号> ").strip()
            if not s:
                continue
            print("=>", convert_one(s))
        except KeyboardInterrupt:
            print("\n終了します。")
            break

if __name__ == "__main__":
    main()
