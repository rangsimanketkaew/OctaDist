# OctaDist  Copyright (C) 2019  Rangsiman Ketkaew et al.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import functools
import tkinter as tk
from tkinter import scrolledtext as tkscrolled

import numpy as np
import rmsd
import scipy.optimize
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from octadist_gui.src import linear, elements, util


class CalcJahnTeller:
    """
    Calculate angular Jahn-Teller distortion parameter.

    Parameters
    ----------
    atom : array_like
        Atomic labels of full complex.
    coord : array_like
        Atomic coordinates of full complex.
    master : None, object
        If None, use tk.Tk().
        If not None, use tk.Toplevel(master).

    Examples
    --------
    >>> atom = ['Fe', 'N', 'N', 'N', 'O', 'O', 'O']

    >>> coord = [[2.298354000, 5.161785000, 7.971898000],
                 [1.885657000, 4.804777000, 6.183726000],
                 [1.747515000, 6.960963000, 7.932784000],
                 [4.094380000, 5.807257000, 7.588689000],
                 [0.539005000, 4.482809000, 8.460004000],
                 [2.812425000, 3.266553000, 8.131637000],
                 [2.886404000, 5.392925000, 9.848966000]]

    >>> test = CalcJahnTeller(atom=atom, coord=coord)
    >>> test.start_app()
    >>> test.create_widget()
    >>> test.find_bond()
    >>> test.show_app()

    """
    def __init__(self, atom, coord, master=None):
        self.atom = atom
        self.coord = coord

        if master is None:
            self.wd = tk.Tk()
        else:
            self.wd = tk.Toplevel(master)

        self.bond_list = []
        self.coord_A = []
        self.coord_B = []

    def start_app(self):
        """
        Start application.

        """
        self.wd.wm_iconbitmap(r"..\images\molecule.ico")
        self.wd.title("Calculate Jahn-Teller distortion parameter")
        self.wd.geometry("630x550")

    def create_widget(self):
        """
        Create widgets.

        """
        self.lbl = tk.Label(self.wd, text="Group A")
        self.lbl.config(width=12)
        self.lbl.grid(padx="10", pady="5", row=0, column=0, columnspan=2)

        self.lbl = tk.Label(self.wd, text="Group B")
        self.lbl.config(width=12)
        self.lbl.grid(padx="10", pady="5", row=0, column=2, columnspan=2)

        self.box_1 = tkscrolled.ScrolledText(self.wd, height="12", width="40", wrap="word", undo="True")
        self.box_1.grid(padx="5", pady="5", row=1, column=0, columnspan=2)

        self.box_2 = tkscrolled.ScrolledText(self.wd, height="12", width="40", wrap="word", undo="True")
        self.box_2.grid(padx="5", pady="5", row=1, column=2, columnspan=2)

        self.btn = tk.Button(self.wd, text="Select ligand set A", command=lambda: self.pick_atom(group="A"))
        self.btn.config(width=15, relief=tk.RAISED)
        self.btn.grid(padx="10", pady="5", row=2, column=0, columnspan=2)

        self.btn = tk.Button(self.wd, text="Select ligand set B", command=lambda: self.pick_atom(group="B"))
        self.btn.config(width=15, relief=tk.RAISED)
        self.btn.grid(padx="10", pady="5", row=2, column=2, columnspan=2)

        self.btn = tk.Button(self.wd, text="Calculate parameter", command=lambda: self.plot_fit_plane())
        self.btn.config(width=15, relief=tk.RAISED)
        self.btn.grid(padx="10", pady="5", row=3, column=0, columnspan=2)

        self.btn = tk.Button(self.wd, text="Clear all", command=lambda: self.clear_text())
        self.btn.config(width=15, relief=tk.RAISED)
        self.btn.grid(padx="10", pady="5", row=3, column=2, columnspan=2)

        self.lbl = tk.Label(self.wd, text="Supplementary angles between two planes (in degree)")
        self.lbl.grid(pady="10", row=4, columnspan=4)

        self.lbl_angle1 = tk.Label(self.wd, text="Angle 1")
        self.lbl_angle1.grid(pady="5", row=5, column=0)
        self.box_angle1 = tk.Entry(self.wd, width="20", justify='center')
        self.box_angle1.grid(row=5, column=1, sticky=tk.W)

        self.lbl_angle2 = tk.Label(self.wd, text="Angle 2")
        self.lbl_angle2.grid(pady="5", row=6, column=0)
        self.box_angle2 = tk.Entry(self.wd, width="20", justify='center')
        self.box_angle2.grid(row=6, column=1, sticky=tk.W)

        self.lbl = tk.Label(self.wd, text="The equation of the planes")
        self.lbl.grid(pady="10", row=7, columnspan=4)

        self.lbl_eq1 = tk.Label(self.wd, text="Plane A ")
        self.lbl_eq1.grid(pady="5", row=8, column=0)
        self.box_eq1 = tk.Entry(self.wd, width="60", justify='center')
        self.box_eq1.grid(pady="5", row=8, column=1, columnspan=2, sticky=tk.W)

        self.lbl_eq2 = tk.Label(self.wd, text="Plane B ")
        self.lbl_eq2.grid(pady="5", row=9, column=0)
        self.box_eq2 = tk.Entry(self.wd, width="60", justify='center')
        self.box_eq2.grid(pady="5", row=9, column=1, columnspan=2, sticky=tk.W)

    def find_bond(self):
        """
        Find bonds.

        """
        self.bond_list = util.find_bonds(self.atom, self.coord)

    #################
    # Picking atoms #
    #################

    def pick_atom(self, group):
        """
        On-mouse pick atom and get XYZ coordinate.

        Parameters
        ----------
        group : str
            Group A or B.

        """
        fig = plt.figure()
        # fig = plt.figure(figsize=(5, 4), dpi=100)
        ax = Axes3D(fig)
        # ax = fig.add_subplot(111, projection='3d')

        # Plot all atoms
        for i in range(len(self.coord)):
            # Determine atomic number
            n = elements.check_atom(self.atom[i])
            ax.scatter(self.coord[i][0], self.coord[i][1], self.coord[i][2],
                       marker='o', linewidths=0.5, edgecolors='black', picker=5,
                       color=elements.check_color(n), label=f"{self.atom[i]}",
                       s=elements.check_radii(n) * 300)

        atoms_pair = []
        for i in range(len(self.bond_list)):
            get_atoms = self.bond_list[i]
            x, y, z = zip(*get_atoms)
            atoms = list(zip(x, y, z))
            atoms_pair.append(atoms)

        # Draw line
        for i in range(len(atoms_pair)):
            merge = list(zip(atoms_pair[i][0], atoms_pair[i][1]))
            x, y, z = merge
            ax.plot(x, y, z, 'k-', color="black", linewidth=2)

        # Set legend
        # Remove duplicate labels in legend.
        # Ref.https://stackoverflow.com/a/26550501/6596684
        handles, labels = ax.get_legend_handles_labels()
        handle_list, label_list = [], []
        for handle, label in zip(handles, labels):
            if label not in label_list:
                handle_list.append(handle)
                label_list.append(label)
        leg = fig.legend(handle_list, label_list,
                         loc="lower left", scatterpoints=1, fontsize=12)
        # Fixed size of point in legend
        # Ref. https://stackoverflow.com/a/24707567/6596684
        for i in range(len(leg.legendHandles)):
            leg.legendHandles[i]._sizes = [90]

        # Set axis
        ax.set_xlabel(r'X', fontsize=15)
        ax.set_ylabel(r'Y', fontsize=15)
        ax.set_zlabel(r'Z', fontsize=15)
        ax.set_title('Full complex', fontsize="12")
        ax.grid(True)

        def insert_text(text, coord, group):
            """
            Insert text in boxes.

            Parameters
            ----------
            text : str
                Text.
            coord : list or array
                Coordinates.
            group : str
                Group A or B.

            """
            if group == "A":
                self.box_1.insert(tk.INSERT, text + "\n")
                self.box_1.see(tk.END)

                self.coord_A.append(coord)

            elif group == "B":
                self.box_2.insert(tk.INSERT, text + "\n")
                self.box_2.see(tk.END)

                self.coord_B.append(coord)

        def on_pick(event):
            """
            Pick point and get XYZ data

            Parameters
            ----------
            event : object
                Event object for on-pick function.

            Examples
            --------
            >>> def on_pick(event):
            >>> ... ind = event.ind
            >>> ... print("on_pick scatter:", ind, np.take(x, ind), np.take(y, ind))

            """
            ind = event.ind[0]
            x, y, z = event.artist._offsets3d
            for i in range(len(self.atom)):
                if x[ind] == self.coord[i][0]:
                    if y[ind] == self.coord[i][1]:
                        if z[ind] == self.coord[i][2]:
                            atom = self.atom[i]
                            break

            results = f"{i + 1}  {atom}  :  {x[ind]} {y[ind]} {z[ind]}"
            coord = [x[ind], y[ind], z[ind]]
            insert_text(results, coord, group)
            # Highlight selected atom
            index = elements.check_atom(atom)
            ax.scatter(x[ind], y[ind], z[ind],
                       marker='o', linewidths=0.5,
                       edgecolors='orange', picker=5, alpha=0.5,
                       color='yellow', s=elements.check_radii(index) * 400)
            # print(i+1, atom, x[ind], y[ind], z[ind])

        fig.canvas.mpl_connect('pick_event', on_pick)

        # plt.axis('equal')
        # plt.axis('off')
        plt.show()

    #########################################
    # Find best fit plane to selected atoms #
    #########################################

    def find_fit_plane(self, coord):
        """
        Find best fit plane to the given data points (atoms).

        scipy.optimize.minimize is used to find the least-square plane.

        Parameters
        ----------
        coord : array_like
            Coordinates of selected atom chunk.

        Returns
        -------
        xx, yy, z : float
            Coefficient of the surface.
        abcd : tuple
            Coefficient of the equation of the plane.

        Examples
        --------
        >>> Example of set of coordinate of atoms.
        points = [(1.1, 2.1, 8.1),
                  (3.2, 4.2, 8.0),
                  (5.3, 1.3, 8.2),
                  (3.4, 2.4, 8.3),
                  (1.5, 4.5, 8.0),
                  (5.5, 6.7, 4.5)]

        >>> # To plot the plane, run following commands:
        ... # map coordinates for scattering plot

        >>> xs, ys, zs = zip(*points)
        ... ax.scatter(xs, ys, zs)

        """
        def plane(x, y, params):
            a = params[0]
            b = params[1]
            c = params[2]
            z = a * x + b * y + c
            return z

        def error(params, points):
            result = 0
            for (x, y, z) in points:
                plane_z = plane(x, y, params)
                diff = abs(plane_z - z)
                result += diff ** 2
            return result

        def cross(a, b):
            return [a[1] * b[2] - a[2] * b[1],
                    a[2] * b[0] - a[0] * b[2],
                    a[0] * b[1] - a[1] * b[0]]

        points = coord

        fun = functools.partial(error, points=points)
        params0 = [0, 0, 0]
        res = scipy.optimize.minimize(fun, params0)

        a = res.x[0]
        b = res.x[1]
        c = res.x[2]

        point = np.array([0.0, 0.0, c])
        normal = np.array(cross([1, 0, a], [0, 1, b]))
        d = -point.dot(normal)
        xx, yy = np.meshgrid([-5, 10], [-5, 10])
        z = (-normal[0] * xx - normal[1] * yy - d) * 1. / normal[2]

        abcd = (a, b, c, d)

        return xx, yy, z, abcd

    ########################################
    # Plot fit plant to the selected atoms #
    ########################################

    def plot_fit_plane(self):
        """
        Display complex and two fit planes of two sets of ligand in molecule.

        """
        ###############
        # Clear boxes #
        ###############

        self.box_angle1.delete(0, tk.END)
        self.box_angle2.delete(0, tk.END)

        self.box_eq1.delete(0, tk.END)
        self.box_eq2.delete(0, tk.END)

        ########################
        # Find eq of the plane #
        ########################

        xx, yy, z, abcd = self.find_fit_plane(self.coord_A)
        plane_A = (xx, yy, z)
        a1, b1, c1, d1 = abcd

        self.box_eq1.insert(tk.INSERT, f"{a1:8.5f}x {b1:+8.5f}y {c1:+8.5f}z {d1:+8.5f} = 0")

        xx, yy, z, abcd = self.find_fit_plane(self.coord_B)
        plane_B = (xx, yy, z)
        a2, b2, c2, d2 = abcd

        self.box_eq2.insert(tk.INSERT, f"{a2:8.5f}x {b2:+8.5f}y {c2:+8.5f}z {d2:+8.5f} = 0")

        ####################################
        # Calculate angle between 2 planes #
        ####################################

        angle = linear.angle_btw_planes(a1, b1, c1, a2, b2, c2)
        self.box_angle1.insert(tk.INSERT, f"{angle:10.6f}")  # insert to box

        sup_angle = abs(180 - angle)  # supplementary angle
        self.box_angle2.insert(tk.INSERT, f"{sup_angle:10.6f}")  # insert to box

        ###############
        # Plot planes #
        ###############

        fig = plt.figure()
        # fig = plt.figure(figsize=(5, 4), dpi=100)
        ax = Axes3D(fig)
        # ax = fig.add_subplot(111, projection='3d')

        # Plot all atoms
        for i in range(len(self.coord)):
            # Determine atomic number
            n = elements.check_atom(self.atom[i])
            ax.scatter(self.coord[i][0], self.coord[i][1], self.coord[i][2],
                       marker='o', linewidths=0.5, edgecolors='black', picker=5,
                       color=elements.check_color(n), label=f"{self.atom[i]}",
                       s=elements.check_radii(n) * 300)

        atoms_pair = []
        for i in range(len(self.bond_list)):
            get_atoms = self.bond_list[i]
            x, y, z = zip(*get_atoms)
            atoms = list(zip(x, y, z))
            atoms_pair.append(atoms)

        # Draw line
        for i in range(len(atoms_pair)):
            merge = list(zip(atoms_pair[i][0], atoms_pair[i][1]))
            x, y, z = merge
            ax.plot(x, y, z, 'k-', color="black", linewidth=2)

        # Set legend
        # Remove duplicate labels in legend.
        # Ref.https://stackoverflow.com/a/26550501/6596684
        handles, labels = ax.get_legend_handles_labels()
        handle_list, label_list = [], []
        for handle, label in zip(handles, labels):
            if label not in label_list:
                handle_list.append(handle)
                label_list.append(label)
        leg = fig.legend(handle_list, label_list,
                         loc="lower left", scatterpoints=1, fontsize=12)
        # Fixed size of point in legend
        # Ref. https://stackoverflow.com/a/24707567/6596684
        for i in range(len(leg.legendHandles)):
            leg.legendHandles[i]._sizes = [90]

        # Set axis
        ax.set_xlabel(r'X', fontsize=15)
        ax.set_ylabel(r'Y', fontsize=15)
        ax.set_zlabel(r'Z', fontsize=15)
        ax.set_title('Full complex', fontsize="12")
        ax.grid(True)

        # Plot plane A
        xx, yy, z = plane_A
        ax.plot_surface(xx, yy, z, alpha=0.2, color='green')

        # Plot plane B
        xx, yy, z = plane_B
        ax.plot_surface(xx, yy, z, alpha=0.2, color='red')

        # ax.set_xlim(-10, 10)
        # ax.set_ylim(-10, 10)
        # ax.set_zlim(0, 10)

        # plt.axis('equal')
        # plt.axis('off')
        plt.show()

    ##################
    # Clear text box #
    ##################

    def clear_text(self):
        """
        Clear text in box A & B.

        """
        self.box_1.delete(1.0, tk.END)
        self.box_2.delete(1.0, tk.END)

        self.box_angle1.delete(0, tk.END)
        self.box_angle2.delete(0, tk.END)

        self.box_eq1.delete(0, tk.END)
        self.box_eq2.delete(0, tk.END)

        self.coord_A = []
        self.coord_B = []

        try:
            plt.close("all")
        except AttributeError:
            pass

    def show_app(self):
        """
        Show application.

        """
        self.wd.mainloop()


