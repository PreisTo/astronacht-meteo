import numpy as np


def magnus_formula(temp, rh):
    b = 17.625
    c = 243.04
    y = np.log(rh / 100) + (b * temp) / (c + temp)
    return (c * y) / (b - y)
