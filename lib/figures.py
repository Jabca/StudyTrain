from lib.core_classes  import Figure

class Pyramid(Figure):
    def __init__(self, canvas, size=100, x_offset=20, y_offset=200, angle=45):
        super().__init__(canvas, x_offset=x_offset, y_offset=y_offset, angle=angle, size=size)

        self.sections.append(('AB', True))
        self.sections.append(('AD', False))
        self.sections.append(('AS', False))
        self.sections.append(('BC', True))
        self.sections.append(('BS', True))
        self.sections.append(('CD', False))
        self.sections.append(('CS', False))
        self.sections.append(('DS', False))

        self.verges['S'] = (0.5, 0.5, 1)
        self.verges['A'] = (0, 0, 0)
        self.verges['B'] = (1, 0, 0)
        self.verges['C'] = (1, 1, 0)
        self.verges['D'] = (0, 1, 0)

        self.reformat_cords()


class Prism(Figure):
    def __init__(self, canvas, size=100, x_offset=20, y_offset=200, angle=45):
        super().__init__(canvas, x_offset=x_offset, y_offset=y_offset, angle=angle, size=size)

        self.verges['A'] = (0.5, 0, 0)
        self.verges['B'] = (1.5, 0, 0)
        self.verges['C'] = (2, 0.87, 0)
        self.verges['D'] = (1.5, 1.74, 0)
        self.verges['E'] = (0.5, 1.74, 0)
        self.verges['F'] = (0, 0.87, 0)
        self.verges['a'] = (0.5, 0, 1)
        self.verges['b'] = (1.5, 0, 1)
        self.verges['c'] = (2, 0.87, 1)
        self.verges['d'] = (1.5, 1.74, 1)
        self.verges['e'] = (0.5, 1.74, 1)
        self.verges['f'] = (0, 0.87, 1)

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
    def __init__(self, canvas, size=100, x_offset=20, y_offset=200, angle=45):
        super().__init__(canvas, x_offset=x_offset, y_offset=y_offset, angle=angle, size=size)
        self.sections.append(('AB', False))
        self.sections.append(('BC', False))
        self.sections.append(('CA', True))
        self.sections.append(('AS', False))
        self.sections.append(('BS', False))
        self.sections.append(('CS', False))

        self.verges['A'] = (0, 0, 0)
        self.verges['B'] = (0, 1, 0)
        self.verges['C'] = (0.86, 0.86, 0)
        self.verges['S'] = (0.43, 0.43, 0.86)

        self.reformat_cords()


class Cube(Figure):
    def __init__(self, canvas, size=100, x_offset=20, y_offset=200, angle=45):
        super().__init__(canvas, x_offset=x_offset, y_offset=y_offset, angle=angle, size=size)
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

        self.verges['A'] = (0, 0, 0)
        self.verges['B'] = (1, 0, 0)
        self.verges['C'] = (1, 1, 0)
        self.verges['D'] = (0, 1, 0)
        self.verges['a'] = (0, 0, 1)
        self.verges['b'] = (1, 0, 1)
        self.verges['c'] = (1, 1, 1)
        self.verges['d'] = (0, 1, 1)

        self.reformat_cords()