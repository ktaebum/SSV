"""
*.abn parser
"""

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import os
import numpy as np

from stella.utils import config
from stella.utils.config import ABN


class ABNParser:

  def __init__(self, path):
    """
    @param path: file path for data folder (or directly *.abn file)
    """
    if os.path.isdir(path):
      # directory for data folder
      filename = os.path.join(path, path.split('/')[-1] + '.abn')
    elif os.path.isfile(path):
      # file
      if path[-4:] == '.abn':
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

  def get_element_data(self, key, threshold=0.1):
    if isinstance(key, ABN):
      data = self.data[:, config.ABN2IDX[key]]
      valid = np.where(data > threshold)
      if len(valid[0]) == 0:
        return -1, -1
      else:
        return valid[0][0], valid[0][-1]
    elif isinstance(key, tuple):
      data = np.zeros(self.data.shape[0], dtype=np.float32)
      for k in key:
        data += self.data[:, config.ABN2IDX[k]]
      valid = np.where(data > threshold)
      if len(valid[0]) == 0:
        return -1, -1
      else:
        return valid[0][0], valid[0][-1]

  def _store_data(self):
    self.data = np.loadtxt(self.filename)
