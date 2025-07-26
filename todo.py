#!/usr/bin/env python3
import json
import os
import argparse

DATA_FILE = 'todo.json'

def load_tasks():
    """保存ファイルがあれば読み込み、なければ空リストを返す"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    """リストをJSONファイルに保存する"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def list_tasks(tasks):
    """タスク一覧を番号付きで表示"""
    if not tasks:
        print("やることはまだ登録されていません。")
        return
    for i, t in enumerate(tasks, start=1):
        status = '✅' if t['done'] else '❌'
        print(f"{i}. {status} {t['task']}")

def add_task(tasks, text):
    """新しいタスクを追加"""
    tasks.append({'task': text, 'done': False})
    save_tasks(tasks)
    print(f"「{text}」を追加しました。")

def complete_task(tasks, index):
    """タスクを完了済みにする"""
    try:
        tasks[index-1]['done'] = True
        save_tasks(tasks)
        print(f"{index}番を完了にしました。")
    except IndexError:
        print("番号が違います。")

def delete_task(tasks, index):
    """タスクを削除する"""
    try:
        removed = tasks.pop(index-1)
        save_tasks(tasks)
        print(f"{index}番「{removed['task']}」を削除しました。")
    except IndexError:
        print("番号が違います。")

def main():
    parser = argparse.ArgumentParser(description='簡単ToDoリスト管理ツール')
    sub = parser.add_subparsers(dest='cmd')

    sub.add_parser('list', help='タスク一覧を表示')

    p_add = sub.add_parser('add', help='タスクを追加')
    p_add.add_argument('text', help='追加するタスク内容')

    p_done = sub.add_parser('done', help='タスクを完了にする')
    p_done.add_argument('num', type=int, help='完了にするタスク番号')

    p_del = sub.add_parser('del', help='タスクを削除')
    p_del.add_argument('num', type=int, help='削除するタスク番号')

    args = parser.parse_args()
    tasks = load_tasks()

    if args.cmd == 'list':
        list_tasks(tasks)
    elif args.cmd == 'add':
        add_task(tasks, args.text)
    elif args.cmd == 'done':
        complete_task(tasks, args.num)
    elif args.cmd == 'del':
        delete_task(tasks, args.num)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
