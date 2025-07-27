from datetime import datetime  # 今の日時を使うためのモジュール

while True:
    memo = input("メモを入力してください（終了したいときは 'exit' と入力）：")

    if memo.lower() == "exit":
        print("メモアプリを終了します。")
        break

    # 今の時間を取得して、文字にする
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 書き込む内容を作る（例：2025-07-27 14:30:10 メモ内容）
    entry = f"{timestamp} {memo}\n"

    # ファイルに追記（'a'モードで書くと、どんどん下に追加される）
    with open("memo_log.txt", "a", encoding="utf-8") as f:
        f.write(entry)

# ✅ タイムスタンプを画面にも表示
    print(f"✅ {timestamp} にメモを保存しました！\n")
    
    
    print("✅ メモを保存しました！\n")
