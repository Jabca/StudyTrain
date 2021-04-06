from Basic_math import Plain, Straight

plain1 = Plain((0, 0, 0), (0, 0, 0), (0, 0, 0))
str1 = Straight((1, 0, 1), (2, 0, 1))
print(str1.plain_straight_crossing(plain1))
