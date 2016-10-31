from FGAme import *
from copy import copy

NUMBERS = []
# 0
num = []
num.append(draw.Segment(Vec(0, 30.0), Vec(20.0, 30.0)))
num.append(draw.Segment(Vec(2, 0), Vec(2, 30)))
num.append(draw.Segment(Vec(0.0, 0.0), Vec(20.0, 0.0)))
num.append(draw.Segment((20, 0), (20, 30)))

NUMBERS.append(num)
# 1
num = []
num.append(draw.Segment((20, 0), (20, 30)))

NUMBERS.append(num)
# 2
num = []
num.append(draw.Segment(Vec(0, 30.0), Vec(20.0, 30.0)))
num.append(draw.Segment(Vec(0.0, 0.0), Vec(20.0, 0.0)))
num.append(draw.Segment(Vec(2.0, 0.0), Vec(2.0, 15.0)))
num.append(draw.Segment(Vec(18.0, 30.0), Vec(18.0, 15.0)))
num.append(draw.Segment(Vec(0.0, 15.0), Vec(20.0, 15.0)))

NUMBERS.append(num)
# 3
num = []
num.append(draw.Segment(Vec(20.0, 0.0), Vec(20.0, 30.0)))
num.append(draw.Segment(Vec(2.0, 2.0), Vec(22.0, 2.0)))
num.append(draw.Segment(Vec(2.0, 30.0), Vec(22.0, 30.0)))
num.append(draw.Segment(Vec(2.0, 15.0), Vec(22.0, 15.0)))

NUMBERS.append(num)

# 4
num = []
num.append(draw.Segment(Vec(20, 0), Vec(20, 30)))
num.append(draw.Segment(Vec(0, 15), Vec(20, 15)))
num.append(draw.Segment(Vec(2, 15), Vec(2, 30)))

NUMBERS.append(num)
# 5
num = []
num.append(draw.Segment(Vec(0, 30.0), Vec(20.0, 30.0)))
num.append(draw.Segment(Vec(0.0, 0.0), Vec(20.0, 0.0)))
num.append(draw.Segment(Vec(18.0, 0.0), Vec(18.0, 15.0)))
num.append(draw.Segment(Vec(2.0, 30.0), Vec(2.0, 15.0)))
num.append(draw.Segment(Vec(0.0, 15.0), Vec(20.0, 15.0)))

NUMBERS.append(num)
# 6
num = []
num.append(draw.Segment(Vec(0, 30.0), Vec(20.0, 30.0)))
num.append(draw.Segment(Vec(0.0, 0.0), Vec(20.0, 0.0)))
num.append(draw.Segment(Vec(2, 0), Vec(2, 30)))
num.append(draw.Segment(Vec(18.0, 0.0), Vec(18.0, 15.0)))
num.append(draw.Segment(Vec(0.0, 15.0), Vec(20.0, 15.0)))

NUMBERS.append(num)
# 7
num = []
num.append(draw.Segment(Vec(0, 30.0), Vec(20.0, 30.0)))
num.append(draw.Segment((20, 0), (20, 30)))

NUMBERS.append(num)
# 8
num = []
num.append(draw.Segment(Vec(0, 30.0), Vec(20.0, 30.0)))
num.append(draw.Segment(Vec(2, 0), Vec(2, 30)))
num.append(draw.Segment(Vec(0.0, 0.0), Vec(20.0, 0.0)))
num.append(draw.Segment(Vec(0.0, 15.0), Vec(20.0, 15.0)))
num.append(draw.Segment((20, 0), (20, 30)))

NUMBERS.append(num)
# 9
num = []
num.append(draw.Segment(Vec(0, 30.0), Vec(20.0, 30.0)))
num.append(draw.Segment(Vec(2.0, 30.0), Vec(2.0, 15.0)))
num.append(draw.Segment(Vec(0.0, 15.0), Vec(20.0, 15.0)))
num.append(draw.Segment((20, 0), (20, 30)))

NUMBERS.append(num)


for num in NUMBERS:
    for n in num:
        n.linewidth = 5

def offset(ofs):
    for num in NUMBERS:
        for n in num:
            n.pos += ofs

# def number_init(size):
#     for i in range(0, size):
#         for j in range(0, 10):
#             print_num()


def print_num(num, offset):
    copied = []
    for n in NUMBERS[num]:
        cop = draw.Segment(n.start+offset, n.end+offset)
        cop.linewidth = 5
        copied.append(cop)
        world.add(cop)
    return copied

def remove_num(num):
    while len(num) > 0:
        num.pop().visible = False