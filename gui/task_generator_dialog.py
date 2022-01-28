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

        self.render_window()
        # self.start_generating()

    def render_window(self):
        self.label = Label(text="Number of tasks:")
        self.label.pack(fill=X)

        self.spinbox = Spinbox(from_=5, to=100)
        self.spinbox.insert(0, 2)
        self.spinbox.pack(fill=X)

        self.start_b = Button(text="Start generating")
        self.start_b.pack(fill=X)
        self.start_b["command"] = lambda: self.start_generating()

    def start_generating(self):
        if "res" not in [name for name in os.listdir(".")]:
            os.mkdir("res")
        now = datetime.datetime.now()
        try:
            root_folder_name = f"res/{now.day}-{now.month}-{now.year}|{now.hour}:{now.minute}:{now.second}"
            os.mkdir(root_folder_name)
        except FileExistsError:
            return

        os.mkdir(f"{root_folder_name}/teacher")
        os.mkdir(f"{root_folder_name}/students")

        to_generate = self.spinbox.get()
        self.root_window.destroy()

        child_window = Tk()
        ex = ApproveWindow(child_window, self.figures, root_folder_name, int(to_generate))
        ex.generate_next_figure()
        ex.update_window()
        child_window.mainloop()
