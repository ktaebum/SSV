"""
Configuration for each datafile format
"""

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import numpy as np
import stella.core.plot as stella_plot

from enum import Enum


def _valid_operation(self_type, other):
  if not isinstance(other, (self_type, np.ndarray, int, float)):
    raise TypeError('Cannot define operation with %r type', type(other))


def build_configuration(key, **kwargs):
  # plot related configuration
  plot_config = {
      'log_time': kwargs.get('log_time', False),
      'log_mass': kwargs.get('log_mass', False),
      'magnitude': kwargs.get('magnitude', False),
      'photosphere': kwargs.get('photosphere', True),
      'log_time_mag': kwargs.get('log_time_mag', False),
      'transparency': kwargs.get('transparency', 0.6),
  }

  return plot_config


class MRT(Enum):
  AM = 'mass in solar mass',
  R = 'radius cm 1e+14',
  V = 'velocity 1e+8',
  T = 'temperature 1e+5',
  Trad = 'rad temperature? 1e+5',
  logD = 'log D 1e-6',
  logP = 'log P 1e+7',
  XHI = 'xhi',
  ENG = 'eng',
  LUM = 'lum',
  CAPPA = 'cappa',
  ZON = 'radial zone number km',
  N_BAR = 'n_bar',
  N_E = 'n_e',
  Fe = 'Fe',
  II = 'II',
  III = 'III',


MRT2IDX = {k: v for v, k in enumerate(MRT)}
MRT_TIME_PREFIX = 'OBS.TIME='


class TT(Enum):
  TBB = 'temperature'
  RBB = 'radius',
  TEFF = 'effective temperature',
  RLAST_SC = 'rlast_sc',
  R = 'R(tau2/3)',
  MBOL = 'mbol',
  MU = 'MU',
  MB = 'MB',
  MV = 'MV',
  MI = 'MI',
  MR = 'MR',
  MBOLAVG = 'Mbolavg',
  GDEPOS = 'gdepos'

  def __add__(self, other):
    pass


TT2IDX = {k: v for v, k in enumerate(TT)}

TT_TIME_PREFIX = 'time'


class SWD(Enum):
  TIME = 'time in days (non-zero)'
  ZON = 'radial zone number km'
  MASS = 'logarith of Lagrangean mass from surface lgm'
  R = 'logarith of radius cm lgr'
  V = 'velocity in 1e8 cm/s v8'
  T = 'lg T'
  TRAD = 'lg Trad  7 when nonzero'
  RHO = 'lg rho in 1e-6 gcc'
  P = 'lg P'
  QV = 'lg qv artificial viscosity'
  ENG = 'lg eng12 in 1e12'
  LUM = 'luminosity L_r lum40 in units 1e40 erg/s'
  KAPPA_ROSSELAND = 'kappa_Rosseland cap'

  def __add__(self, other):
    _valid_operation(SWD, other)

    plotter = stella_plot.get_plotter()
    self_data = plotter._swd.get_value_of_key(self)
    if isinstance(other, SWD):
      other_data = plotter._swd.get_value_of_key(other)
      return self_data + other_data
    else:
      return self_data + other

  def __mul__(self, other):
    _valid_operation(SWD, other)

    plotter = stella_plot.get_plotter()
    self_data = plotter._swd.get_value_of_key(self)
    if isinstance(other, SWD):
      other_data = plotter._swd.get_value_of_key(other)
      return self_data * other_data
    else:
      return self_data * other

  def __div__(self, other):
    _valid_operation(SWD, other)

    plotter = stella_plot.get_plotter()
    self_data = plotter._swd.get_value_of_key(self)
    if isinstance(other, SWD):
      other_data = plotter._swd.get_value_of_key(other)
      return self_data / other_data
    else:
      return self_data / other

  def __pow__(self, other):
    _valid_operation(SWD, other)

    plotter = stella_plot.get_plotter()
    self_data = plotter._swd.get_value_of_key(self)
    if isinstance(other, SWD):
      other_data = plotter._swd.get_value_of_key(other)
      return self_data**other_data
    else:
      return self_data**other


SWD2IDX = {k: v for v, k in enumerate(SWD)}


class ABN(Enum):
  ZON = 'radial zone number',
  DUM1 = 'dummy1',
  DUM2 = 'dummy2',
  DUM3 = 'dummy3',
  H = 'hydrogen',
  He = 'helium',
  C = 'Carbon',
  N = 'nitrogen',
  O = 'Oxygen',
  Ne = 'Neon',
  DUM4 = 'dummy4',
  Mg = 'magnesium',
  DUM5 = 'dummy5',
  Si = 'Silicon',
  S = 'Sulfur',
  Ar = 'Argon',
  Ca = 'calcium',
  Fe = 'iron',
  DUM6 = 'dummy6',
  Ni = 'Nickel'


ABN2IDX = {k: v for v, k in enumerate(ABN)}
