from tkinter import *

from gui.approval_window import ApproveWindow
from shared_objects import figures




def main():
    root = Tk()
    ex = ApproveWindow(root, figures)
    ex.generate_next_figure()
    ex.render_window()
    root.mainloop()


if __name__ == '__main__':
    main()
