from basic_math import Plain, Straight

plain = Plain((0, 0, 10), (1, 1, 10), (0, 1, 10))
str1 = Straight((0, 2, 0), (0, 2, 2))
print(str1.whether_dot_on_section((0, 2, 1)))
