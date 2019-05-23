from sympy import *
import pandas as pd
import numpy as np
import math
import os
import re

def getSx(x, y):
    n = len(x)

    s = [""] * (n - 1)      # (points - 1) curves
    c = [ [ 0 for i in range(n) ] for j in range(4) ]     # c stands for coefficient
    c[0], c[1], c[2], c[3] = find_all_coef(x, y)

    # covert int list into string list
    for i in range(len(c)):
        c[i] = list(map(str, c[i]))
    x = list(map(str, x))

    for i in range(n - 1):      # get a list of S(X) in string type
        s[i] = c[0][i] + "+" + c[1][i] + "*(x-" + x[i] + ")+" + c[2][i] + "*(x-" + x[i] + ")**2+" + c[3][i] + "*(x-" + x[i] +")**3"
        print(s[i])
    return s

def find_all_coef(x, y):
    n = len(x)
    a, b, d = ([ 0 for i in range(n) ] for i in range(3))
    for i in range(n):      # get all the coefficient of a
        a[i] = y[i]

    c, h = getCsHs(x, a)     # get all the coefficients of c and h

    for i in range(n - 1):
        b[i] = ((a[i + 1] - a[i]) / h[i]) - (h[i] * (2 * c[i] + c[i + 1]) / 3)
    for i in range(n - 1):
        d[i] = (c[i + 1] - c[i]) / (3 * h[i])

    return a, b, c, d

def getCsHs(x, a):
    n = len(x)
    h = [0] * (n - 1)
    c = [0] * n

    for i in range(len(h)):       # calculate all the h
        h[i] = x[i + 1] - x[i]

    s, r, t, e = ([ 0 for i in range(n - 1) ] for i in range(4))

    # s[0] = c[0] = e[0] = 0, s[n - 1] = c[n -1] = e[n - 1] = 0
    for i in range(1, n - 1):   # initialize s, r, and t
        s[i] = 2 * (h[i - 1] + h[i])
        e[i] = (3 * (a[i + 1] - a[i]) / h[i]) - (3 * (a[i] - a[i - 1]) / h[i - 1])
        t[i] = r[i] = h[i]
    # solving the tridiagonal systems
    for i in range(2, n - 1):
        s[i] = s[i] - (r[i - 1] / s[i - 1]) * t[i - 1]
        e[i] = e[i] - (r[i - 1] / s[i - 1]) * e[i - 1]

    # back subsititution
    c[n - 2] = e[n - 2] / s[n - 2]
    for i in range(n - 3, 0, -1):
        c[i] = (e[i] - t[i] * c[i + 1]) / s[i]

    return c, h

def draw(sx, x):
    n = len(x)
    s = len(sx)
    p = sympy_plot(sx[0], (x[0], x[0 + 1]))
    for i in range(n - 1):
        p.append(sympy_plot(sx[i], (x[i], x[i + 1]))[0])
    p.show()

def sympy_plot(sx, interval):
    a, b = interval
    f = sympify(sx)
    x = symbols("x")

    p = plot(f,(x ,a, b), show = False)   # using sympy's plot function
    return p

if __name__ == "__main__":

    # read testcase from file
    #fp = open("testcase.txt", "r")     # test using cmd
    fp = open("hw3/testcase.txt", "r")   # test using Atom(editor)
    n = int(fp.readline().replace("\n", ""))  # first line which indicates the case numbers

    for i in range(1):
        case = []   # to load the list of figures in a line

        for j in range(3):
            line = fp.readline()
            # parsing data
            new_line = line.replace("\n", "")
            nums = re.split(" |, ", new_line)
            # load the data into case
            case.append(nums)

        # assign testcase to variables
        x = list(map(eval, case[0]))
        y = list(map(eval, case[1]))
        intervals = tuple(map(eval, case[2]))

        splines = [None] * (len(x) - 1)   # (points - 1) curves
        splines = getSx(x, y)
        draw(splines, x)

    os.system("pause")
