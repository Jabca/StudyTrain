from tkinter import *
from shared_objects import figures
from gui import StartingDialog


def main():
    root = Tk()
    ex = StartingDialog(root, figures)
    root.mainloop()


if __name__ == '__main__':
    main()
