# app.py
# メニュー付きメモ帳：新規 / 開く / 上書き保存 / 名前を付けて保存 / 終了

import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

current_path = None  # 今開いているファイルの場所（未保存ならNone）

def set_title(path: Path | None):
    name = path.name if path else "無題"
    root.title(f"{name} - シンプルメモ帳")

def new_file():
    global current_path
    if confirm_discard():
        text_area.delete("1.0", tk.END)
        current_path = None
        set_title(current_path)

def open_file():
    global current_path
    if not confirm_discard():
        return
    path = filedialog.askopenfilename(
        filetypes=[("テキストファイル", "*.txt"), ("すべてのファイル", "*.*")]
    )
    if not path:
        return
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        text_area.delete("1.0", tk.END)
        text_area.insert("1.0", content)
        current_path = Path(path)
        set_title(current_path)
        text_area.edit_modified(False)  # 変更フラグをリセット
    except Exception as e:
        messagebox.showerror("エラー", f"開けませんでした:\n{e}")

def save():
    if current_path is None:
        save_as()
    else:
        try:
            with open(current_path, "w", encoding="utf-8") as f:
                f.write(text_area.get("1.0", tk.END))
            messagebox.showinfo("保存完了", f"上書き保存しました:\n{current_path}")
            text_area.edit_modified(False)
        except Exception as e:
            messagebox.showerror("エラー", f"保存に失敗:\n{e}")

def save_as():
    global current_path
    path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("テキストファイル", "*.txt"), ("すべてのファイル", "*.*")],
        title="名前を付けて保存"
    )
    if not path:
        return
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text_area.get("1.0", tk.END))
        current_path = Path(path)
        set_title(current_path)
        messagebox.showinfo("保存完了", f"保存しました:\n{path}")
        text_area.edit_modified(False)
    except Exception as e:
        messagebox.showerror("エラー", f"保存に失敗:\n{e}")

def on_close():
    if confirm_discard():
        root.destroy()

def confirm_discard() -> bool:
    """未保存の変更があれば確認してから進む"""
    if text_area.edit_modified():
        ans = messagebox.askyesnocancel("確認", "変更が保存されていません。保存しますか？")
        if ans is None:
            return False  # キャンセル
        if ans:  # はい → 保存して続行
            save()
            # 保存に成功したら変更フラグはFalseになる
            return not text_area.edit_modified()
        # いいえ → 破棄して続行
        return True
    return True

# --- UI 作成 ---
root = tk.Tk()
set_title(None)
root.geometry("800x600")

# テキスト欄
text_area = tk.Text(root, wrap="word", font=("Meiryo", 12), undo=True)
text_area.pack(fill="both", expand=True)

# メニュー
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="新規", command=new_file)
filemenu.add_command(label="開く", command=open_file)
filemenu.add_separator()
filemenu.add_command(label="上書き保存", command=save)
filemenu.add_command(label="名前を付けて保存", command=save_as)
filemenu.add_separator()
filemenu.add_command(label="終了", command=on_close)
menubar.add_cascade(label="ファイル", menu=filemenu)
root.config(menu=menubar)

# ウィンドウを閉じる時の確認
root.protocol("WM_DELETE_WINDOW", on_close)

# 文字を打ったら「変更あり」フラグを立てる
def mark_modified(event=None):
    text_area.edit_modified(True)
text_area.bind("<<Modified>>", lambda e: None)  # 既定の挙動抑制
text_area.bind("<Key>", mark_modified)

root.mainloop()
