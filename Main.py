from tkinter import *
from lib.figures import Cube, Prism, Pyramid, Tetrahedron
from gui.main_window import MainWindow


pyramid = Pyramid(None, size=200, x_move=40)
cube = Cube(None, size=200, x_move=40, y_move=240)
prism = Prism(None, size=140, x_move=0, y_move=180)
tetrahedron = Tetrahedron(None, size=200, x_move=70, y_move=210)

figures = {'Cube': cube, 'Pyramid': pyramid, 'Prism': prism, 'Tetrahedron': tetrahedron}


def main():
    root = Tk()
    ex = MainWindow(root, figures)
    ex.render_window()
    root.mainloop()


if __name__ == '__main__':
    main()
