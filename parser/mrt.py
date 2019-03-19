"""
*.mrt parser
"""
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import os
import numpy as np

from utils import config


class MRTParser:

  def __init__(self, path):
    """
    @param path: file path for data folder (or directly *.mrt file)
    """
    if os.path.isdir(path):
      # directory for data folder
      filename = os.path.join(path, path.split('/')[-1] + '.mrt')
    elif os.path.isfile(path):
      # file
      if path[-4:] == '.mrt':
        filename = path
      else:
        raise ValueError('Non-supported file type %s' % path[-4:])
    else:
      raise FileNotFoundError('Neither dir nor file')

    self.filename = filename
    self.data = dict()
    self.input_param = dict()

    # misc information
    self.stellar_info = dict()

    # store whole data
    self._store_data()

  def get_time_range(self):
    return np.array(list(self.data.keys()), dtype=np.float32)

  def get_mass_coordinate(self):
    key = list(self.data.keys())[-3]
    mass = []
    data = self.data[key]
    for value in data.values():
      coordinate = value['AM/SOL']
      if coordinate < 0:
        # adjust
        coordinate = self.stellar_info['MASS'] + coordinate
      mass.append(coordinate)

    return np.array(mass, dtype=np.float32)

  def get_value_of_key_per_zon(self, key, zon):
    values = []

    for timestep_data in self.data.values():
      if zon not in timestep_data:
        raise KeyError('Non existing ZON %r' % zon)
      values.append(timestep_data[zon].get(key, 0.0))
    return np.array(values, dtype=np.float32)

  def get_value_of_key(self, key):
    values = []
    for timestep_data in self.data.values():
      value = []
      for i in range(1, 250):
        if i in timestep_data:
          value.append(timestep_data[i][key])
        else:
          value.append(0.0)
      values.append(value)

    return np.rot90(np.array(values, dtype=np.float32))

  def _store_data(self):
    """
    read each line of mrt file and store
    """
    with open(self.filename, 'r') as file:
      # initialize
      timestep_data = {}
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

          if line[0] == config.MRT_TIME_PREFIX:
            record_value = True

            if len(timestep_data) > 0:
              # flush out previous time_info and timestep_data
              self.data[time_info] = timestep_data

            # prepare new data
            # generate new timestep_data to store actual value
            time_info = float(line[1])
            timestep_data = {}

            if time_info < 0:
              # do not care negative time (not realistic)
              record_value = False
              continue
          elif line[0] == config.MRT_TABLE_LABELS[0]:
            # column label line
            # next line is target data
            continue
          else:
            # real data
            if record_value:
              ZON = int(line[0])
              timestep_data[ZON] = {}

              def float_safe(value):
                # safe type casting to float
                # in mrt file, there are some text like
                # 2.08-100, not 2.08E-100
                try:
                  return float(value)
                except ValueError:
                  idx = value.find('-')
                  if idx == -1:
                    idx = value.find('+')
                  if idx == -1:
                    raise ValueError(
                        'Cannot convert %r into floating point' % value)
                  value = value[0:idx] + 'E' + value[idx:]
                  return float(value)

              for idx, value in enumerate(line[1:], 1):
                timestep_data[ZON][config.MRT_TABLE_LABELS[idx]] = float_safe(
                    value)

      if len(timestep_data) > 0:
        # final flushing
        self.data[time_info] = timestep_data
