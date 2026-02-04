# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT

import datetime

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import date2num

from . import analysis
from .datafetcher import fetch_measure_levels


def plot_water_level(station, dates, levels):

    # Plot water levels
    plt.plot(dates, levels)

    # Add typical range
    typical_range = station.typical_range
    plt.plot((dates[0], dates[-1]), (typical_range[0], typical_range[0]), '--')
    plt.plot((dates[0], dates[-1]), (typical_range[1], typical_range[1]), '--')

    # Add axis labels
    plt.xlabel('date')
    plt.ylabel('water level (m)')
    plt.xticks(rotation=45)

    # Add title
    plt.title(station.name)

    plt.tight_layout()
    plt.show()


def plot_water_level_with_fit(station, dates, levels, p):

    if len(dates) == 0:
        print("Warning: date array is empty for station '{}'".format(
            station.name))
        return

    if len(dates) != len(levels):
        print(
            "Warning: date and level arrays have different lengths for station '{}'"
            .format(station.name))
        return

    # Compute data fit
    poly, t0 = analysis.polyfit(dates, levels, p)

    # Plot water levels
    plt.plot(dates, levels)

    # Plot fit
    t = np.linspace(date2num(dates[0]), date2num(dates[-1]), 60)
    plt.plot(t, poly(t - t0))

    # Add typical range
    typical_range = station.typical_range
    plt.plot((dates[0], dates[-1]), (typical_range[0], typical_range[0]), '--')
    plt.plot((dates[0], dates[-1]), (typical_range[1], typical_range[1]), '--')

    # Add axis labels
    plt.xlabel('date')
    plt.ylabel('water level (m)')
    plt.xticks(rotation=45)

    # Add title
    plt.title(station.name)

    plt.tight_layout()
    plt.show()


def plot_water_level_multi(stations, dt):

    max_plots = 6
    if len(stations) > max_plots:
        print(
            "Warning: plotting water level stations is limited to 6 stations. Plotting first {} only"
            .format(max_plots))

    # Add axis labels
    plt.xlabel('date')
    plt.ylabel('water level (m)')

    # Determine number of rows and columns in plot
    num_rows = 1
    if len(stations) > 1:
        num_rows = 2
    num_cols = (len(stations[:max_plots]) + 1) // 2

    # Plot each station
    counter = 0
    for station in stations[:max_plots]:

        # Fetch data for station
        dates, levels = fetch_measure_levels(
            station.measure_id, dt=datetime.timedelta(days=dt))

        # Add subplot
        plt.subplot(num_rows, num_cols, counter + 1)
        plt.plot(dates, levels)

        # Add typical range
        typical_range = station.typical_range
        plt.plot((dates[0], dates[-1]), (typical_range[0], typical_range[0]),
                 '--')
        plt.plot((dates[0], dates[-1]), (typical_range[1], typical_range[1]),
                 '--')

        # Add title
        plt.title(station.name)
        plt.xticks(rotation=45)

        counter += 1

    # Display plot
    plt.tight_layout()
    plt.show()
