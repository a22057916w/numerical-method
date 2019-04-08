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

        p = oo       # set default value as infinity
        prev_p = 0  # set Pn-1 default value
        fac = fbc = 0   # count the number of replaced endpoint
        while abs(p - prev_p) > TOL:
            prev_p = p
            p = float(a - (fa * (b - a) /(fb - fa)))    # secant point where intersects x = 0
            fa = f.subs("x", a)
            fb = f.subs("x", b)
            fp = f.subs("x", p)

            # check if an endpoint stays the same for 3 times
            if fac > 3:
                fb /= 2     # f(b)/2 if b stays the same for 3 times
                fac = 0
            if fbc > 3:
                fa /= 2
                fbc = 0

            if fp * fa < 0:
                fac += 1    # add 1 for a being changed
                fbc = 0     # set 0 if a change (changes of a must be continuous)
                b = p
                fb = fp
            else:
                fbc += 1
                fac = 0
                a = p
                fa = fp

            table_list.append({
                "a": a,
                "b": b,
                "p": p,
                "f(p)": fp
            })

        df = pd.DataFrame(table_list)
        print(df)
