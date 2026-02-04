# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT

import matplotlib
import numpy as np


def polyfit(dates, levels, p):

    # Convert dates to numbers (hours since year '0' in Gregorian
    # calendar)
    x = matplotlib.dates.date2num(dates)

    # Use NumPy to find best of a polynomial to the levels data
    print(len(x))
    print(len(levels))
    p_coeff = np.polyfit(x - x[0], levels, p)

    # Create a polynomial from the coefficients
    poly = np.poly1d(p_coeff)

    return poly, x[0]
