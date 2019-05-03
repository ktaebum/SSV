"""
Configuration for each datafile format
"""

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from enum import Enum


def build_configuration(key, **kwargs):
  # plot related configuration
  plot_config = {
      'logx': kwargs.get('logx', False),
      'logy': kwargs.get('logy', False),
  }

  # text related configuration
  text_config = {
      'xlabel':
          kwargs.get('xlabel', 't'),
      'ylabel':
          kwargs.get('ylabel', 'M' if isinstance(key, SWD) else 'value'),
      'title':
          kwargs.get('title',
                     str(key).split('.')[-1]),
  }

  return plot_config, text_config


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


SWD2IDX = {k: v for v, k in enumerate(SWD)}
