"""
OctaDist  Copyright (C) 2019  Rangsiman Ketkaew

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import numpy as np
import linear
import proj


def find_8_faces(cl):
    """Find 8 triangular faces

    1) Choose 3 atoms out of 6 ligand atoms. The total number of combination is 20.

    2) Delete 12 faces that containing two trans atoms.
        2.1) Orthogonally project metal center atom on to the face: m ----> m'
        2.2) Compute the shortest distance between metal center and face
        2.3) Sort out the distances in ascending order
        2.4) Delete 12 faces which closest to metal center atom

    3) The rest of faces is 8.

    :param cl: array - XYZ coordinate of one metal center and six ligand atoms
                cl[0] = metal center atom of complex
                cl[i] = ligand atom of complex
    :return pal: array - plane_atom_list - list of atom on the projection plane
    :return pcl: array - plane_coord_list - list of coordinate of atom on the projection plane
    """
    print("Info: Find all 20 triangles of octahedron")
    print("Info: Find minimum distance from metal center to each triangle")

    pal = []
    pcl = []

    for i in range(1, 5):
        for j in range(i + 1, 6):
            for k in range(j + 1, 7):
                a, b, c, d = find_eq_of_plane(cl[i], cl[j], cl[k])
                m = proj.project_atom_onto_plane(cl[0], a, b, c, d)
                d_btw = linear.distance_between(m, cl[0])
                pal.append([i, j, k])
                pcl.append([cl[i], cl[j], cl[k], d_btw])

    print("Info: Show atoms of each triangle and minimum distance (Angstrom) before sorting out\n")
    print("      Triangle     Minimum distance")
    print("      ---------    ----------------")

    for i in range(len(pcl)):
        print("      {0}      {1:10.6f}".format(pal[i], pcl[i][3]))

    # Sort pcl in ascending order of the minimum distance (column 4)
    i = 0
    while i < len(pcl):
        k = i
        j = i + 1
        while j < len(pcl):
            if pcl[k][3] > pcl[j][3]:
                k = j
            j += 1
        pcl[i], pcl[k] = pcl[k], pcl[i]
        pal[i], pal[k] = pal[k], pal[i]

        i += 1

    print("\nInfo: Sort out minimum distance in ascending order")
    print("Info: Show octahedron triangles after sorting minimum distance out\n")
    print("      Triangle     Minimum distance")
    print("      ---------    ----------------")

    for i in range(len(pcl)):
        print("      {0}      {1:10.6f}".format(pal[i], pcl[i][3]))

    # Remove first 12 triangles, the rest of triangles is 8 faces of octahedron
    print("\nInfo: Delete 12 triangles that mostly close to metal center atom")

    scl = pcl[12:]
    sal = pal[12:]

    # Print new plane list after unwanted plane excluded
    print("Info: Show 8 triangles (faces of octahedron) after deleting unwanted 12 triangles\n")
    print("      Face  Atom         X           Y           Z")
    print("      ----  ----     ---------   ---------   ---------")

    for i in range(len(scl)):
        print("              {0}     {1:10.6f}  {2:10.6f}  {3:10.6f}"
              .format(sal[i][0], scl[i][0][0], scl[i][0][1], scl[i][0][2]))
        print("        {0}     {1}     {2:10.6f}  {3:10.6f}  {4:10.6f}"
              .format(i+1, sal[i][1], scl[i][1][0], scl[i][1][1], scl[i][1][2]))
        print("              {0}     {1:10.6f}  {2:10.6f}  {3:10.6f}"
              .format(sal[i][2], scl[i][2][0], scl[i][2][1], scl[i][2][2]))
        print("      ------------------------------------------------")

    plane_atom_list = sal

    # Remove the 4th column (distance)
    plane_coord_list = np.delete(scl, 3, 1)

    return plane_atom_list, plane_coord_list


def find_opposite_atoms(x, cl):
    """Find the atom on the parallel opposite face (plane).
    For example,

    list of atom on reference plane    list of atom on opposite plane
             [[1 2 3]                            [[4 5 6]
              [1 2 4]              --->           [3 5 6]
              [2 3 5]]                            [1 4 6]]

    :param x: list - list of three ligand atoms for 4 reference planes (pal)
    :param cl: array - coordinates of octahedron atoms (coord_list)
    :return oppo_pal: list - atoms on the opposite plane
    :return oppo_pcl: array - coordinates of atoms on the opposite plane
    """
    print("\nInfo: Find pair of opposite faces")
    print("Info: Show 8 pairs of opposite faces")

    all_atom = [1, 2, 3, 4, 5, 6]
    oppo_pal = []

    # loop over 4 reference planes
    for i in range(len(x)):
        # Find the list of atoms on opposite plane
        new_pal = []

        for j in all_atom:
            if j not in (x[i][0], x[i][1], x[i][2]):
                new_pal.append(j)
        oppo_pal.append(new_pal)

    print("\n      Pair   Reference    Opposite")
    print("               face         face")
    print("      ----   ---------    ---------")

    v = np.array(cl)

    for i in range(len(oppo_pal)):
        print("        {0}    {1}    {2}".format(i+1, x[i], oppo_pal[i]))

    print("\nInfo: Show 8 opposite faces\n")
    print("      Face  Atom         X           Y           Z")
    print("      ----  ----     ---------   ---------   ---------")

    oppo_pcl = []

    for i in range(len(oppo_pal)):
        new_pcl = []
        for j in range(3):
            new_pcl.append([v[int(oppo_pal[i][j])][0], v[int(oppo_pal[i][j])][1], v[int(oppo_pal[i][j])]][2])
            oppo_pcl.append(new_pcl)

        print("              {0}     {1:10.6f}  {2:10.6f}  {3:10.6f}"
              .format(oppo_pal[i][0], new_pcl[0][0], new_pcl[0][1], new_pcl[0][2]))
        print("        {0}     {1}     {2:10.6f}  {3:10.6f}  {4:10.6f}"
              .format(i + 1, oppo_pal[i][1], new_pcl[1][0], new_pcl[1][1], new_pcl[1][2]))
        print("              {0}     {1:10.6f}  {2:10.6f}  {3:10.6f}"
              .format(oppo_pal[i][2], new_pcl[2][0], new_pcl[2][1], new_pcl[2][2]))
        print("      ------------------------------------------------")

    return oppo_pal, oppo_pcl


def find_eq_of_plane(x, y, z):
    """Find the equation of plane of given three points (ligand atoms)
    The general form of plane equation is Ax + By + Cz = D
    where A, B, C, and D are coefficient. They can be computed using cross product definition

    -->    -->
    XZ  X  XY = (a, b, c)

    d = (a, b, c).Z

    :param x: array - point 1
    :param y: array - point 2
    :param z: array - point 3
    :return a, b, c, d: float - coefficients of the equation of the given plane
    """
    XZ = z - x
    XY = y - x

    cross_vector = np.cross(XZ, XY)
    a, b, c = cross_vector
    d = np.dot(cross_vector, z)

    return a, b, c, d
