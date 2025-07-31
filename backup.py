#!/usr/bin/env python3
# backup_debug.py
# デバッグ出力＋パス改善版バックアップスクリプト

import os
import shutil
import datetime
import sys

def backup_folder(src_folder: str, dest_root: str) -> None:
    # ① コピー元チェック
    if not os.path.exists(src_folder):
        parent = os.path.dirname(src_folder)
        print("ERROR: コピー元フォルダが見つかりません。")
        print(f"  指定パス: {src_folder}")
        # 親ディレクトリの中身一覧を出力
        if os.path.exists(parent):
            print(f"  親ディレクトリ({parent}) の中身一覧:")
            for name in os.listdir(parent):
                print("   -", name)
        else:
            print(f"  親ディレクトリも存在しません: {parent}")
        sys.exit(1)

    # ② コピー先ルートを作成（なければ自動で）
    os.makedirs(dest_root, exist_ok=True)

    # ③ 今日の日付取得＆コピー先フォルダ名組み立て
    today = datetime.datetime.now().strftime('%Y%m%d')
    folder_name = os.path.basename(src_folder.rstrip('/\\'))
    dest_folder = os.path.join(dest_root, f"{folder_name}_{today}")

    # ④ コピー実行
    try:
        shutil.copytree(src_folder, dest_folder)
        print(f"バックアップ完了: {dest_folder}")
    except FileExistsError:
        print(f"ERROR: 既に同名フォルダが存在します: {dest_folder}")
        sys.exit(1)
    except Exception as e:
        print("予期せぬエラー:", e)
        sys.exit(1)

if __name__ == "__main__":
    # —— ここをあなたの環境のパスに書き換えてください —— 
    # Windows の場合、Raw String (r"…") で書くと \ がそのまま扱われます
    src = r"C:\Users\shima\OneDrive\デスクトップ\Pythonチャレンジ\backup_project\backup_sample\src"
    dest_root = r"C:\Users\shima\OneDrive\デスクトップ\Pythonチャレンジ\backup_project\backup_sample\dest"
    # ——————————————————————————————

    # デバッグ出力：カレントディレクトリ
    print("実行時のカレントディレクトリ:", os.getcwd())
    backup_folder(src, dest_root)
