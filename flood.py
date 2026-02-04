# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""This module provides functionality for determining the flood risk
at a monitoring station.

"""

import sys

from . import utils


def stations_level_over_threshold(stations, tol):
    """Return list of (station, f) tuples, where f is the current water
    level as a fraction of the typical range. The list is for all
    stations with a water level fraction over tol.

    """

    station_over_limit = []
    for station in stations:
        rel_level = station.relative_water_level()
        if rel_level is not None:
            if rel_level > tol:
                station_over_limit.append((station, rel_level))

    return utils.sorted_by_key(station_over_limit, 1, reverse=True)


def stations_highest_rel_level(stations, N):
    """Return N stations with highest relative level"""

    _stations = stations_level_over_threshold(stations, -sys.float_info.max)
    return [station for station, l in _stations[:N]]
