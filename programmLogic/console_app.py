from math import atan2, degrees, cos, sin, radians
from PIL import Image, ImageDraw, ImageFont
from random import choice, randint


class Plain:
    def __init__(self, m0, m1, m2):
        a = [[m1[0] - m0[0], m2[0] - m0[0]], [m1[1] - m0[1], m2[1] - m0[1]], [m1[2] - m0[2], m2[2] - m0[2]]]
        alpha = a[1][0] * a[2][1] - a[2][0] * a[1][1]
        beta = a[0][0] * a[2][1] - a[2][0] * a[0][1]
        gamma = a[0][0] * a[1][1] - a[1][0] * a[0][1]
        self.coeffs = [alpha, -1 * beta, gamma, -1 * (alpha * m0[0] - beta * m0[1] + gamma * m0[2])]

    def dot_on_plain(self, cord):
        return sum([cord[i] * self.coeffs[i] for i in range(3)]) + self.coeffs[3] == 0


class Straight:
    def __init__(self, m0, m1):
        self.m0 = m0
        self.m1 = m1
        self.m = m1[0] - m0[0]
        self.n = m1[1] - m0[1]
        self.p = m1[2] - m0[2]
        self.x = lambda t: self.m * t + m0[0]
        self.y = lambda t: self.n * t + m0[1]
        self.z = lambda t: self.p * t + m0[2]

    def plain_straight_crossing(self, plain):
        a, b, c, d = plain.coeffs
        try:
            t0 = -1 * (a * self.m0[0] + b * self.m0[1] + c * self.m0[2] + d) / (a * self.m + b * self.n + c * self.p)
            return self.x(t0), self.y(t0), self.z(t0)
        except ZeroDivisionError:
            return None

    def whether_dot_on_section(self, dot):
        dx = self.m1[0] - self.m0[0]
        dy = self.m1[1] - self.m0[1]
        dz = self.m1[2] - self.m0[2]

        m = dot[0] - self.m0[0]
        n = dot[1] - self.m0[1]
        p = dot[2] - self.m0[2]

        try:
            m_bool = self.m / m
        except ZeroDivisionError:
            m_bool = self.m == m

        try:
            n_bool = self.n / n
        except ZeroDivisionError:
            n_bool = self.n == n

        try:
            p_bool = self.p / p
        except ZeroDivisionError:
            p_bool = self.p == p

        if not all(filter(lambda x: type(x) is bool, [m_bool, n_bool, p_bool])):
            return False

        ints_coeffs = list(filter(lambda x: type(x) is not bool, [m_bool, n_bool, p_bool]))

        if all([ints_coeffs[0] == el for el in ints_coeffs]):
            max_delta = max([abs(dx), abs(dy), abs(dz)])
            if max_delta == abs(dx):
                xs = sorted([self.m0[0], self.m1[0]])
                return xs[0] <= dot[0] <= xs[1]
            elif max_delta == abs(dy):
                ys = sorted([self.m0[1], self.m1[1]])
                return ys[0] <= dot[1] <= ys[1]
            else:
                zs = sorted([self.m0[2], self.m1[2]])
                return zs[0] <= dot[2] <= zs[1]

        else:
            return False


def rearrange_dots(dots):
    center = [sum([el[0] for el in dots]), sum([el[1] for el in dots])]
    center[0] = center[0] / len(dots)
    center[1] = center[1] / len(dots)
    ans = sorted(dots, key=lambda x: atan2(x[0] - center[0], x[1] - center[1]))
    return ans


