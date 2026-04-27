import tkinter as tk
from tkinter import messagebox

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Pro")
        self.root.geometry("350x400")
        self.root.configure(bg="#2E3440") # ダーク北欧風カラー
        self.root.attributes("-topmost", True) # 常に最前面

        # 設定
        self.work_time = 25 * 60
        self.break_time = 5 * 60
        self.remaining_time = self.work_time
        self.is_running = False
        self.is_work_session = True
        self.timer_id = None # 重複動作防止用

        self.setup_ui()

    def setup_ui(self):
        # スタイル設定
        label_style = {"bg": "#2E3440", "fg": "#D8DEE9"}
        
        self.state_label = tk.Label(self.root, text="FOCUS TIME", font=("Helvetica", 18, "bold"), **label_style)
        self.state_label.pack(pady=20)

        self.timer_label = tk.Label(self.root, text="25:00", font=("Helvetica", 60), bg="#2E3440", fg="#88C0D0")
        self.timer_label.pack(pady=10)

        # 入力エリアのフレーム
        input_frame = tk.Frame(self.root, bg="#2E3440")
        input_frame.pack(pady=10)

        entry_opt = {"width": 5, "bg": "#3B4252", "fg": "white", "insertbackground": "white", "relief": "flat"}
        
        tk.Label(input_frame, text="Work:", **label_style).grid(row=0, column=0, padx=5)
        self.work_entry = tk.Entry(input_frame, **entry_opt)
        self.work_entry.insert(0, "25")
        self.work_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Break:", **label_style).grid(row=0, column=2, padx=5)
        self.break_entry = tk.Entry(input_frame, **entry_opt)
        self.break_entry.insert(0, "5")
        self.break_entry.grid(row=0, column=3, padx=5)

        # ボタンエリア
        btn_frame = tk.Frame(self.root, bg="#2E3440")
        btn_frame.pack(pady=20)

        self.start_button = tk.Button(btn_frame, text="START", command=self.toggle_timer, 
                                      width=10, bg="#A3BE8C", fg="#2E3440", font=("Helvetica", 10, "bold"))
        self.start_button.grid(row=0, column=0, padx=10)

        self.reset_button = tk.Button(btn_frame, text="RESET", command=self.reset_timer, 
                                      width=10, bg="#EBCB8B", fg="#2E3440", font=("Helvetica", 10, "bold"))
        self.reset_button.grid(row=0, column=1, padx=10)

    def update_clock(self):
        if self.is_running and self.remaining_time >= 0:
            mins, secs = divmod(self.remaining_time, 60)
            self.timer_label.config(text=f"{mins:02d}:{secs:02d}")
            
            if self.remaining_time == 0:
                self.is_running = False
                self.switch_session()
                return

            self.remaining_time -= 1
            self.timer_id = self.root.after(1000, self.update_clock)

    def toggle_timer(self):
        if self.is_running:
            self.is_running = False
            self.start_button.config(text="START", bg="#A3BE8C")
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
        else:
            # 設定の反映（開始時のみ）
            try:
                self.work_time = int(self.work_entry.get()) * 60
                self.break_time = int(self.break_entry.get()) * 60
            except ValueError:
                messagebox.showerror("Error", "数字を入力してください")
                return

            self.is_running = True
            self.start_button.config(text="STOP", bg="#BF616A")
            self.update_clock()

    def switch_session(self):
        if self.is_work_session:
            self.is_work_session = False
            self.remaining_time = self.break_time
            self.state_label.config(text="TAKE A BREAK", fg="#EBCB8B")
            messagebox.showinfo("Done!", "作業終了！休憩しましょう")
        else:
            self.is_work_session = True
            self.remaining_time = self.work_time
            self.state_label.config(text="FOCUS TIME", fg="#D8DEE9")
            messagebox.showinfo("Back to Work", "休憩終了！集中しましょう")
        
        self.start_button.config(text="START", bg="#A3BE8C")
        self.update_clock() # 次のセッションの初期値を表示

    def reset_timer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.is_running = False
        self.is_work_session = True
        self.remaining_time = int(self.work_entry.get()) * 60
        self.state_label.config(text="FOCUS TIME", fg="#D8DEE9")
        self.timer_label.config(text=f"{self.remaining_time//60:02d}:00", fg="#88C0D0")
        self.start_button.config(text="START", bg="#A3BE8C")

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()
