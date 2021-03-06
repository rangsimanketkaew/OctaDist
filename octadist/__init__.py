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

# Use TkAgg as MPL backend
# Note that IPython service such as Google Colab does not support TkAgg
try:
    import tkinter
    import matplotlib

    matplotlib.use("TkAgg")
except ImportError:
    pass

__author__ = "R. Ketkaew, Y. Tantirungrotechai, D. J. Harding, P. Harding, M. Marchivie"
__author_full__ = (
    "Rangsiman Ketkaew, Yuthana Tantirungrotechai, David J. Harding, "
    "Phimphaka Harding, Mathieu Marchivie"
)
__maintainer__ = "Rangsiman Ketkaew"
__copyright__ = "OctaDist  Copyright (C) 2019  Rangsiman Ketkaew et al."
__license__ = "GNU v3"
__credit__ = "OctaDist Development Team"
__email__ = "rangsiman1993@gmail.com"
__version__ = "2.6.1"
__revision__ = "2019.261"
__release__ = "August 2019"
__status__ = "stable"
__title__ = "Octahedral Distortion Calculator"
__description__ = (
    "OctaDist: A tool for calculating distortion parameters in coordination complexes."
)
__doc__ = "OctaDist documentation is available at https://octadist.readthedocs.io"
__help__ = "https://octadist.readthedocs.io"
__website__ = "https://octadist.github.io"
__github__ = "https://github.com/OctaDist/OctaDist"

__all__ = [
    "calc",
    "draw",
    "elements",
    "linear",
    "molecule",
    "plane",
    "plot",
    "popup",
    "projection",
    "structure",
    "tools",
    "util",
    # -----------------------
    "CalcDistortion",
    "DrawComplex",
    "DrawProjection",
    "DrawTwistingPlane",
    "check_atom",
    "check_radii",
    "check_color",
    "angle_sign",
    "angle_btw_vectors",
    "angle_btw_planes",
    "triangle_area",
    "count_line",
    "extract_coord",
    "find_metal",
    "extract_octa",
    "is_xyz",
    "is_gaussian",
    "is_nwchem",
    "is_orca",
    "is_qchem",
    "get_coord_xyz",
    "get_coord_gaussian",
    "get_coord_nwchem",
    "get_coord_orca",
    "get_coord_qchem",
    "find_eq_of_plane",
    "find_fit_plane",
    "Plot",
    "project_atom_onto_line",
    "project_atom_onto_plane",
    "DataComplex",
    "StructParam",
    "SurfaceArea",
    "CalcJahnTeller",
    "CalcRMSD",
    "find_bonds",
    "find_faces_octa",
]


# Bring sub-modules to top-level directory

from octadist import logo
from .logo import Icon_Base64

from octadist import src

from .src import __src__

from .src import calc
from .src import draw
from .src import elements
from .src import linear
from .src import molecule
from .src import plane
from .src import plot
from .src import popup
from .src import projection
from .src import structure
from .src import tools
from .src import util

# Bring function and method to top-level directory

from .src.calc import CalcDistortion

from .src.draw import DrawComplex
from .src.draw import DrawProjection
from .src.draw import DrawTwistingPlane

from .src.elements import check_atom
from .src.elements import check_radii
from .src.elements import check_color

from .src.linear import angle_sign
from .src.linear import angle_btw_vectors
from .src.linear import angle_btw_planes
from .src.linear import triangle_area

from .src.molecule import count_line
from .src.molecule import extract_coord
from .src.molecule import find_metal
from .src.molecule import extract_octa
from .src.molecule import is_xyz
from .src.molecule import is_gaussian
from .src.molecule import is_nwchem
from .src.molecule import is_orca
from .src.molecule import is_qchem
from .src.molecule import get_coord_xyz
from .src.molecule import get_coord_gaussian
from .src.molecule import get_coord_nwchem
from .src.molecule import get_coord_orca
from .src.molecule import get_coord_qchem

from .src.plane import find_eq_of_plane
from .src.plane import find_fit_plane

from .src.plot import Plot

from .src.projection import project_atom_onto_line
from .src.projection import project_atom_onto_plane

from .src.structure import DataComplex
from .src.structure import StructParam
from .src.structure import SurfaceArea

from .src.tools import CalcJahnTeller
from .src.tools import CalcRMSD

from .src.util import find_bonds
from .src.util import find_faces_octa

