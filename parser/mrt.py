"""
*.mrt parser
"""
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import os

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
    self.mrt_data = dict()
    self.input_param = dict()
    self._store_data()

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
          if line[0] == config.TIME_PREFIX:
            record_value = True

            if len(timestep_data) > 0:
              # flush out previous time_info and timestep_data
              self.mrt_data[time_info] = timestep_data

            # prepare new data
            # generate new timestep_data to store actual value
            time_info = float(line[1])

            if time_info < 0:
              # do not care negative time (not realistic)
              record_value = False
              continue

            timestep_data = {}
          elif line[0] == config.MRT_TABLE_LABELS[0]:
            # column label line
            continue
          else:
            # real data, or prefix of file
            if record_value:
              for idx, value in enumerate(line):
                try:
                  timestep_data[config.MRT_TABLE_LABELS[idx]] = float(value)
                except ValueError:
                  # there are some text like 2.08-100, not 2.08E-100
                  # handle these cases
                  idx = value.find('-')
                  if idx == -1:
                    idx = value.find('+')

                  if idx == -1:
                    raise ValueError(
                        'Cannot convert %r into floating point' % value)
                  value = value[0:idx] + 'E' + value[idx:]
                  timestep_data[config.MRT_TABLE_LABELS[idx]] = float(value)

      if len(timestep_data) > 0:
        # final flushing
        self.mrt_data[time_info] = timestep_data
