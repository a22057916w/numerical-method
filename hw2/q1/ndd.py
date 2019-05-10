from sympy import *
import pandas as pd
import numpy
import math
import os

def dividedDiffTable(x, y, tlen):
    row = tlen
    col = tlen + 1
    # initialize the table
    DD = [ [ 0 for i in range(col) ] for j in range(row) ]
    for i in range(row):
        DD[i][0] = y[i]

    # calculate the difference
    for i in range(1, col):
        for j in range(row - i):
            DD[j][i] = (DD[j + 1][i - 1] - DD[j][i - 1]) / (x[j + i] - x[j])
    return DD

if __name__ == "__main__":
    x = [5, 6, 9, 11]
    y = [12, 13, 14, 16]
    DD = dividedDiffTable(x, y, len(x))
    print(DD)
