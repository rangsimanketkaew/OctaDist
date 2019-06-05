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

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import octadist_gui.src.structure
from octadist_gui.src import elements, tools, plane, projection


class DrawComplex:
    """
    Display 3D structure of octahedral complex with label for each atoms.

    Parameters
    ----------
    self.atom : list
        Atomic symbols of octahedral structure.
    self.coord : list or array or tuple
        Atomic coordinates of octahedral structure.

    Returns
    -------
    None : None

    Examples
    --------
    >>> atom
    ['Fe', 'N', 'N', 'N', 'O', 'O', 'O']
    >>> coord
    [[2.298354000, 5.161785000, 7.971898000],  # <- Metal atom
     [1.885657000, 4.804777000, 6.183726000],
     [1.747515000, 6.960963000, 7.932784000],
     [4.094380000, 5.807257000, 7.588689000],
     [0.539005000, 4.482809000, 8.460004000],
     [2.812425000, 3.266553000, 8.131637000],
     [2.886404000, 5.392925000, 9.848966000]]

    """
    def __init__(self, **kwargs):
        self.atom = kwargs.get('atom')
        self.coord = kwargs.get('coord')

        self.title_name = 'Display Complex'
        self.title_size = '12'
        self.label_size = '10'
        self.show_title = True
        self.show_axis = True
        self.show_grid = True

        self.atoms_pair = []
        self.bond_list = None

        self.start_plot()

    def start_plot(self):
        """
        Introduce figure to plot.

        Returns
        -------
        None : None

        """
        self.fig = plt.figure()
        self.ax = Axes3D(self.fig)

        self.ax.set_title('Full complex', fontsize="12")
        # ax = fig.add_subplot(111, projection='3d')

    def add_atom(self):
        """
        Add all atoms to show in figure.

        Returns
        -------
        None : None

        """
        for i in range(len(self.coord)):
            # Determine atomic number
            n = elements.check_atom(self.atom[i])
            self.ax.scatter(self.coord[i][0],
                            self.coord[i][1],
                            self.coord[i][2],
                            marker='o', linewidths=0.5, edgecolors='black',
                            color=elements.check_color(n), label=f"{self.atom[i]}",
                            s=elements.check_radii(n) * 300)

    def add_symbol(self):
        """
        Add symbol of atoms to show in figure.

        Returns
        -------
        None : None

        """
        for j in range(len(self.atom)):
            self.ax.text(self.coord[j][0] + 0.1,
                         self.coord[j][1] + 0.1,
                         self.coord[j][2] + 0.1,
                         f"{self.atom[j]},{j}", fontsize=9)

    def add_bond(self):
        """
        Calculate bond distance, screen bond, and add them to show in figure.

        Returns
        -------
        None : None

        """
        self.bond_list = octadist_gui.src.structure.find_bonds(self.atom, self.coord)
        for i in range(len(self.bond_list)):
            get_atoms = self.bond_list[i]
            x, y, z = zip(*get_atoms)
            atoms = list(zip(x, y, z))
            self.atoms_pair.append(atoms)

        for i in range(len(self.atoms_pair)):
            merge = list(zip(self.atoms_pair[i][0], self.atoms_pair[i][1]))
            x, y, z = merge
            self.ax.plot(x, y, z, 'k-', color="black", linewidth=2)

    def add_face(self, coord):
        """
        Find the faces of octahedral structure and add those faces to show in figure.

        Returns
        -------
        None : None

        """
        _, c_ref, _, _ = octadist_gui.src.structure.find_faces_octa(coord)

        # Added faces
        color_list = ["red", "blue", "green", "yellow",
                      "violet", "cyan", "brown", "grey"]
        for i in range(8):
            # Create array of vertices for 8 faces
            get_vertices = c_ref[i].tolist()
            x, y, z = zip(*get_vertices)
            vertices = [list(zip(x, y, z))]
            self.ax.add_collection3d(Poly3DCollection(vertices, alpha=0.5, color=color_list[i]))

    def add_legend(self):
        """
        Add all atoms to figure.

        Returns
        -------
        None : None

        Notes
        -----
        Remove duplicate labels in legend.
        Ref.https://stackoverflow.com/a/26550501/6596684

        Fix size of point in legend.
        Ref. https://stackoverflow.com/a/24707567/6596684

        """
        # remove duplicate labels
        handles, labels = self.ax.get_legend_handles_labels()
        handle_list, label_list = [], []
        for handle, label in zip(handles, labels):
            if label not in label_list:
                handle_list.append(handle)
                label_list.append(label)
        leg = plt.legend(handle_list, label_list,
                         loc="lower left", scatterpoints=1, fontsize=12)

        # fix size of point in legend
        for i in range(len(leg.legendHandles)):
            leg.legendHandles[i]._sizes = [90]

    def config_plot(self, show_title=True, show_axis=True, show_grid=True, **kwargs):
        """
        Setting configuration for figure.

        Parameters
        ----------
        show_title
        show_axis
        show_grid
        kwargs

        Returns
        -------
        None : None

        """
        title_name_user = kwargs.get('title_name')
        self.title_size = kwargs.get('title_size')
        self.label_size = kwargs.get('label_size')
        self.show_title = show_title
        self.show_axis = show_axis
        self.show_grid = show_grid

        if title_name_user is not None:
            self.ax.set_title(title_name_user)

        if self.title_size is not None:
            if title_name_user is None:
                title_name_user = self.title_name
            self.ax.set_title(title_name_user, fontsize=self.title_size)

        if self.label_size is not None:
            self.ax.set_xlabel(r'X', fontsize=self.label_size)
            self.ax.set_ylabel(r'Y', fontsize=self.label_size)
            self.ax.set_zlabel(r'Z', fontsize=self.label_size)

        if not self.show_title:
            self.ax.set_title('')
        if not self.show_axis:
            plt.axis('off')
        if not self.show_grid:
            self.ax.grid(False)

    def show_plot(self):
        """
        Show plot.

        Returns
        -------
        None : None

        """
        plt.show()


