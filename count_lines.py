# count_lines.py

import os
import sys

# ── コマンドライン引数としてファイルパスを受け取る ──
# 例：python count_lines.py "C:/path/to/file.txt"
if len(sys.argv) < 2:
    print("使い方: python count_lines.py <ファイルのパス>")
    sys.exit(1)

file_path = sys.argv[1]

# ── ファイルが存在するかチェック ──
if not os.path.isfile(file_path):
    print(f"エラー: ファイルが見つかりません → {file_path}")
    sys.exit(1)

# ── 行をすべて読み込んで数を調べる ──
with open(file_path, encoding="utf-8") as f:
    lines = f.readlines()

count = len(lines)
print(f"{os.path.basename(file_path)} の行数は {count} 行です")
