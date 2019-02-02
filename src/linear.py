"""
OctaDist  Copyright (C) 2019  Rangsiman Ketkaew

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import numpy as np
from math import sqrt, pow


def norm_vector(v):
    """Returns the unit vector of the vector v

    :param v: array - vector
    :return: array - normalized vector
    """
    if np.linalg.norm(v) == 0:
        print("Error: Norm of vector", v, "is 0.")

    return v/np.linalg.norm(v)


def distance_between(a, b):
    """Find distance between two point, a = (x1, y1, z1) and b = (x2, y2, z2)

                 -----------------------------------
    distance = \/ (x2-x1)^2 + (y2-y1)^2 + (z2-z1)^2

    :param a: array - cartesian coordinate of point a
    :param b: array - cartesian coordinate of point b
    :return: float - distance
    """

    return sqrt(sum([pow(a[i]-b[i], 2) for i in range(len(a))]))


def distance_avg(x):
    """Calculate average bond distance

    :param x: array - coordinates of ligand atoms
    :return: float - average bond distance
    """
    dist_list = []

    for i in range(1, 7):
        dist = distance_between(x[i], x[0])
        dist_list.append(dist)

    return sum([dist_list[i] for i in range(6)])/6


def midpoint_of_line(a, b):
    """Find the midpoint of line segment, a = (x1,y1,z1) and b = (x2,y2,z2)

    :param a: array - cartesian coordinate of head atom
    :param b: array - cartesian coordinate of tail atom
    :return: array - midpoint of line segment
    """

    return np.array([(a[0] + b[0])/2, (a[1] + b[1])/2, (a[2] + b[2])/2])


def angle_between(p1, p2, p3):
    """Compute the angle between vector p2 - p1 and p3 - p1

                                / p2_x * p3_x + p2_y * p3_y + p2_z * p3_z  \
    angle (in radian) = arccos | ----------------------------------------- |
                               \               |p2| * |p3|                /

    :param p1: array - coordinate of atom 1
    :param p2: array - coordinate of atom 2
    :param p3: array - coordinate of atom 3
    :return: float - angle in degree unit
    """
    v1 = p2 - p1
    v2 = p3 - p1

    nv1 = norm_vector(v1)
    nv2 = norm_vector(v2)

    return np.degrees(np.arccos(np.clip(np.dot(nv1, nv2), -1.0, 1.0)))


def triangle_area(a, b, c):
    """Calculate the area of the triangle using the following equation


           |  AB X AC |
    Area = | -------- |     where AB = B - A
           |    2     |           AC = C - A

    :param a: point A - (Ax, Ay, Az)
    :param b: point B - (Bx, By, Bz)
    :param c: point C - (Cx, Cy, Cz)
    :return: float - triangle area
    """
    AB = b - a
    AC = c - a

    value = (pow(np.dot(AB[1], AC[2]) - np.dot(AB[2], AC[1]), 2) +
             pow(np.dot(AB[2], AC[0]) - np.dot(AB[0], AC[2]), 2) +
             pow(np.dot(AB[0], AC[1]) - np.dot(AB[1], AC[0]), 2))

    return sqrt(value)/2
