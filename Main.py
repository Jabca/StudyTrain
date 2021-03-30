from tkinter import *
from math import cos, sin, radians

greek_letters = ['α', 'β', 'γ', 'δ', 'ε', 'θ']

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
    def __init__(self, parent, x_move, y_move, angle, size):
        self.sections = []
        self.dots_cords = {}
        self.x_move = x_move
        self.y_move = y_move
        self.parent = parent
        self.added_dots = {}
        self.projecting_angle = radians(angle)
        self.size = size

    def add_dot_on_section(self, section, prop):
        d1, d2 = self.dots_cords[section[0]], self.dots_cords[section[1]]
        delta_x = d2[0] - d1[0]
        delta_y = d2[1] - d1[1]
        delta_z = d2[2] - d1[0]
        x = d1[0] + delta_x * prop
        y = d1[1] + delta_y * prop
        z = d1[2] + delta_z * prop
        self.added_dots[greek_letters[len(list(self.added_dots.keys()))]] = (x, y, z)
        print(self.added_dots)

    def get_cords_of_section(self, string):

        string = sorted(list(string))
        d1 = self.get_point_cords(string[0])
        d2 = self.get_point_cords(string[1])

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
            cord = self.get_point_cords(dot)
            cord = (cord[0] + self.x_move, cord[1] + self.y_move)
            x1, y1 = map(int, [(cord[0] - size), (cord[1] - size)])
            x2, y2 = map(int, [(cord[0] + size), (cord[1] + size)])
            canvas.create_oval(x1, y1, x2, y2, fill='green')

        for verge in self.dots_cords.keys():
            x, y = self.get_point_cords(verge)[0] - 14, self.get_point_cords(verge)[1] - 14
            canvas.create_text(x + self.x_move, y + self.y_move,
                               text=verge,
                               justify=CENTER, font=("Verdana", 15), fill='blue')

    def get_point_cords(self, point):
        if point in greek_letters:
            d1 = list(self.added_dots[point])
        else:
            d1 = list(self.dots_cords[point])

        return [d1[0] + 0.5 * d1[1] * cos(self.projecting_angle), -1 * d1[2] + 0.5 * d1[1] * sin(self.projecting_angle)]

    def reformat_cords(self):
        for key in self.dots_cords:
            cords = self.dots_cords[key]
            self.dots_cords[key] = (cords[0] * self.size, cords[1] * self.size, cords[2] * self.size)


class Cube(Figure):
    def __init__(self, canvas, size=100, x_move=20, y_move=200, angle=45):
        super().__init__(canvas, x_move=x_move, y_move=y_move, angle=angle, size=size)
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

        self.dots_cords['A'] = (0, 0, 0)
        self.dots_cords['B'] = (1, 0, 0)
        self.dots_cords['C'] = (1, 1, 0)
        self.dots_cords['D'] = (0, 1, 0)
        self.dots_cords['a'] = (0, 0, 1)
        self.dots_cords['b'] = (1, 0, 1)
        self.dots_cords['c'] = (1, 1, 1)
        self.dots_cords['d'] = (0, 1, 1)

        self.reformat_cords()


class Pyramid(Figure):
    def __init__(self, canvas, size=100, x_move=20, y_move=200, angle=45):
        super().__init__(canvas, x_move=x_move, y_move=y_move, angle=angle, size=size)

        self.sections.append(('AB', True))
        self.sections.append(('AD', False))
        self.sections.append(('AS', False))
        self.sections.append(('BC', True))
        self.sections.append(('BS', True))
        self.sections.append(('CD', False))
        self.sections.append(('CS', False))
        self.sections.append(('DS', False))

        self.dots_cords['S'] = (0.5, 0.5, 1)
        self.dots_cords['A'] = (0, 0, 0)
        self.dots_cords['B'] = (1, 0, 0)
        self.dots_cords['C'] = (1, 1, 0)
        self.dots_cords['D'] = (0, 1, 0)

        self.reformat_cords()


class Prism(Figure):
    def __init__(self, canvas, size=100, x_move=20, y_move=200, angle=45):
        super().__init__(canvas, x_move=x_move, y_move=y_move, angle=angle, size=size)

        self.dots_cords['A'] = (0.5, 0, 0)
        self.dots_cords['B'] = (1.5, 0, 0)
        self.dots_cords['C'] = (2, 0.87, 0)
        self.dots_cords['D'] = (1.5, 1.74, 0)
        self.dots_cords['E'] = (0.5, 1.74, 0)
        self.dots_cords['F'] = (0, 0.87, 0)
        self.dots_cords['a'] = (0.5, 0, 1)
        self.dots_cords['b'] = (1.5, 0, 1)
        self.dots_cords['c'] = (2, 0.87, 1)
        self.dots_cords['d'] = (1.5, 1.74, 1)
        self.dots_cords['e'] = (0.5, 1.74, 1)
        self.dots_cords['f'] = (0, 0.87, 1)

        self.sections.append(('AB', True))
        self.sections.append(('Aa', True))
        self.sections.append(('AF', True))
        self.sections.append(('Bb', True))
        self.sections.append(('BC', True))
        self.sections.append(('Cc', False))
        self.sections.append(('CD', False))
        self.sections.append(('Dd', False))
        self.sections.append(('DE', False))
        self.sections.append(('Ee', False))
        self.sections.append(('EF', False))
        self.sections.append(('Ff', False))
        self.sections.append(('ab', False))
        self.sections.append(('bc', False))
        self.sections.append(('cd', False))
        self.sections.append(('de', False))
        self.sections.append(('ef', False))
        self.sections.append(('af', False))

        self.reformat_cords()


class Tetrahedron(Figure):
    def __init__(self, canvas, size=100, x_move=20, y_move=200, angle=45):
        super().__init__(canvas, x_move=x_move, y_move=y_move, angle=angle, size=size)
        self.sections.append(('AB', False))
        self.sections.append(('BC', False))
        self.sections.append(('CA', True))
        self.sections.append(('AS', False))
        self.sections.append(('BS', False))
        self.sections.append(('CS', False))

        self.dots_cords['A'] = (0, 0, 0)
        self.dots_cords['B'] = (0, 1, 0)
        self.dots_cords['C'] = (0.86, 0.86, 0)
        self.dots_cords['S'] = (0.43, 0.43, 0.86)

        self.reformat_cords()


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
