import datetime
import os
from tkinter import *

from gui.approval_window import ApproveWindow


class StartingDialog:
    def __init__(self, root, figures):
        self.root_window = root
        self.width = 150
        self.height = 70
        self.root_window.geometry(f'{self.width}x{self.height}')
        self.root_window.configure(bg='white')
        self.figures = figures
        self.root_window.winfo_toplevel().title("Generate")

        self.render_window()

        self.root_window.bind("<Up>", lambda x: self.increment_spinbox)
        self.root_window.bind("<Down>", lambda x: self.decrement_spinbox)
        self.root_window.bind("<Return>", self.enter_handler)


    def decrement_spinbox(self, e):
        prev = int(self.spinbox.get())
        self.spinbox.delete(0, "end")
        self.spinbox.insert(0, prev-1)

    def increment_spinbox(self, e):
        prev = int(self.spinbox.get())
        self.spinbox.delete(0, "end")
        self.spinbox.insert(0, prev + 1)

    def enter_handler(self, e):
        self.start_generating()

    def render_window(self):
        self.label = Label(text="Number of tasks:")
        self.label.pack(fill=X)

        self.spinbox = Spinbox(from_=1, to=100)
        self.spinbox.delete(0, "end")
        self.spinbox.insert(0, 25)
        self.spinbox.pack(fill=X)

        self.start_b = Button(text="Start generating")
        self.start_b.pack(fill=X)
        self.start_b["command"] = lambda: self.start_generating()

        self.spinbox.focus_set()

    def start_generating(self):
        if "res" not in [name for name in os.listdir(".")]:
            os.mkdir("res")
        now = datetime.datetime.now()
        try:
            root_folder_name = f"res/{now.day}-{now.month}-{now.year}_{now.hour}-{now.minute}-{now.second}"
            os.mkdir(root_folder_name)
        except FileExistsError:
            return

        os.mkdir(f"{root_folder_name}/teacher")
        os.mkdir(f"{root_folder_name}/students")

        to_generate = int(self.spinbox.get())
        self.root_window.destroy()

        child_window = Tk()
        ex = ApproveWindow(child_window, self.figures, root_folder_name, to_generate)
        ex.generate_next_figure()
        ex.update_window()
        child_window.mainloop()
