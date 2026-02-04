# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""This module contains a collection of functions related to
geographical data.

"""

from collections import defaultdict

from haversine import haversine

from .utils import sorted_by_key


def distance(p0, p1):
    """Return distance between two geographic coordinates (in km)"""
    return haversine(p0, p1)


def stations_by_distance(stations, p):
    """Return list of (station, distance) tuples, where 'distance' is the
    distance from the coordinate p. The list is sorted by distance.

    """

    # Build list of tuples (distance, station)
    stations_by_dist = []
    for station in stations:
        d = distance(p, station.coord)
        stations_by_dist.append((station, d))

    # Return list sorted by distance
    return sorted_by_key(stations_by_dist, 1)


def stations_within_radius(stations, centre, r):
    """Return list of names of all stations within a radius r of the
    coordinate 'centre' (all units in km)

    """

    # Build list of stations, sorted by distance
    station_by_dist = stations_by_distance(stations, centre)

    # Build list within r
    within_radius = []
    for station, d in station_by_dist:
        if d < r:
            within_radius.append(station)

    return within_radius


def rivers_with_station(stations):
    """Return set of all rivers with a monitoring station(s)"""

    # rivers = set()
    # for station in stations:
    #     rivers.add(station.get_river())
    rivers = set(station.river for station in stations)
    return rivers


def stations_by_river(stations):
    """Return dictionary that maps river name to a list of stations on the
    river

    """

    # Build dictionary (map) from river to monitoring stations
    river_to_stations = defaultdict(list)
    for station in stations:
        river_to_stations[station.river].append(station)

    return river_to_stations


def rivers_most_stations(stations, N):
    """Return list of (river, num stations) for (at least) N rivers with
    greatest number of monitoring stations. List is sorted by number
    of rivers.

    """

    # Get dict that maps river -> stations
    river_to_stations = stations_by_river(stations)

    # Build list [(river name, num stations)]
    num_stations_per_river = []
    for river, stations in river_to_stations.items():
        num_stations_per_river.append((river, len(stations)))

    # Shorter version using list comprehension
    # num_stations_per_river = [(river, len(stations))
    #                           for river, stations in river_to_stations.items()]

    # Sort by number of rivers (reverse order)
    num_stations_per_river = sorted_by_key(
        num_stations_per_river, 1, reverse=True)

    # Get N rivers with most stations
    rivers_most_stations = num_stations_per_river[:N]

    # If the last entry is 'tied' for number of stations, add extra
    # rivers
    while num_stations_per_river[N - 1][1] == num_stations_per_river[N][1]:
        rivers_most_stations.append((num_stations_per_river[N][0],
                                     num_stations_per_river[N][1]))
        N += 1

    return rivers_most_stations
