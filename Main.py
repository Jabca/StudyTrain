from tkinter import *
from programmLogic.Figures import Cube, Prism, Pyramid, Tetrahedron
#from PIL import ImageGrab


class Program:
    def __init__(self, root, window_width=400, window_height=540, canvas_width=400, canvas_height=350):
        self.width = window_width
        self.height = window_height
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.figure = None

        self.root_window = root
        self.root_window.geometry(f'{self.width}x{self.height}')
        self.root_window.configure(bg='white')

        self.root_canvas = Canvas(self.root_window, width=self.canvas_width, height=self.canvas_height, bg='#f3f3f3')
        self.root_canvas.pack(side=BOTTOM)
        self.render_window()
        self.update_window()

    def update_window(self):
        self.update_canvas()
        for el in list(self.list_sections.curselection())[::-1]:
            self.list_sections.delete(el)
        if self.figure is not None:
            for i, section in enumerate(sorted(self.figure.sections, key=lambda x: x[0])):
                self.list_sections.insert(i, section[0])
        if self.figure is not None:
            try:
                self.scale.set(self.figure.projecting_angle)
            except ValueError:
                self.scale.set(45)
        

    def update_canvas(self):
        self.root_canvas.delete("all")
        if(self.figure is not None):
            self.figure.render()
        self.root_canvas.update()

    def render_window(self):
        b_figure = Button(text="Change figure to:")
        b_figure.place(relwidth=0.3, relheight=0.1)
        b_figure['command'] = lambda: self.change_figure_to(figures[list_figures.get(list_figures.curselection()[0])])

        list_figures = Listbox()
        for figure in sorted(figures.keys()):
            list_figures.insert(END, figure)
        list_figures.place(relwidth=0.3, relheight=0.1, relx=0.31)

        list_sections = Listbox()
        list_sections.place(relwidth=0.3, relheight=0.1, relx=0.31, rely=0.12)

        b_dot = Button(text='Add dot to:')
        b_dot.place(relwidth=0.3, relheight=0.1, rely=0.12)
        b_dot['command'] = lambda: self.add_dot(list_sections.get(list_sections.curselection()[0]),
                                                prop=float(proportion.get()))

        b_clear = Button(text='Clear dots')
        b_clear.place(relwidth=0.3, relheight=0.1, relx=0.62)
        b_clear['command'] = lambda: self.clear_dots()

        proportion = Spinbox(values=(0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0))
        proportion.delete(0, "end")
        proportion.insert(0, '0.5')
        proportion.place(rely=0.12, relx=0.62, relwidth=0.3)

        scrollbar = Scrollbar()
        scrollbar.place(relwidth=0.05, relheight=0.1, relx=0.56, rely=0.12)
        list_sections.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=list_sections.yview)

        b_cross = Button(text='Cross')
        b_cross.place(relwidth=0.3, relheight=0.1, relx=0.62, rely=0.17)
        b_cross['command'] = lambda: self.cross_with_plain()

        w2 = Scale(from_=0, to=90, tickinterval=30, orient=HORIZONTAL)
        w2.place(relwidth=0.6, relheight=0.12, rely=0.22, relx=0.01)
        w2.bind("<Motion>", lambda x: self.change_angle(w2.get()))

        save_b = Button(text='↓')
        save_b.place(relx=0.75, rely=0.28, relwidth=0.05, relheight=0.05)
        save_b['command'] = lambda: self.getter()

        self.list_sections = list_sections
        self.scale = w2

        self.update_window()

    def change_angle(self, angle: int) -> None:
        if self.figure is not None:
            if self.figure.projecting_angle != angle:
                self.figure.set_angle(angle)
                self.update_canvas()

    def change_figure_to(self, fig):
        if self.figure is not None:
            self.figure.parent = None
        fig.parent = self
        self.figure = fig
        self.update_window()

    def add_dot(self, section, prop=0.5):
        if self.figure is not None:
            self.figure.add_dot_on_section(section, prop)
            self.update_canvas()
        else:
            print('<Error> figure is not declared')

    def getter(self):
        x = self.root_window.winfo_rootx() + self.root_canvas.winfo_x()
        y = self.root_window.winfo_rooty() + self.root_canvas.winfo_y()
        x1 = x + self.root_canvas.winfo_width()
        y1 = y + self.root_canvas.winfo_height()
        ImageGrab.grab().crop((x, y, x1, y1)).save("images/save.jpg")

    def clear_dots(self):
        self.figure.added_dots.clear()
        self.figure.secant_plain = None
        self.figure.plain_crossing_points.clear()
        self.figure.additional_dots.clear()
        self.update_canvas()

    def cross_with_plain(self):
        if self.figure is None:
            print('<Error> figure is not defined')
            return None
        self.figure.cross_figure_with_plain()
        self.update_canvas()


pyramid = Pyramid(None, size=200, x_move=40)
cube = Cube(None, size=200, x_move=40, y_move=240)
prism = Prism(None, size=140, x_move=0, y_move=180)
tetrahedron = Tetrahedron(None, size=200, x_move=70, y_move=210)

# cube.

figures = {'Cube': cube, 'Pyramid': pyramid, 'Prism': prism, 'Tetrahedron': tetrahedron}


def main():
    root = Tk()
    ex = Program(root)
    ex.render_window()
    root.mainloop()


if __name__ == '__main__':
    main()
