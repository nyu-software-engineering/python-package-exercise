import random

RED = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
BLACK = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}
EVEN = set(range(2, 37, 2))
ODD = set(range(1, 37, 2))
LOW = set(range(1, 19))
HIGH = set(range(19, 37))

FIRST_DOZEN = set(range(1, 13))
SECOND_DOZEN = set(range(13, 25))
THIRD_DOZEN = set(range(25, 37))

FIRST_COLUMN = set(range(1, 37, 3))
SECOND_COLUMN = set(range(2, 37, 3))
THIRD_COLUMN = set(range(3, 37, 3))

STRAIGHTS = {}
for pocket in range(37):
    STRAIGHTS[pocket] = {pocket}