class DrawProjection:
    """
    Display the selected 4 faces of octahedral complex.

    Parameters
    ----------
    aco : list
        Atomic labels and coordinates of octahedral structure.

    Returns
    -------
    None : None

    """
    def __init__(self, **kwargs):
        self.atom = kwargs.get('atom')
        self.coord = kwargs.get('coord')

        self.sub_plot = []

        self.start_plot()
        self.shift_plot()

    def start_plot(self):
        """
        Introduce figure to plot.

        Returns
        -------
        None : None

        """
        self.fig = plt.figure()
        self.st = self.fig.suptitle("4 pairs of opposite planes", fontsize="x-large")

        for i in range(4):
            ax = self.fig.add_subplot(2, 2, int(i + 1), projection='3d')
            ax.set_title(f"Pair {i + 1}")
            self.sub_plot.append(ax)

    def shift_plot(self):
        """
        Shift subplots down. Default value is 0.25.

        Returns
        -------
        None : None

        """
        self.fig.subplots_adjust(top=0.25)
        self.st.set_y(1.0)

    def add_atom(self):
        """
        Add all atoms to show in figure.

        Returns
        -------
        None : None

        """
        for i in range(4):
            ax = self.sub_plot[i]
            # Metal
            ax.scatter(self.coord[0][0],
                       self.coord[0][1],
                       self.coord[0][2],
                       color='yellow', marker='o', s=100, linewidths=1,
                       edgecolors='black', label="Metal center")

            # Ligand
            for j in range(1, 7):
                ax.scatter(self.coord[j][0],
                           self.coord[j][1],
                           self.coord[j][2],
                           color='red', marker='o', s=50, linewidths=1,
                           edgecolors='black', label="Ligand atoms")

    def add_symbol(self):
        """
        Add all atoms to show in figure.

        Returns
        -------
        None : None

        """
        for i in range(4):
            ax = self.sub_plot[i]
            # Metal
            ax.text(self.coord[0][0] + 0.1,
                    self.coord[0][1] + 0.1,
                    self.coord[0][2] + 0.1,
                    self.atom[0], fontsize=9)

            # Ligand
            for j in range(1, 7):
                ax.text(self.coord[j][0] + 0.1,
                        self.coord[j][1] + 0.1,
                        self.coord[j][2] + 0.1,
                        f"{self.atom[j]},{j}", fontsize=9)

    def add_plane(self):
        """
        Add the projection planes to show in figure.

        Returns
        -------
        None : None

        """
        _, c_ref, _, c_oppo = octadist_gui.src.structure.find_faces_octa(self.coord)

        color_1 = ["red", "blue", "orange", "magenta"]
        color_2 = ["green", "yellow", "cyan", "brown"]

        for i in range(4):
            ax = self.sub_plot[i]

            # reference face
            get_vertices = c_ref[i].tolist()
            x, y, z = zip(*get_vertices)
            vertices_ref = [list(zip(x, y, z))]

            # opposite face
            x, y, z = zip(*c_oppo[i])
            vertices_oppo = [list(zip(x, y, z))]

            ax.add_collection3d(Poly3DCollection(vertices_ref, alpha=0.5, color=color_1[i]))
            ax.add_collection3d(Poly3DCollection(vertices_oppo, alpha=0.5, color=color_2[i]))

    def show_plot(self):
        """
        Show plot.

        Returns
        -------
        None : None

        """
        plt.tight_layout()
        plt.show()


