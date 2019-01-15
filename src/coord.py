"""
OctaDist  Copyright (C) 2019  Rangsiman Ketkaew

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import numpy as np
import elements


def file_len(fname):
    """Count line in file

    :param fname: string
    :return: number of line in file
    """
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def check_xyz_file(f):
    """Check if the input file is .xyz file format

    xyz file format
    ---------------

    <number of atom>
    comment
    <index 0> <X> <Y> <Z>
    <index 1> <X> <Y> <Z>
    <index 2> <X> <Y> <Z>
    <index 3> <X> <Y> <Z>
    <index 4> <X> <Y> <Z>
    <index 5> <X> <Y> <Z>
    <index 6> <X> <Y> <Z>

    ***The first atom must be a metal center.
    :param f: string - filename
    :return: int - 1 if the file is .xyz format
    """
    file = open(f, 'r')

    first_line = file.readline()

    first = 0

    try:
        first = int(first_line)
    except ValueError:
        return 0

    if file_len(f) >= 9:
        return 1
    else:
        return 0


def get_coord_from_xyz(f):
    """Get coordinate from .xyz file

    :param f: string - input file
    :return: atom_list and coord_list
    """
    print("Command: Get Cartesian coordinates")

    file = open(f, "r")
    # read file from 3rd line
    line = file.readlines()[2:]
    file.close()

    atom_list = []

    for l in line:
        # read atom on 1st column and insert to array
        lst = l.split(' ')[0]
        atom_list.append(lst)

    # Get only first 7 atoms
    atom_list = atom_list[0:7]

    """Read file again for getting XYZ coordinate
        We have two ways to do this, 
        1. use >> file.seek(0) <<
        2. use >> file = open(f, "r") <<
    """

    file = open(f, "r")
    coord_list = np.loadtxt(file, skiprows=2, usecols=[1, 2, 3])
    file.close()

    # Get only first 7 atoms
    coord_list = coord_list[0:7]

    return atom_list, coord_list


def check_txt_file(f):
    """Check if the input file
    text file format
    ----------------

    <index 0> <X> <Y> <Z>
    <index 1> <X> <Y> <Z>
    <index 2> <X> <Y> <Z>
    <index 3> <X> <Y> <Z>
    <index 4> <X> <Y> <Z>
    <index 5> <X> <Y> <Z>
    <index 6> <X> <Y> <Z>

    ***The first atom must be metal center.

    :param f: string - filename
    :return: int 1 if file is a .txt fie format
    """

    if file_len(f) < 7:
        return 0
    else:
        return 1


def get_coord_from_txt(f):
    """Get coordinate from .txt file

    :param f: string - file
    :return: atom_list and coord_list
    """
    print("Command: Get Cartesian coordinates")

    file = open(f, "r")
    line = file.readlines()
    file.close()

    atom_list = []

    for l in line:
        # read atom on 1st column and insert to array
        lst = l.split(' ')[0]
        atom_list.append(lst)

    # Get only first 7 atoms
    atom_list = atom_list[0:7]

    """Read file again for getting XYZ coordinate
        We have two ways to do this, 
        1. use >> file.seek(0) <<
        2. use >> file = open(f, "r") <<
    """

    file = open(f, "r")
    coord_list = np.loadtxt(file, skiprows=0, usecols=[1, 2, 3])
    file.close()

    # Get only first 7 atoms
    coord_list = coord_list[0:7]

    return atom_list, coord_list


def check_gaussian_file(f):
    """Check if the input file is Gaussian file format

    :param f: string - input file
    :return: int - 1 if file is Gaussian output file, return 0 if not.
    """
    gaussian_file = open(f, "r")
    nline = gaussian_file.readlines()

    for i in range(len(nline)):
        if "Standard orientation:" in nline[i]:
            return 1

    return 0


def get_coord_from_gaussian(f):
    """Extract XYZ coordinate from Gaussian output file

    :param f: string - input file
    :return: atom_list and coord_list
    """
    print("Command: Get Cartesian coordinates")

    gaussian_file = open(f, "r")
    nline = gaussian_file.readlines()

    start = 0
    end = 0

    atom_list, coord_list = [], []

    for i in range(len(nline)):
        if "Standard orientation:" in nline[i]:
            start = i

    for i in range(start + 5, len(nline)):
        if "---" in nline[i]:
            end = i
            break

    for line in nline[start + 5: end]:
        dat = line.split()
        dat1 = int(dat[1])
        coord_x = float(dat[3])
        coord_y = float(dat[4])
        coord_z = float(dat[5])

        dat1 = elements.check_atom(dat1)

        atom_list.append(dat1)
        coord_list.append([coord_x, coord_y, coord_z])

    gaussian_file.close()

    atom_list = atom_list[0:7]
    coord_list = np.asarray(coord_list[0:7])

    return atom_list, coord_list


def check_nwchem_file(f):
    """Check if the input file is NWChem file format

    :param f: string - input file
    :return: int - 1 if file is NWChem output file, return 0 if not.
    """
    nwchem_file = open(f, "r")
    nline = nwchem_file.readlines()

    for i in range(len(nline)):
        if "No. of atoms" in nline[i]:
            if not int(nline[i].split()[4]):
                return 0

    for j in range(len(nline)):
        if "Optimization converged" in nline[j]:
            return 1

    return 0


def get_coord_from_nwchem(f):
    """Extract XYZ coordinate from NWChem output file

    :param f: string - input file
    :return: atom_list and coord_list
    """
    print("Command: Get Cartesian coordinates")

    nwchem_file = open(f, "r")
    nline = nwchem_file.readlines()

    start = 0
    end = 0

    atom_list, coord_list = [], []

    for i in range(len(nline)):
        if "Optimization converged" in nline[i]:
            start = i

    for i in range(len(nline)):
        if "No. of atoms" in nline[i]:
            end = int(nline[i].split()[4])

    start = start + 18
    end = start + end

    # The 1st line of coordinate is at 18 lines next to 'Optimization converged'
    for line in nline[start:end]:
        dat = line.split()
        dat1 = int(float(dat[2]))
        coord_x = float(dat[3])
        coord_y = float(dat[4])
        coord_z = float(dat[5])

        dat1 = elements.check_atom(dat1)

        atom_list.append(dat1)
        coord_list.append([coord_x, coord_y, coord_z])

    nwchem_file.close()

    atom_list = atom_list[0:7]
    coord_list = np.asarray(coord_list[0:7])

    return atom_list, coord_list


def check_orca_file(f):
    """Check if the input file is ORCA file format

    :param f: string - input file
    :return: int - 1 if file is ORCA output file, return 0 if not.
    """
    orca_file = open(f, "r")
    nline = orca_file.readlines()

    for i in range(len(nline)):
        if "CARTESIAN COORDINATES (ANGSTROEM)" in nline[i]:
            return 1

    return 0


def get_coord_from_orca(f):
    """Extract XYZ coordinate from ORCA output file

    :param f: string - input file
    :return: atom_list and coord_list
    """
    print("Command: Get Cartesian coordinates")

    orca_file = open(f, "r")
    nline = orca_file.readlines()

    start = 0
    end = 0

    atom_list, coord_list = [], []

    for i in range(len(nline)):
        if "CARTESIAN COORDINATES (ANGSTROEM)" in nline[i]:
            start = i

    for i in range(start + 2, len(nline)):
        if "---" in nline[i]:
            end = i - 1
            break

    for line in nline[start + 2:end]:
        dat = line.split()
        dat1 = dat[0]
        coord_x = float(dat[1])
        coord_y = float(dat[2])
        coord_z = float(dat[3])

        atom_list.append(dat1)
        coord_list.append([coord_x, coord_y, coord_z])

    orca_file.close()

    atom_list = atom_list[0:7]
    coord_list = np.asarray(coord_list[0:7])

    return atom_list, coord_list


def get_coord(f):
    """Check file type, read data, extract atom and coord from input file

    :param f: string - input file
    :return: insert atom and coord read from input file into text box
    """
    # Check file extension
    if f.endswith(".xyz"):
        if check_xyz_file(f) == 1:
            print("         File type: XYZ file\n")
            atom_list, coord_list = get_coord_from_xyz(f)
        else:
            print("Error: Invalid XYZ file format")
            print("       Could not read data in XYZ file '%s'\n" % f)
    elif f.endswith(".txt"):
        if check_txt_file(f) == 1:
            print("         File type: TEXT file")
            print("")
            atom_list, coord_list = get_coord_from_txt(f)
        else:
            print("Error: Invalid TEXT file format")
            print("       Could not read data in TEXT file '%s'\n" % f)
    elif check_gaussian_file(f) == 1:
        print("         File type: Gaussian Output\n")
        atom_list, coord_list = get_coord_from_gaussian(f)
    else:
        print("Error")
        print("Error: Could not read file '%s'\n" % f)

    return atom_list, coord_list

