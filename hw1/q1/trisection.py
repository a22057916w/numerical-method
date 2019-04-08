from sympy import *
import pandas as pd
import numpy
import math
import os


if __name__ == "__main__":
    fs = ["x**3 + 4*x**2 - 10", "x**2 - exp(x)**-x", "4*sin(x) - 3*x"]
    intervals = [(1, 2), (0, 1), (1, 2)]
    TOLs = [0.0005, 0.0001, 0.0001]

    for i in range(0, 3):
        f = sympify(fs[i])      # functions
        TOL = TOLs[i]
        a, b = intervals[i]     # interval [a, b]

        fa = f.subs("x", a)
        fb = f.subs("x", b)

        if fa * fb > 0:         # check if f(a) * f(b) < 0
            print("ERROR: f(a) * f(b) > 0 (function No." + str(i) + ")")
            continue

        table_list = []      # result table

        while abs(b - a) > TOL:
            p1 = a + (b - a) / 3
            p2 = a + (b - a) / 3 * 2

            fa = f.subs("x", a)
            fb = f.subs("x", b)
            fp1 = f.subs("x", p1)
            fp2 = f.subs("x", p2)

            if fp1 * fp2 > 0:   # f(p1) and f(p2) are equal sign
                if fp1 * fa < 0:
                    if abs(fp1 - fa) < abs(fp2 - fa):
                        b = p1
                    else:
                        b = p2
                else:
                    if abs(fp1 - fb) < abs(fp2 - fb):
                        a = p1
                    else:
                        a = p2
            else:               # f(p1) and f(p2) are different sigh
                if fp1 * fa < 0:
                    if abs(fp1 - fa) < abs(fp2 - fb):
                        b = p1
                    else:
                        a = p2
                else:
                    if abs(fp1 - fb) < abs(fp2 - fa):
                        a = p1
                    else:
                        b = p2

            table_list.append({
                "a": a,
                "b": b,
                "p1": p1,
                "p2": p2,
                "f(p1)": fp1,
                "f(p2)": fp2
            })

        df = pd.DataFrame(table_list)
        print(df)

    os.system("pause")
