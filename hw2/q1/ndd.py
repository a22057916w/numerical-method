from sympy import *
import pandas as pd
import numpy as np
import math
import os
import re

def dividedDiffTable(x, y, tlen):
    row = col = tlen

    # initialize the table
    DD = [ [ 0 for i in range(col) ] for j in range(row) ]
    for i in range(row):
        DD[i][0] = y[i]

    # calculate the differences
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
            name += ", ...,x" + str(i) + "]"
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

    print("The function between [" + str(a) + ", " + str(b) + "] is:")
    plot(f,(x ,a, b))   # using sympy's plot function

if __name__ == "__main__":

    # read testcase from file
    fp = open("testcase.txt", "r")     # test using cmd
    #fp = open("hw2/q1/testcase.txt", "r")   # test using Atom(IDE)
    n = int(fp.readline().replace("\n", ""))  # first line which indicates the case numbers

    for i in range(n):
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

        # getting DD data
        DD = dividedDiffTable(x, y, len(x))   # return a two dim list
        DDtable = getTable(DD)    # return a DataFrame
        px = poly(DD)   # return a string

        # print out the results
        print("Test case " + str(i + 1) + ":")
        print("The Newton's divided-differences table is :\n", DDtable, "\n")
        print("The polynomial is:\n", px, "\n")
        sympy_plot(px, intervals)

    os.system("pause")
