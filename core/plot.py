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
    self._mrt_time, self._mrt_mass = self._get_mrt_mesh_grid()
    self._tt = tt

    self._figsize = figsize

  @property
  def times(self):
    return self._mrt_time

  @property
  def mass(self):
    return self._mrt_mass

  def _get_mrt_mesh_grid(self):
    times = self._mrt.get_time_range()
    mass = self._mrt.get_mass_coordinate()

    return tuple(np.meshgrid(times, mass))

  def plot_key(self, key, log_time=True, log_value=True):
    value = self._mrt.get_value_of_key(key)
    value = ma.masked_where(value <= 0, value)
    plt.figure()
    plt.contour(self.times, self.mass, value, locator=ticker.LogLocator())
    plt.colorbar()
    plt.xscale('log')
    plt.show()
    pass
