"""
Main module for plotting data
"""

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import matplotlib.pyplot as plt
import numpy as np

from utils import config
from utils import SWD
from utils import TT
from parser import TTParser
from parser import SWDParser

_SUPPORT_EXTENSIONS = ['TT', 'SWD']


class Plotter:
  """
  Basic plotting container for STELLAR simulation data
  Each holds single parser for specific file
  """

  def __init__(self, root):
    """
    @param root: project root
    """
    self._tt = TTParser(root)
    self._swd = SWDParser(root)
    self.mass = self._mass_coord()

    self.figs = {k: None for k in _SUPPORT_EXTENSIONS}
    self.axs = {k: None for k in _SUPPORT_EXTENSIONS}

  def plot_key(self, key, **kwargs):
    plot_config, text_config = config.build_configuration(key, **kwargs)
    if isinstance(key, SWD):
      self._plot_swd_data(key, plot_config, text_config)
    elif isinstance(key, TT):
      self._plot_tt_data(key, plot_config, text_config)

  def _mass_coord(self):
    mass = self._tt.stellar_info['MASS']
    log_mass = self._swd.mass
    return mass - np.power(10, log_mass)

  def _plot_swd_data(self, key, plot_config, text_config):
    if self._swd is None:
      raise ValueError('Must set swd parser')

    datas = self._swd.get_value_of_key(key)
    times = self._swd.times

    times, mass = np.meshgrid(times, self.mass)

    if self.figs['SWD'] is None:
      self.figs['SWD'] = plt.figure()
      self.axs['SWD'] = self.figs['SWD'].add_subplot(111)

    fig = self.figs['SWD']
    ax = self.axs['SWD']

    if plot_config['logx']:
      ax.set_xscale('log')
    if plot_config['logy']:
      ax.set_yscale('log')

    im = ax.contourf(times, mass, datas)
    fig.colorbar(im, ax=ax)
    self.__set_misc(ax, text_config)
    plt.show()

  def _plot_tt_data(self, key, plot_config, text_config):
    times = self._tt.get_time_range()
    value = self._tt.get_values(key)

    if plot_config['logx']:
      times = np.log10(times)
    if plot_config['logy']:
      value = np.log10(value)

    if self.figs['TT'] is None:
      self.figs['TT'] = plt.figure()
      self.axs['TT'] = self.figs['TT'].add_subplot(111)

    fig = self.figs['TT']
    ax = self.axs['TT']

    ax.plot(times, value)
    self.__set_misc(ax, text_config)
    plt.show()

  def __set_misc(self, ax, text_config):
    ax.set_title(text_config['title'])
    ax.set_xlabel(text_config['xlabel'])
    ax.set_ylabel(text_config['ylabel'])
