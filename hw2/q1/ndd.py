from sympy import *
#import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import os

def dividedDiffTable(x, y, tlen):
    row = col = tlen

    # initialize the table
    DD = [ [ 0 for i in range(col) ] for j in range(row) ]
    for i in range(row):
        DD[i][0] = y[i]

    # calculate the difference
    for i in range(1, col):
        for j in range(row - i):
            DD[j][i] = (DD[j + 1][i - 1] - DD[j][i - 1]) / (x[j + i] - x[j])

    return DD

def getTable(DD):
    col = len(DD) + 1

    # initialize the name of the columns of DD table
    col_names = []
    for i in range(col):
        if i == 0:
            continue
        if i < 5:
            name = "f["
            for j in range(i):
                if j > 0:
                    name += ", "
                name += "x" + str(j)
            name += "]"
        else:
            name = "f["
            for j in range(3):
                if j > 0:
                    name += ", "
                name += "x" + str(j)
            name += "...x" + str(i) + "]"
        col_names.append(name)

    df = pd.DataFrame(DD)
    df.columns = col_names  # assign column names to df

    return df

def poly(DD):
    px = ""
    for i in range(len(DD)):
        if i == 0:
            px += str(DD[0][0])
        else:
            px += " + (x - " + str(x[i - 1]) + ")*(" + str(DD[0][i])
    for i in range(len(DD) - 1):
        px += ")"
    return px

def sympy_plot(px, interval):

    a, b = interval
    f = sympify(px)
    x = symbols("x")
    plot(f,(x ,a, b))   # using sympy's plot function

if __name__ == "__main__":
    fp = open("testcase", "r")
    line = fp.readline()
    print(line)

    x = [5, 6, 9, 11]
    y = [12, 13, 14, 16]
    intervals = [(0.9, 13.3)]

    # getting DD data
    DD = dividedDiffTable(x, y, len(x))   # return a two dim list
    DDtable = getTable(DD)    # return a DataFrame
    px = poly(DD)   # return a string

    # print out the results
    print("The Newton's divided-differences table is :\n", DDtable, "\n")
    print("The polynomial is:\n", px, "\n")
    sympy_plot(px, intervals[0])
