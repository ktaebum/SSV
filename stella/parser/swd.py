"""
*.swd parser
"""

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import os
import numpy as np

from stella.utils import config


class SWDParser:

  def __init__(self, path, prefix):
    """
    @param path: file path for data folder (or directly *.swd file)
    """
    if os.path.isdir(path):
      # directory for data folder
      filename = os.path.join(path, prefix + '.swd')
    elif os.path.isfile(path):
      # file
      if path[-4:] == '.swd':
        filename = path
      else:
        raise ValueError('Non-supported file type %s' % path[-4:])
    else:
      raise FileNotFoundError('Neither dir nor file')

    self.filename = filename
    self.data = None
    self.num_zon = None

    # store whole data
    self._store_data()
    """
    for d in self.data:
      print(d)
    print(self.times)
    print(self.time2idx)
    print(self.data.shape)
    """

  @property
  def times(self):
    return self.data[:, 0, 0]

  @property
  def time2idx(self):
    return {k: v for v, k in enumerate(self.times)}

  @property
  def zons(self):
    return np.arange(1, self.num_zon + 1, dtype=np.float32)

  @property
  def mass(self):
    idx = config.SWD2IDX[config.SWD.MASS]
    return self.data[0, :, idx]

  def get_value_of_key(self, key):
    # get data from given key
    try:
      idx = config.SWD2IDX[key]
      data = self.data[:, :, idx]
      return data.transpose()
    except KeyError:
      return None

  def _store_data(self):
    self.data = np.loadtxt(self.filename)
    num_columns = len(config.SWD)

    zon_interval = np.where(self.data[:, 0] > 0)[0]
    self.num_zon = zon_interval[1] - zon_interval[0] + 1

    # data shape is (time_step, time_interval, num_columns)
    self.data = self.data.reshape(-1, self.num_zon, num_columns)
