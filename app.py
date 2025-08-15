import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

SAVE_FILE = "tasks.json"


class TodoApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("TODOリスト - Tkinter")
        self.root.geometry("520x420")

        # データ（辞書のリスト: {"title": 文字列, "done": True/False}）
        self.tasks = []
        self.hide_done = tk.BooleanVar(value=False)

        # --------------- 上部：入力と追加ボタン ---------------
        top = ttk.Frame(self.root, padding=8)
        top.pack(fill="x")

        self.entry = ttk.Entry(top)
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", self.add_task_event)

        add_btn = ttk.Button(top, text="追加", command=self.add_task)
        add_btn.pack(side="left", padx=(8, 0))

        # --------------- 中央：リスト（スクロール付き） ---------------
        mid = ttk.Frame(self.root, padding=(8, 0, 8, 8))
        mid.pack(fill="both", expand=True)

        self.listbox = tk.Listbox(
            mid,
            font=("Meiryo UI", 11),
            activestyle="none",
            selectmode="extended",  # 複数選択で削除しやすい
        )
        self.listbox.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(mid, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

        # ダブルクリックで完了/未完を切り替え
        self.listbox.bind("<Double-1>", self.toggle_done_event)

        # --------------- 下部：操作ボタン群 ---------------
        bottom = ttk.Frame(self.root, padding=8)
        bottom.pack(fill="x")

        done_btn = ttk.Button(bottom, text="完了/未完", command=self.toggle_done)
        done_btn.pack(side="left")

        edit_btn = ttk.Button(bottom, text="編集", command=self.edit_task)
        edit_btn.pack(side="left", padx=6)

        del_btn = ttk.Button(bottom, text="削除", command=self.delete_task)
        del_btn.pack(side="left")

        hide_chk = ttk.Checkbutton(
            bottom, text="完了を隠す", variable=self.hide_done, command=self.refresh_list
        )
        hide_chk.pack(side="right")

        # --------------- メニュー（おまけ） ---------------
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="ファイル", menu=file_menu)
        file_menu.add_command(label="保存", command=self.save_tasks, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="終了", command=self.root.quit)

        help_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="ヘルプ", menu=help_menu)
        help_menu.add_command(label="使い方", command=self.show_help)

        # キーボードショートカット
        self.root.bind("<Control-s>", lambda e: self.save_tasks())
        self.root.bind("<Delete>", lambda e: self.delete_task())

        # 起動時に読み込み → 表示
        self.load_tasks()
        self.refresh_list()

    # ---------- データの読み込み/保存 ----------
    def load_tasks(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r", encoding="utf-8") as f:
                    self.tasks = json.load(f)
            except Exception as e:
                messagebox.showwarning("読み込みエラー", f"tasks.jsonを開けませんでした。\n{e}")
                self.tasks = []
        else:
            self.tasks = []

    def save_tasks(self):
        try:
            with open(SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump(self.tasks, f, ensure_ascii=False, indent=2)
            # ちょっとした達成感フィードバック
            self.root.title("TODOリスト - Tkinter（保存しました）")
            self.root.after(800, lambda: self.root.title("TODOリスト - Tkinter"))
        except Exception as e:
            messagebox.showerror("保存エラー", f"保存に失敗しました。\n{e}")

    # ---------- 表示更新 ----------
    def refresh_list(self):
        self.listbox.delete(0, tk.END)

        # 表示用の一覧を作る（完了を下、未完を上にすると見やすい）
        items = []
        for t in self.tasks:
            if self.hide_done.get() and t.get("done"):
                continue
            mark = "✅" if t.get("done") else "□"
            items.append(f"{mark} {t.get('title')}")

        # 未完→完了 の順に並べる（視認性アップ）
        def sort_key(text):
            return text.startswith("✅")  # False(未完)が先、True(完了)が後

        for s in sorted(items, key=sort_key):
            self.listbox.insert(tk.END, s)

    # ---------- タスク操作 ----------
    def add_task_event(self, event):
        self.add_task()

    def add_task(self):
        title = self.entry.get().strip()
        if not title:
            messagebox.showinfo("入力なし", "タスク名を入力してください。")
            return
        self.tasks.append({"title": title, "done": False})
        self.entry.delete(0, tk.END)
        self.refresh_list()
        self.save_tasks()

    def get_visible_indices(self):
        """現在のListboxの表示における選択されたアイテムの元データindexを返す。
        フィルタやソートがあるため、表示→元データの対応を逆算する。
        """
        selected = self.listbox.curselection()
        if not selected:
            return []

        # 表示中のテキストを順にたどり、元データindexを対応付け
        visible_map = []
        for i, t in enumerate(self.tasks):
            if self.hide_done.get() and t.get("done"):
                continue
            mark = "✅" if t.get("done") else "□"
            visible_map.append((i, f"{mark} {t.get('title')}"))

        # 未完→完了の順でソートした並びを再現
        visible_sorted = sorted(visible_map, key=lambda x: x[1].startswith("✅"))
        picked_indices = [visible_sorted[i][0] for i in selected]
        return picked_indices

    def toggle_done_event(self, event):
        self.toggle_done()

    def toggle_done(self):
        indices = self.get_visible_indices()
        if not indices:
            messagebox.showinfo("未選択", "切り替えるタスクを選んでください。")
            return
        for idx in indices:
            self.tasks[idx]["done"] = not self.tasks[idx]["done"]
        self.refresh_list()
        self.save_tasks()

    def edit_task(self):
        indices = self.get_visible_indices()
        if len(indices) != 1:
            messagebox.showinfo("1つ選択", "編集するタスクを1つだけ選んでください。")
            return
        idx = indices[0]
        current = self.tasks[idx]["title"]
        new_title = simpledialog.askstring("編集", "新しいタスク名：", initialvalue=current)
        if new_title is None:
            return  # キャンセル
        new_title = new_title.strip()
        if not new_title:
            messagebox.showinfo("入力なし", "タスク名を入力してください。")
            return
        self.tasks[idx]["title"] = new_title
        self.refresh_list()
        self.save_tasks()

    def delete_task(self):
        indices = self.get_visible_indices()
        if not indices:
            messagebox.showinfo("未選択", "削除するタスクを選んでください。")
            return
        if not messagebox.askyesno("確認", f"{len(indices)}件のタスクを削除します。よろしいですか？"):
            return
        # 後ろから削除するとindexずれを防げる
        for idx in sorted(indices, reverse=True):
            del self.tasks[idx]
        self.refresh_list()
        self.save_tasks()

    # ---------- ヘルプ ----------
    def show_help(self):
        tips = (
            "使い方：\n"
            "・上の入力欄にタスク名を入れて「追加」またはEnter\n"
            "・タスクをダブルクリックで完了/未完を切替\n"
            "・下のボタンで編集/削除、「完了を隠す」チェックでフィルタ\n"
            "・Ctrl+Sで保存\n"
        )
        messagebox.showinfo("ヘルプ", tips)


def main():
    root = tk.Tk()
    # WindowsでもMacでも見やすいテーマを適用（ttkの標準）
    try:
        style = ttk.Style()
        if "vista" in style.theme_names():
            style.theme_use("vista")
        elif "clam" in style.theme_names():
            style.theme_use("clam")
    except Exception:
        pass
    app = TodoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
