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

__src__ = "source code"

import tkinter as tk


def echo_outs(self, text):
    """
    Insert text to result box

    Parameters
    ----------
    self : object
        Class object reference.
    text : str
        Text to show in result box.

    Returns
    -------
    None : None

    """
    self.box_result.insert(tk.INSERT, text + "\n")
    self.box_result.see(tk.END)
