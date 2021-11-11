import os
import shutil
import argparse

from random import choice, randint
from PIL import Image, ImageDraw, ImageFont
from math import atan2, degrees, cos, sin, radians

from programmLogic.core_classes import Figure
from programmLogic.Basic_math import Plain, Straight
from programmLogic.Figures import Cube, Prism, Pyramid, Tetrahedron


pyramid = Pyramid(None, size=200, x_move=40)
cube = Cube(None, size=200, x_move=40, y_move=240)
prism = Prism(None, size=140, x_move=0, y_move=180)
tetrahedron = Tetrahedron(None, size=200, x_move=70, y_move=210)
figures = {'Cube': cube, 'Pyramid': pyramid, 'Prism': prism, 'Tetrahedron': tetrahedron}



parser = argparse.ArgumentParser()
parser.add_argument('--images_amount', type=int, default=26, help='Amount of images to generate')
parser.add_argument('--angle', type=int, default=30, help='projecting angle of figures')
parser.add_argument('--figure', choices=['Cube', 'Pyramid', 'Prism', 'Tetrahedron', 'random'],
                    help='Which figure to choose', default='random')
args = parser.parse_args()

if 'sections_res' in os.listdir('..'):
    shutil.rmtree('../sections_res')

os.mkdir('../sections_res')
os.mkdir('../sections_res/teacher')
os.mkdir('../sections_res/students')


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
