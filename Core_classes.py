from math import cos, sin, radians
from Basic_math import Plain, Straight, rearrange_dots
from tkinter import *

greek_letters = ['α', 'β', 'γ', 'δ', 'ε', 'θ', 'π',  'ψ', 'ω', 'Π', 'Σ', 'Ψ', 'Δ']


class Figure:
    def __init__(self, parent, x_move, y_move, angle, size):
        self.sections = []
        self.dots_cords = {}
        self.x_move = x_move
        self.y_move = y_move
        self.parent = parent
        self.added_dots = {}
        self.projecting_angle = angle
        self.size = size
        self.secant_plain = None
        self.plain_crossing_points = []
        self.additional_dots = []

    def add_dot_on_section(self, section, prop):
        d1, d2 = self.dots_cords[section[0]], self.dots_cords[section[1]]
        delta_x = d2[0] - d1[0]
        delta_y = d2[1] - d1[1]
        delta_z = d2[2] - d1[2]
        x = d1[0] + delta_x * prop
        y = d1[1] + delta_y * prop
        z = d1[2] + delta_z * prop
        self.added_dots[greek_letters[len(list(self.added_dots.keys()))]] = (x, y, z)

    def add_dot(self, cord):
        x, y, z = cord
        self.added_dots[greek_letters[len(list(self.added_dots.keys()))]] = (x, y, z)

    def get_cords_of_section(self, string):

        string = sorted(list(string))
        d1 = self.get_point_cords(string[0])
        d2 = self.get_point_cords(string[1])

        return d1, d2

    def cross_figure_with_plain(self):
        if self.get_secant_plain() is None:
            return None
        for section in self.sections:
            d1, d2 = self.dots_cords[section[0][0]], self.dots_cords[section[0][1]]
            str1 = Straight(d1, d2)
            cross_dot = str1.plain_straight_crossing(self.secant_plain)
            if cross_dot is not None and str1.whether_dot_on_section(cross_dot) and cross_dot not in self.added_dots.values():
                self.additional_dots.append(cross_dot)
                self.add_dot(cross_dot)

    def render(self):
        canvas = self.parent.root_canvas
        if self.secant_plain is not None:
            points_2d = [self.get_point_cords(point) for point in self.added_dots]
            points_2d = rearrange_dots(points_2d)
            canvas.create_polygon(*points_2d, fill='orange', outline='black')

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
            x1, y1 = map(int, [(cord[0] - size), (cord[1] - size)])
            x2, y2 = map(int, [(cord[0] + size), (cord[1] + size)])
            canvas.create_oval(x1, y1, x2, y2, fill='green')

        for verge in self.dots_cords.keys():
            x, y = self.get_point_cords(verge)[0] - 14, self.get_point_cords(verge)[1] - 14
            canvas.create_text(x, y,
                               text=verge,
                               justify=CENTER, font=("Verdana", 15), fill='blue')

        for additional_point in self.additional_dots:
            cord = self.point_cords(additional_point)
            x1, y1 = map(int, [(cord[0] - size), (cord[1] - size)])
            x2, y2 = map(int, [(cord[0] + size), (cord[1] + size)])
            canvas.create_oval(x1, y1, x2, y2, fill='blue')

    def get_point_cords(self, point):
        if point in greek_letters:
            d1 = list(self.added_dots[point])
        else:
            d1 = list(self.dots_cords[point])
        projecting_angle = radians(self.projecting_angle)
        return [d1[0] + 0.5 * d1[1] * cos(projecting_angle) + self.x_move, -1 * d1[2] + 0.5 * d1[1] * sin(projecting_angle) + self.y_move]

    def point_cords(self, cords):
        d1 = cords[:]
        projecting_angle = radians(self.projecting_angle)
        return [d1[0] + 0.5 * d1[1] * cos(projecting_angle) + self.x_move, -1 * d1[2] + 0.5 * d1[1] * sin(projecting_angle) + self.y_move]

    def reformat_cords(self):
        for key in self.dots_cords:
            cords = self.dots_cords[key]
            self.dots_cords[key] = (cords[0] * self.size, cords[1] * self.size, cords[2] * self.size)

    def get_secant_plain(self):
        if len(self.added_dots) != 3:
            print(f'<Error> wrong number of dots: {len(self.added_dots)}')
            return None
        else:
            dots = [self.added_dots[key] for key in self.added_dots]
            self.secant_plain = Plain(*dots)
            return 1

    def set_angle(self, angle):
        self.projecting_angle = angle
        self.parent.render_window()
