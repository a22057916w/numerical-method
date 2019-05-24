from sympy import *
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import os
import re

def printTable(x, y):
    c = [ [ 0 for i in range(n) ] for j in range(4) ]     # c stands for coefficient
    c[0], c[1], c[2], c[3] = find_all_coef(x, y)        # get as, bs, cs, ds

    dict = {
        "a": c[0],
        "b": c[1],
        "c": c[2],
        "d": c[3]
    }

    df = pd.DataFrame(dict)
    print(df)

def getSx(x, y):
    n = len(x)
    s = [""] * (n - 1)      # (points - 1) curves
    c = [ [ 0 for i in range(n) ] for j in range(4) ]     # c stands for coefficient
    c[0], c[1], c[2], c[3] = find_all_coef(x, y)        # get as, bs, cs, ds

    # covert int list into string list
    for i in range(len(c)):
        c[i] = list(map(str, c[i]))
    x = list(map(str, x))

    for i in range(n - 1):      # get a list of S(X) in string type
        s[i] = c[0][i] + "+" + c[1][i] + "*(x-" + x[i] + ")+" + c[2][i] + "*(x-" + x[i] + ")**2+" + c[3][i] + "*(x-" + x[i] + ")**3"
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

def draw(ogn, sx, x):
    n = len(x)
    p = sympy_plot(sx[0], (x[0], x[0 + 1]), (x[0], x[n - 1]) )      # set first plot
    for i in range(1, len(sx)):
        p.append(sympy_plot(sx[i], (x[i], x[i + 1]), (x[0], x[len(x) - 1]) )[0])

    plt.rcParams["figure.figsize"] = 10, 3          # set figure width and heigh by inches

    print("The figure is:")
    if ogn:         # if exists orignal function, put it into figure
        p1 = sympy_plot(ogn, (x[0], x[n - 1]), (x[0], x[n - 1]))
        p1[0].line_color = "r"
        p1.extend(p)
        p1.show()
    else:
        p.show()

def sympy_plot(fs, interval, xlim):
    a, b = interval     # Xj, Xj+1
    f = sympify(fs)
    x = symbols("x")

    p = plot(f,(x ,a, b), show = False, xlim = [xlim[0] - 1, xlim[1] + 1])   # using sympy's plot function
    return p

if __name__ == "__main__":

    # read testcase from file
    fp = open("testcase.txt", "r")     # test using cmd
    #fp = open("hw3/testcase.txt", "r")   # test using Atom(editor)
    n = int(fp.readline().replace("\n", ""))  # first line which indicates the case numbers

    ogn = ["", "1/(1 + 25*x**2)", "1/(1 + 25*x**2)", "1/(1 + 25*x**2)", "1/(1 + 25*x**2)"]

    for i in range(n):
        case = []   # to load the list of figures in a line

        for j in range(2):
            line = fp.readline()
            # parsing data
            new_line = line.replace("\n", "")
            line = re.split(" |, ", new_line)
            # load the data into case
            case.append(line)

        # assign testcase to variables
        x = list(map(eval, case[0]))
        y = list(map(eval, case[1]))
              # original function
        splines = [None] * (len(x) - 1)   # (points - 1) curves
        splines = getSx(x, y)

        # print results
        print("Case " + str(i + 1) + ":")
        printTable(x, y)
        draw(ogn[i], splines, x)

    os.system("pause")
