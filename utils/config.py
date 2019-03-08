"""
Configuration for each datafile format
"""

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

# TODO (taebum): more flexible way to labeling table column ?

MRT_TABLE_LABELS = [
    'ZON',
    'AM/SOL',
    'R [1e+14]',
    'V [1e+8]',
    'T [1e+5]',
    'Trad [1e+5]',
    'lgD [1e-6]',
    'lgP [1e+7]',
    'XHI',
    'ENG',
    'LUM',
    'CAPPA',
    'ZON',
    'n_bar',
    'n_e',
    'Fe',
    'II',
    'III',
]

MRT_TIME_PREFIX = 'OBS.TIME='

TT_TABLE_LABELS = [
    'Tbb',
    'rbb',
    'Teff',
    'Rlast_sc',
    'R(tau2/3)',
    'Mbol',
    'MU',
    'MB',
    'MV',
    'MI',
    'MR',
    'Mbolavg',
    'gdepos',
]

TT_TIME_PREFIX = 'time'
