#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
シンプルTODO CLI
機能: add / list / done
保存先: ホームディレクトリに .todo_cli.json
使い方:
  python todo.py add "牛乳を買う"
  python todo.py list
  python todo.py list --all
  python todo.py done 3
"""

import argparse
import json
from pathlib import Path
from datetime import datetime

# 保存ファイル（各OSでユーザーのホームフォルダに置く）
DATA_FILE = Path.home() / ".todo_cli.json"

def now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M")

def load_tasks():
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            # 壊れた場合はバックアップして新規作成
            backup = DATA_FILE.with_suffix(".bak.json")
            DATA_FILE.rename(backup)
            print(f"⚠️ データが壊れていたのでバックアップしました: {backup}")
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def next_id(tasks):
    return (max([t["id"] for t in tasks]) + 1) if tasks else 1

def cmd_add(args):
    tasks = load_tasks()
    task = {
        "id": next_id(tasks),
        "title": args.title,
        "done": False,
        "created_at": now_str(),
        "done_at": None
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"✅ 追加しました(ID {task['id']}): {task['title']}")

def format_row(cols, widths):
    # 幅調整してきれいに並べる
    padded = []
    for col, width in zip(cols, widths):
        s = str(col)
        if len(s) > width:
            s = s[: width - 1] + "…"
        padded.append(s.ljust(width))
    return "  ".join(padded)

def cmd_list(args):
    tasks = load_tasks()
    if not args.all:
        tasks = [t for t in tasks if not t["done"]]

    # 新しい順に表示（idの大きい順）
    tasks = sorted(tasks, key=lambda t: t["id"], reverse=True)

    headers = ["ID", "状態", "タイトル", "作成日"]
    widths = [3, 2, 24, 16]  # 見やすい幅

    print(format_row(headers, widths))
    for t in tasks:
        status = "☑" if t["done"] else "☐"
        print(format_row([t["id"], status, t["title"], t["created_at"]], widths))

    if not tasks:
        if args.all:
            print("（タスクはありません）")
        else:
            print("（未完了のタスクはありません。--all で完了含む全件表示）")

def cmd_done(args):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == args.id:
            if t["done"]:
                print(f"ℹ️ すでに完了済みです: ID {args.id}")
            else:
                t["done"] = True
                t["done_at"] = now_str()
                save_tasks(tasks)
                print(f"🎉 完了にしました: ID {args.id} → {t['title']}")
            break
    else:
        print(f"❓ 指定したIDが見つかりません: {args.id}")

def main():
    parser = argparse.ArgumentParser(
        description="シンプルTODO CLI（add/list/done）"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # add
    p_add = sub.add_parser("add", help="タスクを追加します")
    p_add.add_argument("title", help="タスクの内容（例: '英語の宿題をやる'）")
    p_add.set_defaults(func=cmd_add)

    # list
    p_list = sub.add_parser("list", help="タスクを一覧表示します")
    p_list.add_argument("--all", action="store_true", help="完了済みも含めて表示します")
    p_list.set_defaults(func=cmd_list)

    # done
    p_done = sub.add_parser("done", help="タスクを完了にします")
    p_done.add_argument("id", type=int, help="完了にしたいタスクID")
    p_done.set_defaults(func=cmd_done)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
