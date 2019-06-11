"""
*.tt parser
"""

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import os
import numpy as np

from stella.utils import config


class TTParser:

  def __init__(self, path, prefix):
    """
    @param path: file path for data folder (or directly *.tt file)

    *.tt data is single dimension vector per each time

    Data Structure is formed as
      DataFrame of [time, ...]
    """
    if os.path.isdir(path):
      # directory for data folder
      filename = os.path.join(path, prefix + '.tt')
    elif os.path.isfile(path):
      # file
      if path[-3:] == '.tt':
        filename = path
      else:
        raise ValueError('Non-supported file type %s' % path[-4:])
    else:
      raise FileNotFoundError('Neither dir nor file')

    self.filename = filename
    self.data = {}
    self.stellar_info = {}
    self._store_data()

  @property
  def times(self):
    return np.array(list(self.data.keys()), dtype=np.float32)

  def get_time_range(self):
    return np.array(list(self.data.keys()), dtype=np.float32)

  def get_values(self, key):
    values = []
    for timestep_data in self.data.values():
      values.append(timestep_data.get(key, 0.0))
    return np.array(values, dtype=np.float32)

  def _store_data(self):
    """
    read each line of mrt file and store
    """
    with open(self.filename, 'r') as file:
      # initialize
      time_info = 0

      # whether record value (skip prefix of file, skip negative time)
      record_value = False

      for line in file:
        line = line.strip()
        if line:
          line = line.split()
          if len(self.stellar_info) == 0 and 'MASS(SOLAR)=' in line:
            # basic (essential) information
            self.stellar_info['MASS'] = float(line[1])
            self.stellar_info['RADIUS'] = float(line[-1])
          if line[0] == config.TT_TIME_PREFIX:
            record_value = True
          else:
            if record_value:
              time_info = float(line[0])
              if time_info > 0:
                # valid time
                values = {k: float(v) for k, v in zip(config.TT, line[1:])}
                self.data[time_info] = values
