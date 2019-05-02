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

from utils.config import SWD, TT
from parser.mrt import MRTParser
from parser.tt import TTParser
from parser.swd import SWDParser


class Plotter:
  """
  Basic plotting container for STELLAR simulation data
  Each holds single parser for specific file
  """

  def __init__(self, root, figsize=(6, 4)):
    """
    @param root: project root
    """
    self._tt = TTParser(root)
    self._swd = SWDParser(root)
    self.mass = self._mass_coord()

    self._figsize = figsize
    self._fig = None
    self._ax = None
    self._plot_config = {}

  def plot_key(self, key, **kwargs):
    if isinstance(key, SWD):
      self._plot_swd_data(key, **kwargs)
    elif isinstance(key, TT):
      self._plot_tt_data(key, **kwargs)

  def _mass_coord(self):
    mass = self._tt.stellar_info['MASS']
    log_mass = self._swd.mass
    return mass - np.power(10, log_mass)

  def _plot_swd_data(self, key, **kwargs):
    if self._swd is None:
      raise ValueError('Must set swd parser')

    logx = kwargs.get('logx', False)
    logy = kwargs.get('logy', False)

    datas = self._swd.get_value_of_key(key)
    times = self._swd.times

    times, mass = np.meshgrid(times, self.mass)

    if self._fig is None:
      self._fig = plt.figure()
      self._ax = self._fig.add_subplot(111)

    if logx:
      self._ax.set_xscale('log')
    if logy:
      self._ax.set_yscale('log')

    # plot setting
    ax_dict = {
        'title': str(key).split('.')[-1],
        'xlabel': 't',
        'ylabel': 'M',
    }
    self._ax.contour(times, mass, datas)
    self.__set_misc(**ax_dict)

  def _plot_tt_data(self, key, **kwargs):
    times = self._tt.get_time_range()
    value = self._tt.get_values(key)

    logx = kwargs.get('logx', False)
    logy = kwargs.get('logy', False)

    if logx:
      times = np.log10(times)
    if logy:
      value = np.log10(value)

    if self._fig is None:
      self._fig = plt.figure()
      self._ax = self._fig.add_subplot(111)

    ax_dict = {
        'title': str(key).split('.')[-1],
        'xlabel': 't',
        'ylabel': 'value',
    }
    self._ax.plot(times, value)
    self.__set_misc(**ax_dict)

  def __set_misc(self, **kwargs):
    title = kwargs.get('title', '')
    xlabel = kwargs.get('xlabel', '')
    ylabel = kwargs.get('ylabel', '')
    self._ax.set_title(title)
    self._ax.set_xlabel(xlabel)
    self._ax.set_ylabel(ylabel)
    pass
