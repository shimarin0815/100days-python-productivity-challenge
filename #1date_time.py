# date_time.py
from datetime import datetime

def main():
    # いまの日時を取得
    now = datetime.now()
    # 「年-月-日 時:分:秒」の形にする
    formatted = now.strftime("%Y-%m-%d %H:%M:%S")
    # 表示
    print("現在の日時:", formatted)

# 直接このファイルを実行したときだけ main() を呼ぶ
if __name__ == "__main__":
    main()
