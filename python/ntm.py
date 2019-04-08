from sympy import *
import pandas as pd
import numpy
import math
import os


if __name__ == "__main__":
    v = [729, 1500, -72]    # testcase
    TOLs = [0.0005, 0.0001, 0.0001]

    for i in range(0, 3):
        if v[i] < 0:
            print("ERROR: f(a) * f(b) > 0 (function No." + str(i) + ")")
            continue

        f = sympify("x**2 - " + str(v[i]))      # functions
        TOL = TOLs[i]

        fa = f.subs("x", a)
        fb = f.subs("x", b)

        table_list = []      # result table

        p = oo       # set default value as infinity
        prev_p = v  # set Pn-1 default value
        while abs(p - prev_p) > TOL:
            p = prev_p - fprev_p / fprev_p.diff(x)
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
                fbc += 1    # add 1 for b being changed
                fac = 0     # set 0 if b change (changes of b must be continuous)
                b = p
                fb = fp
            else:
                fac += 1
                fbc = 0
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
