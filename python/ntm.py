from sympy import *
import pandas as pd
import numpy
import math
import os


if __name__ == "__main__":
    v = [729, 1500, -72]    # testcase

    for i in range(0, 3):
        if v[i] < 0:
            print("ERROR: v < 0 (function No." + str(i) + ")")
            continue

        f = sympify("x**2 - " + str(int(v[i])))      # functions
        print(f)
        table_list = []      # result table

        p = v[i]       # set default value as v
        prev_p = 0  # set Pn-1 default value as infinity

        while abs((p - prev_p) / p) > 0.0001:
            prev_p = p
            fprev_p = f.subs("x", prev_p)
            x = Symbol("x")
            p = float(prev_p - fprev_p / f.diff(x).subs("x", prev_p))

            table_list.append({
                "p": p,
                "f(p)": f.subs("x", p)
            })

        df = pd.DataFrame(table_list)
        print(p)
