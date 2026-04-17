import tkinter as tk
from tkinter import messagebox
import time

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("ポモドーロ・タイマー")
        self.root.geometry("300x200")

        self.target_time = 25 * 60  # 最初は25分
        self.is_running = False
        self.remaining_time = self.target_time

        # UI部分
        self.label = tk.Label(root, text="25:00", font=("Helvetica", 48))
        self.label.pack(pady=20)

        self.start_button = tk.Button(root, text="Start", command=self.toggle_timer)
        self.start_button.pack(side="left", padx=40)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset_timer)
        self.reset_button.pack(side="right", padx=40)

        self.update_clock()

    def update_clock(self):
        mins, secs = divmod(self.remaining_time, 60)
        self.label.config(text=f"{mins:02d}:{secs:02d}")
        
        if self.is_running and self.remaining_time > 0:
            self.remaining_time -= 1
            self.root.after(1000, self.update_clock)
        elif self.remaining_time <= 0:
            self.is_running = False
            messagebox.showinfo("時間です！", "休憩（または集中）の時間ですよ！")
            self.reset_timer()
        else:
            self.root.after(1000, self.update_clock)

    def toggle_timer(self):
        if self.is_running:
            self.is_running = False
            self.start_button.config(text="Start")
        else:
            self.is_running = True
            self.start_button.config(text="Stop")

    def reset_timer(self):
        self.is_running = False
        self.remaining_time = self.target_time
        self.start_button.config(text="Start")
        self.label.config(text="25:00")

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()