class CalcRMSD:
    """
    Calculate root mean squared displacement of atoms in complex, RMSD.

    Parameters
    ----------
    coord_1 : array_list
        Atomic labels and coordinates of structure 1.
    coord_2 : array_list
        Atomic labels and coordinates of structure 2.

    Returns
    -------
    rmsd_normal : float
        Normal RMSD.
    rmsd_translate : float
        Translate RMSD (re-centered).
    rmsd_rotate : float
        Kabsch RMSD (rotated).

    References
    ----------
    https://github.com/charnley/rmsd

    Examples
    --------
    >>> comp1.xyz
    Fe       10.187300000     5.746300000     5.615000000
    O         8.494000000     5.973500000     4.809100000
    O         9.652600000     6.422900000     7.307900000
    N        10.803800000     7.531900000     5.176200000
    N         9.622900000     3.922100000     6.008300000
    N        12.006500000     5.556200000     6.349700000
    N        10.804600000     4.947100000     3.921900000

    >>> comp2.xyz
    Fe       12.093762780     2.450541280     3.420711630
    O        12.960362780     2.295241280     1.728611630
    O        13.487662780     1.618241280     4.423011630
    N        12.852262780     4.317441280     3.989411630
    N        10.930762780     0.769741280     2.931511630
    N        10.787862780     2.298741280     5.107111630
    N        10.677362780     3.796041280     2.542411630

    >>> comp1_xyz = get_octa(comp1.xyz)
    >>> comp2_xyz = get_octa(comp2.xyz)

    >>> test = CalcRMSD(coord_1=comp1_xyz, coord_2=comp2_xyz)

    >>> rmsd_normal = test.get_rmsd_normal()
    >>> rmsd_translate = test.get_rmsd_translate()
    >>> rmsd_rotate = test.get_rmsd_rotate()

    >>> rmsd_normal
    6.758144

    >>> rmsd_translate
    0.305792

    >>> rmsd_rotate
    0.277988

    """
    def __init__(self, coord_1, coord_2):
        self.coord_1 = np.asarray(coord_1, dtype=np.float64)
        self.coord_2 = np.asarray(coord_2, dtype=np.float64)

        self.rmsd_normal = 0
        self.rmsd_translate = 0
        self.rmsd_rotate = 0

        self.calc_rmsd_normal()
        self.calc_rmsd_translate()
        self.calc_rmsd_rotate()

    def calc_rmsd_normal(self):
        """
        Calculate normal RMSD.

        """
        self.rmsd_normal = rmsd.rmsd(self.coord_1, self.coord_2)

    def calc_rmsd_translate(self):
        """
        Calculate translate RMSD.

        """
        # Manipulate recenter
        self.coord_1 -= rmsd.centroid(self.coord_1)
        self.coord_2 -= rmsd.centroid(self.coord_2)

        self.rmsd_translate = rmsd.rmsd(self.coord_1, self.coord_2)

    def calc_rmsd_rotate(self):
        """
        Calculate rotate RMSD.

        """
        # Rotate
        rotation_matrix = rmsd.kabsch(self.coord_1, self.coord_2)
        self.coord_1 = np.dot(self.coord_1, rotation_matrix)

        self.rmsd_rotate = rmsd.rmsd(self.coord_1, self.coord_2)

    def get_rmsd_normal(self):
        """
        Get normal RMSD.

        """
        return self.rmsd_normal

    def get_rmsd_translate(self):
        """
        Get translate RMSD.

        """
        return self.rmsd_translate

    def get_rmsd_rotate(self):
        """
        Get rotate RMSD.

        """
        return self.rmsd_rotate

