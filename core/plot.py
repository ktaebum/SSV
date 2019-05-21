"""
Main module for plotting data
"""

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import warnings

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

from utils import config
from utils import SWD
from utils import TT
from utils import ABN
from parser import TTParser
from parser import SWDParser
from parser import ABNParser

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
    #  self._mrt = MRTParser(root)
    self._abn = ABNParser(root)
    self.tot_mass = self._tt.stellar_info['MASS']
    self.mass = self._mass_coord()
    self.photosphere = self._photosphere()

    self.fig = None
    self.ax1 = None
    self.ax2 = None

    self.colors = []
    self.__fill_colors()

  def plot(self, key, **kwargs):
    """ Main plot function
    """
    plot_config, text_config = config.build_configuration(key, **kwargs)

    data = self._swd.get_value_of_key(key)
    if data is None:
      warnings.warn('Cannot retreive key %s' % str(key))
      return

    time_vector = self._swd.times
    if plot_config['log_mass']:
      mass_vector = self._swd.mass
    else:
      mass_vector = self.mass

    #  build mesh grid
    times, mass = np.meshgrid(time_vector, mass_vector)

    if self.fig is None:
      self.fig = plt.figure()
      if plot_config['magnitude']:
        self.ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=8, colspan=12)
        self.ax2 = plt.subplot2grid((12, 12), (9, 0), rowspan=3, colspan=12)
        self._plot_magnitude()
      else:
        self.ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=12, colspan=12)
        self.ax2 = None

    fig = self.fig
    ax = self.ax1

    if plot_config['log_time']:
      ax.set_xscale('log')
    if plot_config['log_mass']:
      ax.invert_yaxis()

    contour = ax.contourf(times, mass, data, alpha=0.6)
    if plot_config['photosphere']:
      self.__fill_colors()

      if plot_config['log_mass']:
        ax.plot(
            self._tt.times,
            np.log10(self.tot_mass - self.photosphere),
            color=self.colors.pop(),
            label='photosphere')
      else:
        ax.plot(
            self._tt.times,
            self.photosphere,
            color=self.colors.pop(),
            label='photosphere')

    ax.set_xlim(time_vector[0], time_vector[-1])
    if not plot_config['log_mass']:
      ax.set_ylim(mass_vector[0], self.tot_mass)
    fig.colorbar(contour, ax=ax)

    ax.set_title(text_config['title'])
    if plot_config['log_mass']:
      ax.set_ylabel(r'$\log{(M_{tot} - M_{r})}$')
    else:
      ax.set_ylabel(r'$M_{r}$')
    ax.set_xlabel('t')
    ax.legend()

  def plot_abn_data(self, key, ratio=0.1, **kwargs):
    if self.ax1 is None:
      return

    if not isinstance(key, (ABN, tuple)):
      return

    if isinstance(key, ABN):
      name = str(key).split('.')[-1]
    elif isinstance(key, tuple):
      name = ' + '.join(list(map(lambda x: str(x).split('.')[-1], key)))

    plot_config, text_config = config.build_configuration(key, **kwargs)
    d_low, d_high = self._abn.get_element_data(key, ratio)

    if d_low == -1 and d_high == -1:
      # warning and return
      warnings.warn('Cannot plot for %s > %1.1f' % (name, ratio))
      return

    time_vector = self._swd.times

    if plot_config['log_mass']:
      mass_low = np.log10(self.tot_mass - self.mass[d_low])
      mass_high = np.log10(self.tot_mass - self.mass[d_high])
    else:
      mass_low = self.mass[d_low]
      mass_high = self.mass[d_high]

    self.__fill_colors()
    color = self.colors.pop()

    ax = self.ax1
    ax.plot(
        time_vector,
        np.ones_like(time_vector) * mass_low,
        color=color,
        label='%s > %1.1f' % (name, ratio),
        linewidth=3,
    )
    ax.plot(
        time_vector,
        np.ones_like(time_vector) * mass_high,
        color=color,
        linewidth=3,
    )
    ax.legend(
        loc='upper right',
        shadow=True,
        bbox_to_anchor=(1.4, 1.0),
        fontsize=12,
    )

  def _plot_magnitude(self):
    ax = self.ax2
    times = self._tt.times
    bol = self._tt.get_values(TT.MBOL)
    ax.plot(times, self._tt.get_values(TT.MBOL), label='Mbol')
    ax.plot(times, self._tt.get_values(TT.MU), label='MU')
    ax.plot(times, self._tt.get_values(TT.MV), label='MV')
    ax.plot(times, self._tt.get_values(TT.MB), label='MB')
    ax.plot(times, self._tt.get_values(TT.MI), label='MI')
    ax.plot(times, self._tt.get_values(TT.MR), label='MR')
    ax.set_yticks(np.linspace(np.min(bol), np.max(bol), 5))
    ax.legend(
        loc='upper center',
        bbox_to_anchor=(0.5, 1.05),
        ncol=3,
        fancybox=True,
        shadow=True,
        fontsize=12)
    ax.set_xlabel('t')
    ax.set_ylabel('Magnitude')

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
    log_mass = self._swd.mass
    return self.tot_mass - np.power(10, log_mass)

  def __set_misc(self, ax, text_config):
    ax.set_title(text_config['title'])
    ax.set_xlabel(text_config['xlabel'])
    ax.set_ylabel(text_config['ylabel'])

  def __fill_colors(self):
    if len(self.colors) == 0:
      self.colors = list(mcolors.BASE_COLORS.values())[:-1]