greek_letters = ['α', 'β', 'γ', 'δ', 'ε', 'θ', 'λ', 'μ', 'o']


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
            if cross_dot is not None and str1.whether_dot_on_section(
                    cross_dot) and cross_dot not in self.added_dots.values():
                self.additional_dots.append(cross_dot)
                self.add_dot(cross_dot)

    def render(self, file_path='image.jpg'):
        new_image = Image.new("RGB", (350, 350), (255, 255, 255))
        canvas = ImageDraw.Draw(new_image)
        if self.secant_plain is not None:
            points_2d = [self.get_point_cords(point) for point in self.added_dots]
            points_2d = rearrange_dots(points_2d)
            points_2d = tuple(map(tuple, points_2d))
            canvas.polygon(points_2d, fill='orange', outline='black')

        for line in self.sections:
            d1, d2 = self.get_cords_of_section(line[0])
            coordinates = (d1[0], d1[1], d2[0], d2[1])
            if not line[1]:
                canvas.line(coordinates, width=5, fill='black')
            else:
                canvas.line(coordinates, width=1, fill='black')

        size = 8
        for dot in self.added_dots:
            cord = self.get_point_cords(dot)
            x1, y1 = map(int, [(cord[0] - size), (cord[1] - size)])
            x2, y2 = map(int, [(cord[0] + size), (cord[1] + size)])
            canvas.ellipse([x1, y1, x2, y2], fill='green')

        for additional_point in self.additional_dots:
            cord = self.point_cords(additional_point)
            x1, y1 = map(int, [(cord[0] - size), (cord[1] - size)])
            x2, y2 = map(int, [(cord[0] + size), (cord[1] + size)])
            canvas.ellipse([x1, y1, x2, y2], fill='blue')
        new_image.save(file_path)

    def get_point_cords(self, point):
        if point in greek_letters:
            d1 = list(self.added_dots[point])
        else:
            d1 = list(self.dots_cords[point])
        projecting_angle = radians(self.projecting_angle)
        return [d1[0] + 0.5 * d1[1] * cos(projecting_angle) + self.x_move,
                -1 * d1[2] + 0.5 * d1[1] * sin(projecting_angle) + self.y_move]

    def point_cords(self, cords):
        d1 = cords[:]
        projecting_angle = radians(self.projecting_angle)
        return [d1[0] + 0.5 * d1[1] * cos(projecting_angle) + self.x_move,
                -1 * d1[2] + 0.5 * d1[1] * sin(projecting_angle) + self.y_move]

    def reformat_cords(self):
        for key in self.dots_cords:
            cords = self.dots_cords[key]
            self.dots_cords[key] = (cords[0] * self.size, cords[1] * self.size, cords[2] * self.size)

    def get_secant_plain(self):
        if len(self.added_dots) != 3:
            print(f'<Error> wrong number of dots: {len(self.added_dots)}')
            print(self.added_dots)
            return None
        else:
            dots = [self.added_dots[key] for key in self.added_dots]
            self.secant_plain = Plain(*dots)
            return 1

    def set_angle(self, angle):
        self.projecting_angle = angle

    def clear_dots(self):
        self.added_dots = {}
        self.secant_plain = None
        self.plain_crossing_points = []
        self.additional_dots = []

    def create_3_dots(self):
        allowed_sections = [el[0] for el in self.sections]
        for _ in range(3):
            section = choice(allowed_sections)
            proportion = randint(4, 7) / 10
            self.add_dot_on_section(section, proportion)
            allowed_sections.remove(section)

    def shoelace_formula(self):
        vertices = rearrange_dots(list(map(lambda z: list(map(int, self.get_point_cords(z))), self.added_dots)))
        numberOfVertices = len(vertices)
        sum1 = 0
        sum2 = 0

        for i in range(0, numberOfVertices - 1):
            sum1 = sum1 + vertices[i][0] * vertices[i + 1][1]
            sum2 = sum2 + vertices[i][1] * vertices[i + 1][0]

        # Add xn.y1
        sum1 = sum1 + vertices[numberOfVertices - 1][0] * vertices[0][1]
        # Add x1.yn
        sum2 = sum2 + vertices[0][0] * vertices[numberOfVertices - 1][1]

        area = abs(sum1 - sum2) / 2
        return area


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


pyramid = Pyramid(None, size=200, x_move=40)
cube = Cube(None, size=200, x_move=40, y_move=240)
prism = Prism(None, size=140, x_move=0, y_move=180)
tetrahedron = Tetrahedron(None, size=200, x_move=70, y_move=210)
figures = {'Cube': cube, 'Pyramid': pyramid, 'Prism': prism, 'Tetrahedron': tetrahedron}

import argparse
import shutil
import os

parser = argparse.ArgumentParser()
parser.add_argument('--images_amount', type=int, default=26, help='Amount of images to generate')
parser.add_argument('--angle', type=int, default=30, help='projecting angle of figures')
parser.add_argument('--figure', choices=['Cube', 'Pyramid', 'Prism', 'Tetrahedron', 'random'],
                    help='Which figure to choose', default='random')
args = parser.parse_args()

if 'sections_res' in os.listdir('.'):
    shutil.rmtree('sections_res')

os.mkdir('sections_res')
os.mkdir('sections_res/teacher')
os.mkdir('sections_res/students')


for i in range(args.images_amount):
    if args.figure == 'random':
        figure = choice(list(figures.values()))
    else:
        figure = figures[args.figure]
    figure.set_angle(args.angle)
    figure.create_3_dots()
    figure.cross_figure_with_plain()
    while figure.shoelace_formula() < 10000:
        figure.clear_dots()
        figure.create_3_dots()
        figure.cross_figure_with_plain()

    figure.render(file_path=f'sections_res/teacher/{i}.jpg')
    area = figure.shoelace_formula()

    new_dict = dict()
    for dot in figure.added_dots:
        if not figure.added_dots[dot] in figure.additional_dots:
            new_dict[dot] = figure.added_dots[dot]
    figure.added_dots = new_dict.copy()
    figure.additional_dots.clear()
    figure.secant_plain = None
    figure.render(file_path=f'sections_res/students/{i}.jpg')
    figure.clear_dots()
    print(f'Created {i}th figure: {figure.__class__.__name__}, area of section: {area}')
