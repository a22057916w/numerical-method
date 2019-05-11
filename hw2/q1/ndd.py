from sympy import *
import pandas as pd
import numpy
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

def printTable(DD):
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

    print(df)

if __name__ == "__main__":
    x = [5, 6, 9, 11]
    y = [12, 13, 14, 16]
    intervals = [(0.9, 13.3)]
    DD = dividedDiffTable(x, y, len(x))
    print(DD)
    printTable(DD)
