# main.py
# ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
# 支出管理アプリ（CSV保存・集計）
# ・追加インストール不要（標準ライブラリのみ）
# ・中学生でも読めるように、短く・やさしいコードとコメント
# ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
from pathlib import Path
import csv
from datetime import datetime
from collections import defaultdict

# CSVファイルの場所（data/expenses.csv）
DATA_DIR = Path("data")
CSV_PATH = DATA_DIR / "expenses.csv"

# CSVヘッダー（列名）
HEADERS = ["date", "category", "memo", "amount"]

def ensure_csv_exists():
    """CSVファイルが無ければフォルダと空のCSVを作る"""
    DATA_DIR.mkdir(exist_ok=True)
    if not CSV_PATH.exists():
        with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)  # ヘッダー行

def valid_date(s: str) -> bool:
    """YYYY-MM-DD 形式かチェック"""
    try:
        datetime.strptime(s, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def read_all():
    """CSVの全行を読み込んで、辞書のリストで返す"""
    ensure_csv_exists()
    rows = []
    with CSV_PATH.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append({
                "date": r["date"],
                "category": r["category"],
                "memo": r["memo"],
                "amount": int(r["amount"])  # 文字→数値
            })
    return rows

def add_record(date:str, category:str, memo:str, amount:int):
    """1件の支出をCSVに追加"""
    ensure_csv_exists()
    with CSV_PATH.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([date, category, memo, str(amount)])

def print_line(char="-", n=40):
    print(char * n)

def show_table(rows):
    """固定幅でカンタンな表を表示"""
    if not rows:
        print("データがありません。")
        return
    print_line("=")
    print(f"{'日付':<12} {'カテゴリ':<10} {'メモ':<16} {'金額':>8}")
    print_line("-")
    total = 0
    for r in rows:
        print(f"{r['date']:<12} {r['category']:<10} {r['memo']:<16} {r['amount']:>8,}")
        total += r["amount"]
    print_line("-")
    print(f"{'合計':<12} {'':<10} {'':<16} {total:>8,}")
    print_line("=")

def list_records():
    rows = read_all()
    # 日付の新しい順で並び替え
    rows.sort(key=lambda r: r["date"], reverse=True)
    show_table(rows)

def summarize_by_month():
    rows = read_all()
    sums = defaultdict(int)  # key: 'YYYY-MM', value: 合計
    for r in rows:
        ym = r["date"][:7]  # 'YYYY-MM'
        sums[ym] += r["amount"]
    show_summary_table(sums, "月ごとの合計（YYYY-MM）")

def summarize_by_category():
    rows = read_all()
    sums = defaultdict(int)  # key: category, value: 合計
    for r in rows:
        sums[r["category"]] += r["amount"]
    show_summary_table(sums, "カテゴリごとの合計")

def show_summary_table(counter: dict, title: str):
    if not counter:
        print("データがありません。")
        return
    print_line("=")
    print(title)
    print_line("-")
    total = 0
    # 表示はキーで並び替え（見やすさ重視）
    for k in sorted(counter.keys()):
        v = counter[k]
        print(f"{k:<16} {v:>10,}")
        total += v
    print_line("-")
    print(f"{'総合計':<16} {total:>10,}")
    print_line("=")

def prompt_add():
    """ユーザーから入力を受けて追加"""
    print("支出の追加：")
    date = input("日付（YYYY-MM-DD）：").strip()
    if not valid_date(date):
        print("日付の形式が正しくありません。例：2025-04-01")
        return
    category = input("カテゴリ（例：食費/交通/趣味など）：").strip() or "未分類"
    memo = input("メモ（例：コンビニ、バス代など）：").strip() or "-"
    amount_str = input("金額（半角数字）：").strip()
    if not amount_str.isdigit():
        print("金額は半角数字で入力してください。")
        return
    amount = int(amount_str)
    add_record(date, category, memo, amount)
    print("✅ 追加しました！")

def main_menu():
    ensure_csv_exists()
    while True:
        print("\n===== 支出管理アプリ =====")
        print("1) 支出を追加する")
        print("2) 記録を一覧表示する")
        print("3) 月ごとに集計する")
        print("4) カテゴリごとに集計する")
        print("5) 終了する")
        choice = input("番号を入力してEnter：").strip()

        if choice == "1":
            prompt_add()
        elif choice == "2":
            list_records()
        elif choice == "3":
            summarize_by_month()
        elif choice == "4":
            summarize_by_category()
        elif choice == "5":
            print("終了します。おつかれさま！")
            break
        else:
            print("1〜5の番号で選んでください。")

if __name__ == "__main__":
    main_menu()
