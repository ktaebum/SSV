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

from stella.utils import config
from stella.utils.config import SWD
from stella.utils.config import TT
from stella.utils.config import ABN
from stella.utils.util import find_closest

from stella.parser.tt import TTParser
from stella.parser.swd import SWDParser
from stella.parser.abn import ABNParser

# global PLOTTER
PLOTTER = None


class Plotter:
  """
  Basic plotting container for STELLAR simulation data
  Each holds single parser for specific file
  """

  def __init__(self, root, prefix):
    """
    @param root: project root
    """
    self._tt = TTParser(root, prefix)
    self._swd = SWDParser(root, prefix)
    self._abn = ABNParser(root, prefix)
    self.tot_mass = self._tt.stellar_info['MASS']
    self.mass = self._mass_coord()
    self.photosphere = self._photosphere_alter()

    self.fig = None
    self.ax1 = None
    self.ax2 = None

    self.colors = []
    self.__fill_colors()

  def save(self, name):
    plt.savefig(name)

  def plot(self, data, **kwargs):
    """ Main plot function
    """
    plot_config = config.build_configuration(data, **kwargs)
    title = kwargs.get('title', str(data).split('.')[-1])

    if isinstance(data, SWD):
      data = self._swd.get_value_of_key(data)

    if data is None:
      warnings.warn('Cannot retreive key %s' % str(data))
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
        self._plot_magnitude(plot_config['log_time_mag'])
      else:
        self.ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=12, colspan=12)
        self.ax2 = None

    fig = self.fig
    ax = self.ax1

    if plot_config['log_time']:
      ax.set_xscale('log')
    if plot_config['log_mass']:
      ax.invert_yaxis()

    contour = ax.contourf(times, mass, data, alpha=plot_config['transparency'])
    if plot_config['photosphere']:
      self.__fill_colors()

      if plot_config['log_mass']:
        ax.plot(
            self._swd.times,
            np.log10(self.tot_mass - self.photosphere),
            color=self.colors.pop(),
            label='photosphere',
            marker='o',
        )
      else:
        ax.plot(
            self._swd.times,
            self.photosphere,
            color=self.colors.pop(),
            label='photosphere',
            marker='o',
        )

    ax.set_xlim(time_vector[0], time_vector[-1])
    if not plot_config['log_mass']:
      ax.set_ylim(mass_vector[0], self.tot_mass)
    else:
      ax.set_ylim(mass_vector[0], mass_vector[-1])

    fig.colorbar(contour, ax=ax)

    ax.set_title(title)
    if plot_config['log_mass']:
      ax.set_ylabel(r'$\log{(M_{tot} - M_{r})}$')
    else:
      ax.set_ylabel(r'$M_{r}$')
    ax.set_xlabel('t')
    ax.legend(
        loc='upper right',
        shadow=True,
        bbox_to_anchor=(1.4, 1.0),
    )

  def plot_abn_data(self, key, threshold=0.1, **kwargs):
    if self.ax1 is None:
      return

    if not isinstance(key, (ABN, tuple)):
      return

    if isinstance(key, ABN):
      name = str(key).split('.')[-1]
    elif isinstance(key, tuple):
      name = ' + '.join(list(map(lambda x: str(x).split('.')[-1], key)))

    plot_config = config.build_configuration(key, **kwargs)
    d_low, d_high = self._abn.get_element_data(key, threshold)

    if d_low == -1 and d_high == -1:
      # warning and return
      warnings.warn('Cannot plot for %s > %1.1f' % (name, threshold))
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
        label='%s > %1.1f' % (name, threshold),
        linewidth=2,
        #  linestyle='--',
    )
    ax.plot(
        time_vector,
        np.ones_like(time_vector) * mass_high,
        color=color,
        linewidth=2,
        linestyle=':',
    )
    ax.legend(
        loc='upper right',
        shadow=True,
        bbox_to_anchor=(1.4, 1.0),
    )

  def _plot_magnitude(self, log_time):
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
    if log_time:
      ax.set_xscale('log')
      ax.legend(loc='best', ncol=3, fancybox=True, shadow=True)
    else:
      ax.legend(loc='best', ncol=3, fancybox=True, shadow=True)
    ax.set_xlabel('t')
    ax.set_ylabel('Magnitude')

  def _photosphere_alter(self):
    """
    calculate photosphere radius (deprecated)
    from swd -> tt finding
    """
    tt_times = self._tt.times
    swd_times = self._swd.times
    swd_time2idx = self._swd.time2idx
    close_time_idx = np.array(
        list(
            map(lambda x: find_closest(tt_times, len(tt_times), x, True),
                swd_times)),
        dtype=np.int32)

    r_taus = np.log10(self._tt.get_values(TT.R))[close_time_idx]

    r_tau_mass = []
    for r_tau, time in zip(r_taus, swd_times):
      swd_time_data = self._swd.data[swd_time2idx[time], :, config.SWD2IDX[SWD.
                                                                           R]]
      idx = find_closest(swd_time_data, len(swd_time_data), r_tau, True)
      r_tau_mass.append(self.mass[idx])

    return np.array(r_tau_mass)

  def _photosphere(self):
    """
    calculate photosphere radius (deprecated)
    from tt -> swd finding
    """
    r_taus = np.log10(self._tt.get_values(TT.R))
    r_tau_mass = []
    tt_times = self._tt.get_time_range()
    swd_times = self._swd.times
    swd_time2idx = self._swd.time2idx

    # closest time corresponding of tt_time in swd_time
    closest_time = np.array(
        list(
            map(
                lambda x: find_closest(swd_times, len(swd_times), x),
                tt_times,
            )))

    tmp = list(sorted(swd_times.copy()))
    for i, j in zip(tmp, swd_times):
      assert i == j

    for r_tau, time in zip(r_taus, closest_time):
      swd_time_data = self._swd.data[swd_time2idx[time], :, config.SWD2IDX[SWD.
                                                                           R]]
      idx = find_closest(swd_time_data, len(swd_time_data), r_tau, True)
      r_tau_mass.append(self.mass[idx])

    return np.array(r_tau_mass)

  def _mass_coord(self):
    log_mass = self._swd.mass
    return self.tot_mass - np.power(10, log_mass)

  def __fill_colors(self):
    if len(self.colors) == 0:
      self.colors = list(mcolors.BASE_COLORS.values())[:-1]


def get_plotter(root=None, prefix=None):
  """
  retreive plotter
  """
  global PLOTTER

  if PLOTTER is None:
    if root is not None:
      PLOTTER = Plotter(root, prefix)

  return PLOTTER
