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

        if round(self.m / m, 1) == round(self.n / n, 1) == round(self.p / p, 1):
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
            print('<Error> dot not on straight')
