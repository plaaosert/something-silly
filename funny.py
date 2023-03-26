import math
import time
import os
import platform
import random
import sys

if "android" not in platform.platform().lower():
    from PIL import Image
else:
    print("\n" * 100)

os.system("")


class EquSet:
    def __init__(self, rop, gop, bop):
        self.r = EquTree(rop)
        self.g = EquTree(gop)
        self.b = EquTree(bop)

    def calc(self, sx, sy, t):
        return [
            [
                (
                    self.r.evaluate(float(x) / float(sx), float(y) / float(sy), t),
                    self.g.evaluate(float(x) / float(sx), float(y) / float(sy), t),
                    self.b.evaluate(float(x) / float(sx), float(y) / float(sy), t)
                ) for x in range(sx)
            ] for y in range(sy)
        ]


class EquTree:
    PLUS = lambda a, b: a + b if b else a
    MINUS = lambda a, b: a - b if b else a
    MULT = lambda a, b: a * b if b else a
    DIV = lambda a, b: a / b if b else a
    POW = lambda a, b: a ** b if b else a

    SIN = lambda a, b: math.sin(a)
    COS = lambda a, b: math.cos(a)
    TAN = lambda a, b: math.tan(a)

    def __init__(self, operation):
        self.operation = operation
        self.left = None
        self.right = None

    def add(self, obj, side):
        if side == 0:
            self.left = obj
        else:
            self.right = obj

    def evaluate(self, x, y, t):
        left_val = None
        right_val = None

        # print(self.left, self.right)
        if self.left:
            left_val = self.left.evaluate(x, y, t)

        if self.right:
            right_val = self.right.evaluate(x, y, t)

        if left_val and right_val:
            return self.operation(left_val, right_val)
        elif left_val:
            return self.operation(left_val, None)
        elif right_val:
            return self.operation(right_val, None)
        else:
            return 0


class Equ:
    @staticmethod
    def ayt(fn):
        return Equ(lambda x, y, t: fn(x))

    @staticmethod
    def xat(fn):
        return Equ(lambda x, y, t: fn(y))

    @staticmethod
    def xya(fn):
        return Equ(lambda x, y, t: fn(t))

    @staticmethod
    def f_constant(v):
        return Equ(lambda x, y, t: v)

    @staticmethod
    def f_sint(mul):
        return Equ(lambda x, y, t: math.sin(t) * mul)

    def __init__(self, fn):
        self.fn = fn

    def evaluate(self, x, y, t):
        return self.fn(x, y, t)


st = EquSet(EquTree.PLUS, EquTree.PLUS, EquTree.PLUS)
st.r.add(EquTree(EquTree.SIN), 0)
st.r.left.add(EquTree(EquTree.PLUS), 0)
st.r.left.left.add(Equ.f_sint(1), 0)
st.r.left.left.add(Equ(lambda x, y, t: x + y), 1)

dst = lambda a, b: math.sqrt(
    (abs(b[0] - a[0]) ** 2) + (abs(b[1] - a[1]) ** 2)
)

p1 = (-1.0, 0.2)
p2 = (2.0, 0.5)


def lindist(a, b):
    # ignores arg a
    x_diff = p2[0] - p1[0]
    y_diff = p2[1] - p1[1]
    num = abs(y_diff * b[0] - x_diff * b[1] + p2[0] * p1[1] - p2[1] * p1[0])
    den = math.sqrt(y_diff ** 2 + x_diff ** 2)
    return num / den


def dist(a, b):
    # print(a, b, round(dst(a,b),4))
    # time.sleep(0.5)
    return dst(a, b)


p = (0.44, 0.77)
st.g.add(
    Equ(lambda x, y, t: max(0.0, -0.1 + min(1.1, 1.12 - lindist(p, (x, y)))) ** 50), 0)

st.b.add(Equ(lambda x, y, t: (random.random() - 0.5) * 100), 1)
st.b.add(EquTree(EquTree.SIN), 0)
st.b.left.add(EquTree(EquTree.MULT), 0)
st.b.left.left.add(Equ.f_sint(3), 0)
st.b.left.left.add(Equ(lambda x, y, t: x * y), 1)

num = 250

if not "android" in platform.platform().lower():
    siz = 250
else:
    siz = 20

for i in range(num):
    t = float(i) / float(num)

    result = st.calc(siz, siz, t)

    if "android" not in platform.platform().lower():
        img = Image.new("RGB", (siz, siz), color=(0, 0, 0))
        for x in range(siz):
            for y in range(siz):
                col = list(result[x][y])
                for c in range(3):
                    col[c] = max(0, min(255, int((max(0, min(1, col[c])) + 1) * 128)))

                img.putpixel((x, y), tuple(col))

        img.save("out/img_{:03}.png".format(i))

        print("frame {:4} done".format(i))

    else:
        print("\033[1;1H\n", end="")
        print("\x1b[38;2;20;255;20mTRUECOLOR\x1b[0m\n")
        txt = ""
        for y in range(siz):
            for x in range(siz):
                col = list(result[x][y])
                for c in range(3):
                    col[c] = max(0, min(255, int((max(0, min(1, col[c])) + 1) * 128)))

                txt += "\x1b[38;2;{};{};{}m##".format(*col)
            txt += "\n"

        print(txt)
