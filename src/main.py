"""
OctaDist  Copyright (C) 2019  Rangsiman Ketkaew

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

----------------------------------------------------------------------

OctaDist version 2.0

Octahedral Distortion Analysis
Software website: www.github.com/rangsimanketkaew/octadist
Last modified: January 2018

This program, we use Python 3.7.2 and TkInter as GUI maker.
PyInstaller is used as executable compiler.
Written and tested on PyCharm 2018.3.3 (Community Edition) program

Author: Rangsiman Ketkaew
        Computational Chemistry Research Unit
        Department of Chemistry
        Faculty of Science and Technology
        Thammasat University, Pathum Thani, 12120 Thailand
Contact: rangsiman1993@gmail.com
         rangsiman_k@sci.tu.ac.th
Personal website: https://sites.google.com/site/rangsiman1993
"""

program_version = 2.0

import numpy as np
import datetime

import popup
import coord
import plane
import proj
import calc

from tkinter import *
from tkinter import filedialog

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


class OctaDist:

    def __init__(self, masters):
        self.masters = masters
        masters.title("OctaDist")
        FONT = "Arial 10"
        self.masters.option_add("*Font", FONT)
        master = Frame(masters, width="2", height="2")
        master.grid(padx=5, pady=5, row=0, column=0)

        """
        Create menu bar
            File
            |- New                        << clear_cache
            |- Open                       << open_file
            |- Open multiple files        << open_multiple
            |- Save as ..                 << save_file
            |-------------
            |- Exit                       << quit_program
            Tools
            |- Show structural parameters << structure_param
            Help
            |- Program help               << help
            |- About program              << about
            |- License info               << license
        """

        menubar = Menu(masters)
        # add menu bar button
        filemenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=filemenu)

        # sub-menu
        filemenu.add_command(label="New", command=self.clear_cache)
        filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_command(label="Open multiple files", command=self.open_multiple)
        filemenu.add_command(label="Save as ..", command=self.save_file)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.masters.quit)

        # add menu bar button
        toolsmenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=toolsmenu)

        # add sub-menu
        toolsmenu.add_command(label="Show structural parameters")

        # add menu bar button
        helpmenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=helpmenu)

        # add sub-menu
        helpmenu.add_command(label="Program help", command=popup.help)
        helpmenu.add_command(label="About program", command=popup.about)
        helpmenu.add_command(label="License information", command=popup.license)
        masters.config(menu=menubar)

        popup.welcome()

        # program details
        program_name = "Octahedral Distortion Analysis"
        self.msg_1 = Label(master, foreground="blue", font=("Arial", 16, "bold"), text=program_name)
        self.msg_1.config()
        self.msg_1.grid(pady="5", row=0, columnspan=4)
        description = "Determine the structural distortion between two octahedral structures."
        self.msg_2 = Label(master, text=description)
        self.msg_2.grid(pady="5", row=1, columnspan=4)

        # button to browse input file
        self.btn_open_file = Button(master, command=self.open_file, text="Browse file", relief=RAISED)
        self.btn_open_file.grid(pady="5", row=2, column=0)

        # button to run
        self.btn_run = Button(master, command=self.calc_all_param, text="Compute parameters")
        # btn_run.config(font="Segoe 10")
        self.btn_run.grid(sticky=W, pady="5", row=2, column=1, columnspan=2)

        # button to clear cache
        self.btn_open_file = Button(master, command=self.clear_cache, text="Clear cache", )
        self.btn_open_file.grid(sticky=W, pady="5", row=2, column=3)

        # coordinate label
        self.lbl_1 = Label(master, text="Molecule Specifications")
        self.lbl_1.grid(sticky=W, pady="5", row=3, columnspan=4)

        # text box for showing cartesian coordinates
        self.textBox_coord = Text(master, height="14", width="65", wrap="word")
        self.textBox_coord.grid(pady="5", row=4, columnspan=4)

        # Octahedral distortion parameters
        self.lbl_2 = Label(master, text="Octahedral distortion parameters")

        # lbl_2.config(font="Segoe 10 bold")
        self.lbl_2.grid(row=6, column=1, columnspan=2)

        # Display coordinate and vector projection
        self.lbl_display = Label(master, text="Graphical Displays")
        # self.lbl_display.config(font="Segoe 10 bold")
        self.lbl_display.grid(row=6, column=0, padx="30")

        # button to draw structure
        self.btn_draw_structure = Button(master, command=self.display_structure, text="Octahedral structure", width="18")
        self.btn_draw_structure.grid(pady="5", row=7, column=0)

        # button to draw plane
        self.btn_draw_plane = Button(master, command=self.display_2D_plane, text="Twisting triangular faces", width="18")
        self.btn_draw_plane.grid(pady="5", row=8, column=0)

        # button to draw vector projection
        self.btn_draw_projection = Button(master, command=self.display_3D_plane, text="3D Projection planes", width="18")
        self.btn_draw_projection.grid(pady="5", row=9, column=0)

        # Delta
        self.lbl_dist = Label(master, text="Δ  = ")
        self.lbl_dist.grid(sticky=E, pady="5", row=7, column=1)
        self.textBox_delta = Text(master, height="1", width="15", wrap="word")
        self.textBox_delta.grid(row=7, column=2, sticky=W)

        # Sigma
        self.lbl_sigma = Label(master, text="Σ  = ")
        self.lbl_sigma.grid(sticky=E, pady="5", row=8, column=1)
        self.textBox_sigma = Text(master, height="1", width="15", wrap="word")
        self.textBox_sigma.grid(sticky=W, row=8, column=2)
        self.lbl_sigma_unit = Label(master, text="degree")
        self.lbl_sigma_unit.grid(sticky=W, pady="5", row=8, column=3)

        # Theta
        self.lbl_theta = Label(master, text="Θ  = ")
        self.lbl_theta.grid(sticky=E, pady="5", row=9, column=1)
        self.textBox_theta = Text(master, height="1", width="15", wrap="word")
        self.textBox_theta.grid(sticky=W, row=9, column=2)
        self.lbl_theta_unit = Label(master, text="degree")
        self.lbl_theta_unit.grid(sticky=W, pady="5", row=9, column=3)

        # Link
        link = "https://github.com/rangsimanketkaew/OctaDist"
        self.lbl_link = Label(master, foreground="blue", text=link, cursor="hand2")
        self.lbl_link.grid(pady="5", row=10, columnspan=4)
        self.lbl_link.bind("<Button-1>", popup.callback)

    def clear_cache(self):
        """Clear all variables
        """
        global file_name, file_data, atom_list, coord_list, mult

        print("Command: Clear cache")

        file_name = ""
        file_data = ""
        atom_list = []
        coord_list = []
        mult = 0

        for name in dir():
            if not name.startswith('_'):
                del locals()[name]

        self.textBox_coord.delete(1.0, END)
        self.textBox_delta.delete(1.0, END)
        self.textBox_sigma.delete(1.0, END)
        self.textBox_theta.delete(1.0, END)

        self.clear_results()

    def clear_results(self):
        """Clear the computed parameters
        """
        global computed_delta, computed_sigma, computed_theta

        computed_delta = 0.0
        computed_sigma = 0.0
        computed_theta = 0.0

        self.textBox_delta.delete(1.0, END)
        self.textBox_sigma.delete(1.0, END)
        self.textBox_theta.delete(1.0, END)

    def open_file(self):
        """Open file using Open Dialog
        Atom and coordinates must be in Cartesian (XYZ) coordinate.
        Supported file extensions: .txt, .xyz, and Gaussian output file
        """
        global file_name, file_data, atom_list, coord_list, full_atom_list, full_coord_list

        print("Command: Open input file")

        if file_name != "":
            self.clear_cache()

        file_name = filedialog.askopenfilename(# initialdir="C:/Users/",
            title="Choose input file",
            filetypes=(("XYZ File", "*.xyz"),
                       ("Text File", "*.txt"),
                       ("Gaussian Output File", "*.out"),
                       ("Gaussian Output File", "*.log"),
                       ("NWChem Output File", "*.out"),
                       ("NWChem Output File", "*.log"),
                       ("ORCA Output File", "*.out"),
                       ("ORCA Output File", "*.log"),
                       ("All Files", "*.*")))

        # Using try/except in case user types in unknown file or closes without choosing a file.
        try:
            with open(file_name, 'r') as f:
                print("         File full path: " + file_name)
                print("         File name: " + file_name.split('/')[-1])
                f.close()

                # Check file type and get coordinate
                print("")
                print("Command: Determine file type")
                full_atom_list, full_coord_list = coord.get_coord(file_name)

                if len(full_coord_list) != 0:
                    atom_list, coord_list = coord.cut_coord(full_atom_list, full_coord_list)
                else:
                    return 1

                texts = "File: {0}\n\n" \
                        "Atom                       Cartesian coordinate".format(file_name.split('/')[-1])
                self.textBox_coord.insert(INSERT, texts)

                for i in range(len(atom_list)):
                    texts = " {A:>2}      {Lx:14.9f}  {Ly:14.9f}  {Lz:14.9f}" \
                            .format(file_name, A=atom_list[i],
                            Lx=coord_list[i][0], Ly=coord_list[i][1], Lz=coord_list[i][2])
                    self.textBox_coord.insert(END, "\n" + texts)

                return atom_list, coord_list
        except:
            print("Error: No input file")
            atom_list, coord_list = 0, 0

            return atom_list, coord_list

    def open_multiple(self):
        """Open multiple input files
        """
        global list_file, mult

        print("Command: Open multiple files")

        if list_file != "":
            self.clear_cache()

        file_name = filedialog.askopenfilenames(# initialdir="C:/Users/",
            title="Choose input file",
            filetypes=(("XYZ File", "*.xyz"),
                       ("Text File", "*.txt"),
                       ("Gaussian Output File", "*.out"),
                       ("Gaussian Output File", "*.log"),
                       ("NWChem Output File", "*.out"),
                       ("NWChem Output File", "*.log"),
                       ("ORCA Output File", "*.out"),
                       ("ORCA Output File", "*.log"),
                       ("All Files", "*.*")))

        list_file = list(file_name)

        try:
            open(file_name[0], 'r')
            mult = 1

            texts = "< Open multiple files >\n< Open multiple files >\n< Open multiple files >"
            self.textBox_coord.insert(INSERT, texts)

            print("Command: %s input files selected" % len(list_file))
            for i in range(len(list_file)):
                print("         File {0:2d} : \"{1}\"".format(i + 1, list_file[i]))
            print("")
        except:
            print("Error: No input file")

    def save_file(self):
        """Save file using Save Dialog. The result will be saved into .txt or .out file.
        """
        print("Command: Save data to output file")

        if file_name == "":
            popup.nofile_error()
            return 1
        if run_check == 0:
            popup.nocalc_error()
            return 1

        f = filedialog.asksaveasfile(mode='w',
                                     defaultextension=".out",
                                     title="Save as",
                                     filetypes=(("Text File", "*.txt"),
                                                ("Output File", "*.out"),
                                                ("All Files", "*.*")))

        if f is None:
            print("Warning: Cancelled save file")
            return 0

        f.write("OctaDist  Copyright (C) 2019  Rangsiman Ketkaew\n")
        f.write("This program comes with ABSOLUTELY NO WARRANTY; for details, go to Help/License.\n")
        f.write("This is free software, and you are welcome to redistribute it under\n")
        f.write("certain conditions; see <https://www.gnu.org/licenses/> for details.\n\n")
        f.write("OctaDist {}: Octahedral Distortion Analysis\n".format(program_version))
        f.write("https://github.com/rangsimanketkaew/OctaDist\n\n")
        f.write("By Rangsiman Ketkaew\n")
        f.write("Computational Chemistry Research Unit\n")
        f.write("Department of Chemistry, Faculty of Science and Technology\n")
        f.write("Thammasat University, Pathum Thani, 12120 Thailand\n")
        f.write("E-mail: rangsiman1993@gmail.com\n\n")
        f.write("================== Output file ==================\n\n")
        f.write("Date: Saved on {}\n\n".format(datetime.datetime.now()))
        f.write("Input file: " + file_name + "\n\n")
        f.write("Molecular specification of Octahedral structure\n")
        f.write("Atom list:\n")
        for item in atom_list:
            f.write("%s  " % item)
        f.write("\n\n")
        f.write("Coordinate list:\n")
        for item in coord_list:
            f.write("%s\n" % item)
        f.write("\n")
        f.write("Distance between atoms:\n")
        for item in distance_list:
            f.write("Distance --> %5.6f Angstrom\n" % item)
        f.write("\n")
        f.write("Angle of three cis atoms (metal center is vertex):\n")
        for item in new_angle_sigma_list:
            f.write("Angle --> %5.6f degree\n" % item)
        f.write("\n")
        f.write("The Theta parameter for each orthogonal plane:\n")
        for item in computed_theta_list:
            f.write("Angle --> %5.6f degree\n" % item)
        f.write("\n")
        f.write("Octahedral distortion parameters:\n")
        f.write(" - Delta = {0:5.10f}\n".format(computed_delta))
        f.write(" - Sigma = {0:5.10f} degree\n".format(computed_sigma))
        f.write(" - Theta = {0:5.10f} degree\n".format(computed_theta))
        f.write("\n\n")
        f.write("============ End of the output file. ============\n\n")
        f.close()

        print("Command: Data has been saved to ", f)

    def calc_all_param(self):
        """Calculate octahedral distortion parameters
        """
        global run_check, computed_delta, computed_sigma, computed_theta
        global distance_list, new_angle_sigma_list, computed_theta_list
        global ref_pal, ref_pcl, oppo_pal, oppo_pcl

        if mult == 1:
            self.clear_results()
            calc.calc_mult(list_file)
            return 0

        if file_name == "":
            popup.nofile_error()
            return 1

        run_check = 1
        self.clear_results()

        if np.any(coord_list) != 0:
            print("Command: Calculate octahedral distortion parameters")
            computed_delta, distance_list = calc.calc_delta(coord_list)
            computed_sigma, new_angle_sigma_list = calc.calc_sigma(coord_list)
            computed_theta, computed_theta_list, selected_plane_lists = calc.calc_theta(coord_list)

            ref_pal, ref_pcl, oppo_pal, oppo_pcl = selected_plane_lists

            print("Command: Show computed octahedral distortion parameters")
            print("")
            print("         Δ = {0:11.6f}".format(computed_delta))
            print("         Σ = {0:11.6f} degree".format(computed_sigma))
            print("         Θ = {0:11.6f} degree".format(computed_theta))
            print("")

            self.textBox_delta.insert(INSERT, '%3.6f' % computed_delta)
            self.textBox_sigma.insert(INSERT, '%3.6f' % computed_sigma)
            self.textBox_theta.insert(INSERT, '%3.6f' % computed_theta)

        else:
            popup.nocoord_error()

    def display_structure(self):
        """Display 3D structure of octahedral complex with label for each atoms
        """
        if file_name == "":
            popup.nofile_error()
            return 1
        if mult == 1:
            popup.nosupport_mult()
            return 1

        print("Command: Display octahedral structure")

        # Plot and configuration
        fig = plt.figure()
        ax = Axes3D(fig)
        cl = coord_list

        # Plot metal center
        ax.scatter(cl[0][0], cl[0][1], cl[0][2], color='yellow', marker='o', s=300, linewidths=2, edgecolors='black')
        ax.text(cl[0][0] + 0.1, cl[0][1] + 0.1, cl[0][2] + 0.1, atom_list[0], fontsize=12)

        # Plot ligand atoms
        for i in range(1, 7):
            ax.scatter(cl[i][0], cl[i][1], cl[i][2], color='red', marker='o', s=200, linewidths=2, edgecolors='black')
            ax.text(cl[i][0] + 0.1, cl[i][1] + 0.1, cl[i][2] + 0.1, "{0},{1}".format(atom_list[i], i), fontsize=10)

        ax.set_xlabel(r'X', fontsize=15)
        ax.set_ylabel(r'Y', fontsize=15)
        ax.set_zlabel(r'Z', fontsize=15)
        ax.set_title('Octahedral structure', fontsize="12")
        ax.grid(True)

        # plt.axis('equal')
        plt.show()
    
    def display_2D_plane(self):
        """Display twisting triangular faces vector projection of all atoms onto the given plane
        """
        if file_name == "":
            popup.nofile_error()
            return 1
        if mult == 1:
            popup.nosupport_mult()
            return 1
        if run_check == 0:
            popup.nocalc_error()
            return 1

        print("Command: Display the selected 4 twisting triangular faces")

        al, cl, vl, ovl = atom_list, coord_list, ref_pcl, oppo_pcl

        fig = plt.figure()

        for i in range(4):
            a, b, c, d = plane.eq_of_plane(vl[i][0], vl[i][1], vl[i][2])
            m = proj.project_atom_onto_plane(cl[0], a, b, c, d)

            ax = fig.add_subplot(2, 2, int(i + 1), projection='3d')
            ax.set_title("Orthogonal projection onto the plane {0}".format(i + 1), fontsize='10')

            # Projected Metal center atom
            ax.scatter(m[0], m[1], m[2], color='orange', marker='o', s=100, linewidths=1,
                       edgecolors='black', label="Projected metal center")
            ax.text(m[0] + 0.1, m[1] + 0.1, m[2] + 0.1, "{}'".format(al[0]), fontsize=9)

            l = []

            for k in range(3):
                # Reference ligand atoms
                ax.scatter(vl[i][k][0], vl[i][k][1], vl[i][k][2], color='red', marker='o', s=50, linewidths=1,
                           edgecolors='black', label="Ligand atom")
                ax.text(vl[i][k][0] + 0.1, vl[i][k][1] + 0.1, vl[i][k][2] + 0.1, "{0}".format(k), fontsize=9)
                # Projected Ligand atom
                l.append(proj.project_atom_onto_plane(ovl[i][k], a, b, c, d))

                print(l[k])

            for k in range(3):
                ax.scatter(l[k][0], l[k][1], l[k][2], color='blue', marker='o', s=50, linewidths=1,
                           edgecolors='black', label="Projected ligand atom")
                ax.text(l[k][0] + 0.1, l[k][1] + 0.1, l[k][2] + 0.1, "{0}".format(k + 1), fontsize=9)

            ax.set_xlabel(r'X', fontsize=10)
            ax.set_ylabel(r'Y', fontsize=10)
            ax.set_zlabel(r'Z', fontsize=10)
            ax.grid(True)

        # ax.legend()

        # Draw line
        # x, y, z = [], [], []
        # for i in range(1, 7):
        #     x.append(cl[i][0])
        #     y.append(cl[i][1])
        #     z.append(cl[i][2])
        # ax.plot(x, y, z, 'k-')

        # plt.axis('equal')
        plt.show()

    def display_3D_plane(self):
        """Display the selected 4 faces of octahedral complex
        """
        if file_name == "":
            popup.nofile_error()
            return 1
        if mult == 1:
            popup.nosupport_mult()
            return 1
        if run_check == 0:
            popup.nocalc_error()
            return 1

        print("Command: Display the selected 4 pairs of opposite faces")

        al, cl, vl = atom_list, coord_list, ref_pcl
        vertex_list = []
        color_list = ["red", "blue", "green", "yellow"]

        ##########################################################
        # This function is hard coding. Waiting for improvement
        ##########################################################

        plane_1_x, plane_1_y, plane_1_z = [], [], []
        plane_2_x, plane_2_y, plane_2_z = [], [], []
        plane_3_x, plane_3_y, plane_3_z = [], [], []
        plane_4_x, plane_4_y, plane_4_z = [], [], []

        for i in range(3):
            plane_1_x.append(vl[0][i][0])
            plane_1_y.append(vl[0][i][1])
            plane_1_z.append(vl[0][i][2])
        for i in range(3):
            plane_2_x.append(vl[1][i][0])
            plane_2_y.append(vl[1][i][1])
            plane_2_z.append(vl[1][i][2])
        for i in range(3):
            plane_3_x.append(vl[2][i][0])
            plane_3_y.append(vl[2][i][1])
            plane_3_z.append(vl[2][i][2])
        for i in range(3):
            plane_4_x.append(vl[3][i][0])
            plane_4_y.append(vl[3][i][1])
            plane_4_z.append(vl[3][i][2])

        vertex_set_1 = [list(zip(plane_1_x, plane_1_y, plane_1_z))]
        vertex_set_2 = [list(zip(plane_2_x, plane_2_y, plane_2_z))]
        vertex_set_3 = [list(zip(plane_3_x, plane_3_y, plane_3_z))]
        vertex_set_4 = [list(zip(plane_4_x, plane_4_y, plane_4_z))]

        vertex_list.append(vertex_set_1)
        vertex_list.append(vertex_set_2)
        vertex_list.append(vertex_set_3)
        vertex_list.append(vertex_set_4)

        fig = plt.figure()

        # Display four planes
        for i in range(4):
            ax = fig.add_subplot(2, 2, int(i + 1), projection='3d')
            ax.set_title("Plane {}".format(i + 1))
            ax.scatter(cl[0][0], cl[0][1], cl[0][2],
                       color='yellow', marker='o', s=100, linewidths=1, edgecolors='black')
            ax.text(cl[0][0] + 0.1, cl[0][1] + 0.1, cl[0][2] + 0.1, al[0], fontsize=9)

            for j in range(1, 7):
                ax.scatter(cl[j][0], cl[j][1], cl[j][2],
                           color='red', marker='o', s=50, linewidths=1, edgecolors='black')
                ax.text(cl[j][0] + 0.1, cl[j][1] + 0.1, cl[j][2] + 0.1,
                        "{0},{1}".format(al[j], j), fontsize=9)

            # Draw plane
            ax.add_collection3d(Poly3DCollection(vertex_list[i], alpha=0.5, color=color_list[i]))

            ax.set_xlabel(r'X', fontsize=10)
            ax.set_ylabel(r'Y', fontsize=10)
            ax.set_zlabel(r'Z', fontsize=10)
            ax.grid(True)

        # plt.axis('equal')
        plt.show()


def main():
    masters = Tk()
    MainProgram = OctaDist(masters)

    global file_name, file_data, list_file, run_check, mult
    file_name = ""
    file_data = ""
    list_file = ""
    run_check = 0
    mult = 0

    # activate program windows
    masters.mainloop()


if __name__ == '__main__':
    main()