class DrawTwistingPlane:
    """
    Display twisting triangular faces and vector projection.

    Parameters
    ----------
    aco : list
        Atomic labels and coordinates of octahedral structure.

    Returns
    -------
    None : None

    """
    def __init__(self, **kwargs):
        self.atom = kwargs.get('atom')
        self.coord = kwargs.get('coord')

        self.all_ax = []
        self.all_c_ref = []
        self.all_m = []
        self.all_proj_ligs = []

        self.start_plot()
        self.shift_plot()

    def start_plot(self):
        """
        Introduce figure to plot.

        Returns
        -------
        None : None

        """
        self.fig = plt.figure()
        self.st = self.fig.suptitle("Projected twisting triangular faces", fontsize="x-large")

    def shift_plot(self):
        """
        Shift subplots down. Default value is 0.25.

        Returns
        -------
        None : None

        """
        self.fig.subplots_adjust(top=0.25)
        self.st.set_y(1.0)

    def add_plane(self):
        """
        Add the projection planes to show in figure.

        Returns
        -------
        None : None

        """
        _, c_ref, _, c_oppo = octadist_gui.src.structure.find_faces_octa(self.coord)

        for i in range(4):
            ax = self.fig.add_subplot(2, 2, int(i + 1), projection='3d')
            ax.set_title(f"Projection plane {i + 1}", fontsize='10')
            a, b, c, d = plane.find_eq_of_plane(c_ref[i][0], c_ref[i][1], c_ref[i][2])
            m = projection.project_atom_onto_plane(self.coord[0], a, b, c, d)

            self.all_ax.append(ax)
            self.all_c_ref.append(c_ref[i])
            self.all_m.append(m)

            # Projected metal center atom
            ax.scatter(m[0],
                       m[1],
                       m[2],
                       color='orange', s=100, marker='o', linewidths=1,
                       edgecolors='black', label="Metal center")

            # Reference atoms
            all_proj_lig = []
            for j in range(3):
                ax.scatter(c_ref[i][j][0],
                           c_ref[i][j][1],
                           c_ref[i][j][2],
                           color='red', s=50, marker='o', linewidths=1,
                           edgecolors='black', label="Reference atom")

                # Project ligand atom onto the reference face
                proj_lig = projection.project_atom_onto_plane(c_oppo[i][j], a, b, c, d)
                all_proj_lig.append(proj_lig)

            # Projected opposite atoms
                ax.scatter(proj_lig[0],
                           proj_lig[1],
                           proj_lig[2],
                           color='blue', s=50, marker='o', linewidths=1,
                           edgecolors='black', label="Projected ligand atom")

            self.all_proj_ligs.append(all_proj_lig)

            # Draw plane
            get_vertices = c_ref[i].tolist()
            x, y, z = zip(*get_vertices)
            vertices = [list(zip(x, y, z))]

            x, y, z = zip(*self.all_proj_ligs[i])
            projected_oppo_vertices_list = [list(zip(x, y, z))]
            ax.add_collection3d(Poly3DCollection(vertices,
                                                 alpha=0.5,
                                                 color="yellow"))
            ax.add_collection3d(Poly3DCollection(projected_oppo_vertices_list,
                                                 alpha=0.5,
                                                 color="blue"))

    def add_bond(self):
        """
        Calculate bond distance, screen bond, and add them to show in figure.

        Returns
        -------
        None : None

        """
        for i in range(4):
            for j in range(3):
                merge = list(zip(self.all_m[i].tolist(), self.all_c_ref[i][j].tolist()))
                x, y, z = merge
                self.all_ax[i].plot(x, y, z, 'k-', color="black")

                merge = list(zip(self.all_m[i].tolist(), self.all_proj_ligs[i][j].tolist()))
                x, y, z = merge
                self.all_ax[i].plot(x, y, z, 'k->', color="black")

    def add_symbol(self):
        """
        Add all atoms to show in figure.

        Returns
        -------
        None : None

        """
        for i in range(4):
            ax = self.all_ax[i]
            ax.text(self.all_m[i][0] + 0.1,
                    self.all_m[i][1] + 0.1,
                    self.all_m[i][2] + 0.1,
                    f"{self.atom[0]}'", fontsize=9)

            for j in range(3):
                ax.text(self.all_c_ref[i][j][0] + 0.1,
                        self.all_c_ref[i][j][1] + 0.1,
                        self.all_c_ref[i][j][2] + 0.1,
                        f"{j + 1}", fontsize=9)

                ax.text(self.all_proj_ligs[i][j][0] + 0.1,
                        self.all_proj_ligs[i][j][1] + 0.1,
                        self.all_proj_ligs[i][j][2] + 0.1,
                        f"{j + 1}'", fontsize=9)

    def show_plot(self):
        """
        Show plot.

        Returns
        -------
        None : None

        """
        # plt.legend(bbox_to_anchor=(1.05, 1), loc=2)
        plt.tight_layout()
        plt.show()
