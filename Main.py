from tkinter import *
from random import choice


class Program:
    def __init__(self, root, window_width=400, window_height=500, canvas_width=400, canvas_height=350):
        self.width = window_width
        self.height = window_height
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.figure = None

        self.root_window = root
        self.root_window.geometry(f'{self.width}x{self.height}+500+300')
        self.root_window.configure(bg='#ACC3A6')

        self.root_canvas = Canvas(self.root_window, width=self.canvas_width, height=self.canvas_height, bg='#F5D6BA')
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

        b_figure = Button(text="Change figure to:", bg='#F49D6E')
        b_figure.place(relwidth=0.3, relheight=0.1)
        b_figure['command'] = lambda: self.change_figure_to(figures[list_figures.get(list_figures.curselection()[0])])
        self.widgets.append(b_figure)

        list_figures = Listbox(bg='#F49D6E')
        for figure in figures.keys():
            list_figures.insert(END, figure)
        list_figures.place(relwidth=0.3, relheight=0.1, relx=0.31)
        self.widgets.append(list_figures)

        list_sections = Listbox(bg='#F49D6E')
        try:
            for section in self.figure.sections:
                list_sections.insert(END, section[0])
        except AttributeError:
            pass
        list_sections.place(relwidth=0.3, relheight=0.1, relx=0.31, rely=0.12)
        self.widgets.append(list_sections)

        b_dot = Button(text='Add dot to:', bg='#F49D6E')
        b_dot.place(relwidth=0.3, relheight=0.1, rely=0.12)
        b_dot['command'] = lambda: self.add_dot(list_sections.get(list_sections.curselection()[0]),
                                                prop=float(proportion.get()))
        self.widgets.append(b_dot)

        b_clear = Button(text='Clear dots', bg='#F49D6E')
        b_clear.place(relwidth=0.3, relheight=0.1, relx=0.62)
        b_clear['command'] = lambda: self.clear_dots()
        self.widgets.append(b_clear)

        proportion = Spinbox(values=(0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0), bg='#F49D6E')
        proportion.delete(0, "end")
        proportion.insert(0, '0.6')
        proportion.place(rely=0.12, relx=0.62, relwidth=0.3)
        self.widgets.append(proportion)

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


class Figure:
    def __init__(self, parent, x_move, y_move):
        self.sections = []
        self.dots_cords = {}
        self.x_move = x_move
        self.y_move = y_move
        self.parent = parent
        self.added_dots = []
        self.planes = []

    def add_dot_on_section(self, section, prop):
        d1, d2 = self.get_cords_of_section(section)
        delta_x = d2[0] - d1[0]
        delta_y = d2[1] - d1[1]
        x = d1[0] + delta_x * prop
        y = d1[1] + delta_y * prop
        self.added_dots.append((x, y))

    def get_cords_of_section(self, string):
        string = sorted(list(string))
        d1 = list(self.dots_cords[string[0]])
        d2 = list(self.dots_cords[string[1]])
        d1[0] += self.x_move
        d2[0] += self.x_move
        d1[1] += self.y_move
        d2[1] += self.y_move
        return d1, d2

    def render(self):
        canvas = self.parent.root_canvas
        for line in self.sections:
            d1, d2 = self.get_cords_of_section(line[0])
            coordinates = (d1[0], d1[1], d2[0], d2[1])
            if not line[1]:
                canvas.create_line(coordinates, width=5)
            else:
                canvas.create_line(coordinates, dash=(5, 5), width=5)

        size = 6
        for dot in self.added_dots:
            x1, y1 = map(int, [(dot[0] - size), (dot[1] - size)])
            x2, y2 = map(int, [(dot[0] + size), (dot[1] + size)])
            canvas.create_oval(x1, y1, x2, y2, fill='green')

        for verge in self.dots_cords.keys():
            x, y = self.dots_cords[verge][0] - 14, self.dots_cords[verge][1] - 14
            canvas.create_text(x + self.x_move, y + self.y_move,
                               text=verge,
                               justify=CENTER, font=("Verdana", 15), fill='#A40E4C')


