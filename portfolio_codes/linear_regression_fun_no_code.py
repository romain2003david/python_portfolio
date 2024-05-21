import numpy as np
from sklearn.linear_model import LinearRegression

from pig_tv import *

import math

ts = [0, 22, 46, 74, 114, 178, 374]

apply_function_to_array(ts, lambda x:x*10**(-6))

vs = [6.406, 5.156, 4.156, 3.156, 2.156, 1.156, 0.188]

apply_function_to_array(vs, lambda x:math.log(x))

incertitude_vs = [(0.03)**2/(vs[x]**2) for x in range(len(vs))]

incertitude_t = [2*10**(-6) for x in range(len(ts))]

x = np.array(ts).reshape((-1, 1))

y = np.array(vs)


test = 1

if test:

    model = LinearRegression().fit(x, y)

    coef_deter = model.score(x, y)

    slope = model.coef_

    const = model.intercept_

    tau = -1/slope

    print(tau, coef_deter, const)

test = 0

if test:

    import matplotlib.pyplot as plt

    from scipy.odr import *

    def affin_func(p, x):
        a, b = p
        return a*x + b

    model = Model(affin_func)

    data = RealData(x, y, sx=incertitude_t, sy=incertitude_vs)

    odr = ODR(data, model, beta0=[0., 1.])

    out = odr.run()

    out.pprint()
