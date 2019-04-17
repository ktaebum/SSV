"""
Main module for plotting data
"""

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import matplotlib.pyplot as plt
import numpy as np

from matplotlib import ticker
from numpy import ma

from utils.config import MRT_TABLE_LABELS, TT_TABLE_LABELS


class Plotter:
  """
  Basic plotting container for STELLAR simulation data
  Each holds single parser for specific file
  """

  def __init__(self, mrt=None, tt=None, figsize=(6, 4)):
    """
    @param mrt: MRTParser
    @param tt: TTParser
    """
    self._mrt = mrt
    self._tt = tt

    self._label2parser = {}
    for key in MRT_TABLE_LABELS:
      self._label2parser[key] = self._mrt
    for key in TT_TABLE_LABELS:
      self._label2parser[key] = self._tt

    self._figsize = figsize
    self._fig = None
    self._ax = None
    self._plot_config = {}

  def _get_mrt_mesh_grid(self):
    times = self._mrt.get_time_range()
    mass = self._mrt.get_mass_coordinate()

    return tuple(np.meshgrid(times, mass))

  def plot_key(self, key, log_x=False, log_y=False):
    parser = self._label2parser.get(key, None)

    if parser is None:
      raise KeyError('Non-existing data key %s' % key)

    times = parser.get_time_range()
    value = parser.get_values(key)

    if log_x:
      times = np.log10(times)
    if log_y:
      value = np.log10(value)

    if self._fig is None:
      self._fig = plt.figure()
      self._ax = self._fig.add_subplot(111)

    self._ax.plot(times, value)
    plt.show()
    pass