class Cube(Figure):
    def __init__(self, canvas, size=100, x_move=20, y_move=20):
        super().__init__(canvas, x_move=x_move, y_move=y_move)
        # 'ABCDabcd'
        self.sections.append(('Aa', False))
        self.sections.append(('AB', True))
        self.sections.append(('AD', False))
        self.sections.append(('BC', True))
        self.sections.append(('Bb', True))
        self.sections.append(('CD', False))
        self.sections.append(('Cc', False))
        self.sections.append(('Dd', False))
        self.sections.append(('ab', False))
        self.sections.append(('ad', False))
        self.sections.append(('bc', False))
        self.sections.append(('cd', False))

        self.dots_cords['A'] = (0, int(1.5 * size))
        self.dots_cords['B'] = (int(0.5 * size), size)
        self.dots_cords['C'] = (int(1.5 * size), size)
        self.dots_cords['D'] = (size, int(1.5 * size))
        self.dots_cords['a'] = (0, int(0.5 * size))
        self.dots_cords['b'] = (int(0.5 * size), 0)
        self.dots_cords['c'] = (int(1.5 * size), 0)
        self.dots_cords['d'] = (size, int(0.5 * size))


class Pyramid(Figure):
    def __init__(self, canvas, size=100, x_move=20, y_move=20):
        super().__init__(canvas, x_move=x_move, y_move=y_move)

        self.sections.append(('AB', True))
        self.sections.append(('AD', False))
        self.sections.append(('AS', False))
        self.sections.append(('BC', True))
        self.sections.append(('BS', True))
        self.sections.append(('CD', False))
        self.sections.append(('CS', False))
        self.sections.append(('DS', False))

        self.dots_cords['S'] = (int(size * 2 / 3), 0)
        self.dots_cords['A'] = (0, int(size * 7 / 6))
        self.dots_cords['D'] = (size, int(size * 7 / 6))
        self.dots_cords['B'] = (int(size / 2), int(size * 5 / 6))
        self.dots_cords['C'] = (int(1.5 * size), int(size * 5 / 6))


class Prism(Figure):
    def __init__(self, canvas, size=100, x_move=20, y_move=20):
        super().__init__(canvas, x_move=x_move, y_move=y_move)

        self.dots_cords['A'] = (int(size * 1 / 5), int(size * 7 / 5))
        self.dots_cords['B'] = (int(size * 4 / 5), int(size * 7 / 5))
        self.dots_cords['C'] = (int(size * 6 / 5), int(size * 6 / 5))
        self.dots_cords['D'] = (size, size)
        self.dots_cords['E'] = (int(2 / 5 * size), size)
        self.dots_cords['a'] = (int(1 / 5 * size), int(size * 2 / 5))
        self.dots_cords['b'] = (int(4 / 5 * size), int(size * 2 / 5))
        self.dots_cords['c'] = (int(6 / 5 * size), int(size * 1 / 5))
        self.dots_cords['d'] = (size, 0)
        self.dots_cords['e'] = (int(2 / 5 * size), 0)
        self.dots_cords['f'] = (0, int(size * 1 / 5))
        self.dots_cords['F'] = (0, int(6 / 5 * size))

        self.sections.append(('AB', False))
        self.sections.append(('Aa', False))
        self.sections.append(('AF', False))
        self.sections.append(('Bb', False))
        self.sections.append(('BC', False))
        self.sections.append(('Cc', False))
        self.sections.append(('CD', True))
        self.sections.append(('Dd', True))
        self.sections.append(('DE', True))
        self.sections.append(('Ee', True))
        self.sections.append(('EF', True))
        self.sections.append(('Ff', False))
        self.sections.append(('ab', False))
        self.sections.append(('bc', False))
        self.sections.append(('cd', False))
        self.sections.append(('de', False))
        self.sections.append(('ef', False))
        self.sections.append(('af', False))


pyr = Pyramid(None, size=200, x_move=40, y_move=30)
cube = Cube(None, size=200, x_move=40, y_move=30)
prism = Prism(None, size=200, x_move=70, y_move=30)
figures = {'Cube': cube, 'Pyramid': pyr, 'Prism': prism}


def main():
    root = Tk()
    ex = Program(root)
    ex.render_window()
    root.mainloop()


if __name__ == '__main__':
    main()
