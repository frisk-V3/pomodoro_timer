import tkinter as tk
from tkinter import messagebox

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("ポモドーロ・タイマー")
        self.root.geometry("320x260")

        # デフォルト時間（秒）
        self.work_time = 25 * 60
        self.break_time = 5 * 60

        self.is_running = False
        self.is_work_session = True  # True = 作業, False = 休憩
        self.remaining_time = self.work_time

        # --- UI ---
        self.state_label = tk.Label(root, text="作業中", font=("Helvetica", 20))
        self.state_label.pack(pady=5)

        self.timer_label = tk.Label(root, text="25:00", font=("Helvetica", 48))
        self.timer_label.pack(pady=10)

        # 時間設定
        frame = tk.Frame(root)
        frame.pack()

        tk.Label(frame, text="作業(分):").grid(row=0, column=0)
        self.work_entry = tk.Entry(frame, width=5)
        self.work_entry.insert(0, "25")
        self.work_entry.grid(row=0, column=1)

        tk.Label(frame, text="休憩(分):").grid(row=1, column=0)
        self.break_entry = tk.Entry(frame, width=5)
        self.break_entry.insert(0, "5")
        self.break_entry.grid(row=1, column=1)

        tk.Button(frame, text="設定反映", command=self.apply_settings).grid(row=2, column=0, columnspan=2, pady=5)

        # ボタン
        self.start_button = tk.Button(root, text="Start", command=self.toggle_timer)
        self.start_button.pack(side="left", padx=40, pady=10)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset_timer)
        self.reset_button.pack(side="right", padx=40, pady=10)

        self.update_clock()

    def apply_settings(self):
        try:
            self.work_time = int(self.work_entry.get()) * 60
            self.break_time = int(self.break_entry.get()) * 60
            self.reset_timer()
        except ValueError:
            messagebox.showerror("エラー", "数字を入力してください")

    def update_clock(self):
        mins, secs = divmod(self.remaining_time, 60)
        self.timer_label.config(text=f"{mins:02d}:{secs:02d}")

        if self.is_running and self.remaining_time > 0:
            self.remaining_time -= 1
            self.root.after(1000, self.update_clock)
        elif self.remaining_time <= 0:
            self.is_running = False
            self.switch_session()
        else:
            self.root.after(1000, self.update_clock)

    def switch_session(self):
        if self.is_work_session:
            messagebox.showinfo("終了！", "作業終了！休憩しましょう")
            self.is_work_session = False
            self.remaining_time = self.break_time
            self.state_label.config(text="休憩中")
        else:
            messagebox.showinfo("終了！", "休憩終了！作業に戻りましょう")
            self.is_work_session = True
            self.remaining_time = self.work_time
            self.state_label.config(text="作業中")

        self.start_button.config(text="Start")

    def toggle_timer(self):
        if self.is_running:
            self.is_running = False
            self.start_button.config(text="Start")
        else:
            self.is_running = True
            self.start_button.config(text="Stop")

    def reset_timer(self):
        self.is_running = False
        self.is_work_session = True
        self.remaining_time = self.work_time
        self.state_label.config(text="作業中")
        self.start_button.config(text="Start")
        self.timer_label.config(text=f"{self.work_time//60:02d}:00")

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()
