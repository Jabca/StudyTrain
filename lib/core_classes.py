from math import cos, sin, radians
from random import randint, choice
from tkinter import *

from lib.basic_math import Plain, Straight, rearrange_dots


class Figure:
    def __init__(self, parent, x_offset: int, y_offset: int, angle: int, size: int) -> None:
        self.sections = []
        self.verges = {}
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.parent = parent
        self.added_dots = []
        self.projecting_angle = angle
        self.size = size
        self.secant_plain = None
        self.plain_crossing_points = []
        self.additional_dots = []

    def add_dot_on_section(self, section: str, prop: float) -> None:
        d1, d2 = self.verges[section[0]], self.verges[section[1]]
        delta_x = d2[0] - d1[0]
        delta_y = d2[1] - d1[1]
        delta_z = d2[2] - d1[2]
        x = d1[0] + delta_x * prop
        y = d1[1] + delta_y * prop
        z = d1[2] + delta_z * prop
        self.add_dot((x, y, z))

    def add_dot(self, cord: tuple) -> None:
        self.added_dots.append(cord)

    def get_cords_of_section(self, string):
        p1, p2 = sorted(list(string))
        d1 = self.get_point_cords(p1)
        d2 = self.get_point_cords(p2)

        return d1, d2

    def cross_figure_with_plain(self) -> None:
        if self.get_secant_plain() is None:
            return None

        for section in self.sections:
            d1, d2 = self.verges[section[0][0]], self.verges[section[0][1]]
            str1 = Straight(d1, d2)
            cross_dot = str1.plain_straight_crossing(self.secant_plain)
            if cross_dot is not None and str1.whether_dot_on_section(cross_dot) and cross_dot not in self.added_dots:
                self.additional_dots.append(cross_dot)
                self.add_dot(cross_dot)

    def render(self) -> None:
        canvas = self.parent.root_canvas
        if self.secant_plain is not None:
            points_2d = [self.transform_point_cords(point) for point in self.added_dots]
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
            cord = self.transform_point_cords(dot)
            x1, y1 = map(int, [(cord[0] - size), (cord[1] - size)])
            x2, y2 = map(int, [(cord[0] + size), (cord[1] + size)])
            canvas.create_oval(x1, y1, x2, y2, fill='green')

        for verge in self.verges.keys():
            x, y = self.get_point_cords(verge)[0] - 14, self.get_point_cords(verge)[1] - 14
            canvas.create_text(x, y,
                               text=verge,
                               justify=CENTER, font=("Verdana", 15), fill='blue')

        for additional_point in self.additional_dots:
            cord = self.transform_point_cords(additional_point)
            x1, y1 = map(int, [(cord[0] - size), (cord[1] - size)])
            x2, y2 = map(int, [(cord[0] + size), (cord[1] + size)])
            canvas.create_oval(x1, y1, x2, y2, fill='blue')

    def get_point_cords(self, point: str) -> tuple:
        return self.transform_point_cords(self.verges[point])

    def point_cords(self, cords) -> tuple:
        d1 = cords[:]
        projecting_angle = radians(self.projecting_angle)
        return d1[0] + 0.5 * d1[1] * cos(projecting_angle) + self.x_offset, \
               -1 * d1[2] + 0.5 * d1[1] * sin(projecting_angle) + self.y_offset

    def transform_point_cords(self, point: tuple) -> tuple:
        projecting_angle = radians(self.projecting_angle)
        return point[0] + 0.5 * point[1] * cos(projecting_angle) + self.x_offset, \
               -1 * point[2] + 0.5 * point[1] * sin(projecting_angle) + self.y_offset

    def reformat_cords(self) -> None:
        for key in self.verges:
            cords = self.verges[key]
            self.verges[key] = (cords[0] * self.size, cords[1] * self.size, cords[2] * self.size)

    def get_secant_plain(self):
        if len(self.added_dots) != 3:
            print(f'<Error> wrong number of dots: {len(self.added_dots)}')
            return None
        else:
            self.secant_plain = Plain(*self.added_dots)
            return 1
        
    def set_x_offset(self, offset):
        self.x_offset = offset
        
    def set_y_offset(self, offset):
        self.y_offset = offset

    def set_angle(self, angle: int) -> None:
        self.projecting_angle = angle

    def create_3_dots(self):
        allowed_sections = [el[0] for el in self.sections]
        for i in range(3):
            section = choice(allowed_sections)
            proportion = randint(4, 7) / 10
            self.add_dot_on_section(section, proportion)
            allowed_sections.remove(section)

    def shoelace_formula(self):
        vertices = rearrange_dots(list(map(lambda z: list(map(int, self.transform_point_cords(z))), self.added_dots)))
        number_of_vertices = len(vertices)
        sum1 = 0
        sum2 = 0

        for i in range(0, number_of_vertices - 1):
            sum1 = sum1 + vertices[i][0] * vertices[i + 1][1]
            sum2 = sum2 + vertices[i][1] * vertices[i + 1][0]

        sum1 = sum1 + vertices[number_of_vertices - 1][0] * vertices[0][1]
        sum2 = sum2 + vertices[0][0] * vertices[number_of_vertices - 1][1]

        area = abs(sum1 - sum2) / 2
        return area
