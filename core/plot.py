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
from utils import MRT
from utils import ABN
from parser import TTParser
from parser import SWDParser
from parser import ABNParser
from parser.mrt import MRTParser

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
    self._mrt = MRTParser(root)
    self._abn = ABNParser(root)
    self.mass = self._mass_coord()
    self.photosphere = self._photosphere()

    self.fig = None
    self.ax1 = None
    self.ax2 = None

  def plot_key(self, key, **kwargs):
    plot_config, text_config = config.build_configuration(key, **kwargs)
    if isinstance(key, SWD):
      self._plot_swd_data(key, plot_config, text_config)
    elif isinstance(key, TT):
      self._plot_tt_data(key, plot_config, text_config)

  def _photosphere(self):

    def findClosest(arr, n, target, return_idx=False):
      if (target <= arr[0]):
        if return_idx:
          return 0
        else:
          return arr[0]
      if (target >= arr[n - 1]):
        if return_idx:
          return n - 1
        else:
          return arr[n - 1]

      # Doing binary search
      i = 0
      j = n
      mid = 0
      while (i < j):
        mid = (i + j) // 2

        if (arr[mid] == target):
          if return_idx:
            return mid
          else:
            return arr[mid]

        # If target is less than array
        # element, then search in left
        if (target < arr[mid]):

          # If target is greater than previous
          # to mid, return closest of two
          if (mid > 0 and target > arr[mid - 1]):
            if target - arr[mid - 1] >= arr[mid] - target:
              if return_idx:
                return mid
              else:
                return arr[mid]
            else:
              if return_idx:
                return mid - 1
              else:
                return arr[mid - 1]

          # Repeat for left half
          j = mid

        # If target is greater than mid
        else:
          if (mid < n - 1 and target < arr[mid + 1]):
            if target - arr[mid] >= arr[mid + 1] - target:
              if return_idx:
                return mid + 1
              else:
                return arr[mid + 1]
            else:
              if return_idx:
                return mid
              else:
                return arr[mid]

          i = mid + 1
      # Only single element left after search
      if return_idx:
        return mid
      else:
        return arr[mid]

    #  calculate photosphere radius
    r_taus = np.log10(self._tt.get_values(TT.R))
    r_tau_mass = []
    tt_times = self._tt.get_time_range()
    swd_times = self._swd.times
    swd_time2idx = self._swd.time2idx

    # closest time corresponding from tt_time to swd_time
    closest_time = np.array(
        list(
            map(lambda x: findClosest(swd_times, len(swd_times), x),
                tt_times)))

    for r_tau, time in zip(r_taus, closest_time):
      swd_time_data = self._swd.data[swd_time2idx[time], :, config.SWD2IDX[SWD.
                                                                           R]]
      idx = findClosest(swd_time_data, len(swd_time_data), r_tau, True)
      r_tau_mass.append(self.mass[idx])

    return np.array(r_tau_mass)

  def _mass_coord(self):
    mass = self._tt.stellar_info['MASS']
    log_mass = self._swd.mass
    return mass - np.power(10, log_mass)

  def _plot_swd_data(self, key, plot_config, text_config):
    if self._swd is None:
      raise ValueError('Must set swd parser')

    datas = self._swd.get_value_of_key(key)
    l_times = self._swd.times  # linear times

    times, mass = np.meshgrid(l_times, self.mass)

    if self.fig is None:
      self.fig = plt.figure()
      self.ax1 = plt.subplot2grid((6, 6), (0, 0), rowspan=3, colspan=6)
      self.ax2 = plt.subplot2grid((6, 6), (4, 0), rowspan=2, colspan=6)

    fig = self.fig
    ax1 = self.ax1
    ax2 = self.ax2

    if plot_config['logx']:
      ax1.set_xscale('log')
    if plot_config['logy']:
      ax1.set_yscale('log')

    H_low, H_high = self._abn.get_element_data(ABN.H)

    im = ax1.contourf(times, mass, datas)
    ax1.plot(self._tt.get_time_range(), self.photosphere)
    ax1.plot(
        l_times, np.ones_like(l_times) * self.mass[H_low + 1], color='red')
    ax1.text(
        l_times[int(l_times.shape[0] * 0.95)],
        self.mass[H_low + 1] + 0.01,
        'H > 0.1',
        color='red')
    ax1.set_xlim(l_times[0], l_times[-1])
    fig.colorbar(im, ax=ax1)
    self.__set_misc(ax1, text_config)

    # plot related to magnitue
    tt_times = self._tt.get_time_range()
    ax2.plot(tt_times, self._tt.get_values(TT.MBOL), label='Mbol')
    ax2.plot(tt_times, self._tt.get_values(TT.MU), label='MU')
    ax2.plot(tt_times, self._tt.get_values(TT.MV), label='MV')
    ax2.plot(tt_times, self._tt.get_values(TT.MB), label='MB')
    ax2.plot(tt_times, self._tt.get_values(TT.MI), label='MI')
    ax2.plot(tt_times, self._tt.get_values(TT.MR), label='MR')
    ax2.legend(
        loc='upper center',
        bbox_to_anchor=(0.5, 1.05),
        ncol=3,
        fancybox=True,
        shadow=True,
        fontsize=12)
    ax2.set_xlabel('t')
    ax2.set_ylabel('Magnitude')
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
