from tkinter import *

from gui import InteractiveWindow
from shared_objects import figures


def main():
    root = Tk()
    ex = InteractiveWindow(root, figures)
    ex.render_window()
    root.mainloop()


if __name__ == '__main__':
    main()
