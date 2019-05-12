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

def Horner(DD, x, value):
    y = DD[0][len(DD) - 1]
    for i in range(len(DD) - 1, -1, -1):
        y = (value - x[i]) * y + DD[0][i]
    return y

if __name__ == "__main__":

    # read testcase from file
    #fp = open("testcase.txt", "r")     # test using cmd
    fp = open("hw2/q2/testcase.txt", "r")   # test using Atom(IDE)
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

        print("Test case " + str(i + 1) + ":")
        value = eval(input("Please enter a number to evaluate:"))   # user input
        print("The value at " + str(value) + " is:\n", Horner(DD, x, value))    # print out the results

    os.system("pause")
