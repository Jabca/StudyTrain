from tkinter import *
from Basic_math import Plain, Straight
from Figures import Cube, Prism, Pyramid, Tetrahedron


class Program:
    def __init__(self, root, window_width=400, window_height=500, canvas_width=400, canvas_height=350):
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
        self.widgets = []

    def render_window(self):
        self.root_canvas.delete('all')
        for el in self.widgets:
            el.destroy()
        self.widgets.clear()

        if self.figure is not None:
            self.figure.render()
            self.root_canvas.update()

        b_figure = Button(text="Change figure to:")
        b_figure.place(relwidth=0.3, relheight=0.1)
        b_figure['command'] = lambda: self.change_figure_to(figures[list_figures.get(list_figures.curselection()[0])])
        self.widgets.append(b_figure)

        list_figures = Listbox()
        for figure in figures.keys():
            list_figures.insert(END, figure)
        list_figures.place(relwidth=0.3, relheight=0.1, relx=0.31)
        self.widgets.append(list_figures)

        list_sections = Listbox()
        try:
            for section in self.figure.sections:
                list_sections.insert(END, section[0])
        except AttributeError:
            pass
        list_sections.place(relwidth=0.3, relheight=0.1, relx=0.31, rely=0.12)
        self.widgets.append(list_sections)

        b_dot = Button(text='Add dot to:')
        b_dot.place(relwidth=0.3, relheight=0.1, rely=0.12)
        b_dot['command'] = lambda: self.add_dot(list_sections.get(list_sections.curselection()[0]),
                                                prop=float(proportion.get()))
        self.widgets.append(b_dot)

        b_clear = Button(text='Clear dots')
        b_clear.place(relwidth=0.3, relheight=0.1, relx=0.62)
        b_clear['command'] = lambda: self.clear_dots()
        self.widgets.append(b_clear)

        proportion = Spinbox(values=(0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0))
        proportion.delete(0, "end")
        proportion.insert(0, '0.5')
        proportion.place(rely=0.12, relx=0.62, relwidth=0.3)
        self.widgets.append(proportion)

        scrollbar = Scrollbar()
        scrollbar.place(relwidth=0.05, relheight=0.1, relx=0.56, rely=0.12)
        list_sections.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=list_sections.yview)
        self.widgets.append(scrollbar)

    def change_figure_to(self, fig):
        if self.figure is not None:
            self.figure.parent = None
        fig.parent = self
        self.figure = fig
        self.render_window()

    def add_dot(self, section, prop=0.5):
        if self.figure is not None:
            self.figure.add_dot_on_section(section, prop)
            self.render_window()
        else:
            print('<Error> figure is not declared')

    def clear_dots(self):
        self.figure.added_dots.clear()
        self.render_window()


pyramid = Pyramid(None, size=200, x_move=40)
cube = Cube(None, size=200, x_move=40, y_move=240)
prism = Prism(None, size=140, x_move=0, y_move=180)
tetrahedron = Tetrahedron(None, size=200, x_move=70, y_move=210)

figures = {'Cube': cube, 'Pyramid': pyramid, 'Prism': prism, 'Tetrahedron': tetrahedron}


def main():
    root = Tk()
    ex = Program(root)
    ex.render_window()
    root.mainloop()


if __name__ == '__main__':
    main()
