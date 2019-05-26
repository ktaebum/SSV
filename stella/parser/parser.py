"""
Interface for parser
"""

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from parser.tt import TTParser
from parser.mrt import MRTParser


class Parser:

  def __init__(self, proj_root):
    self._fig = None

  def get_value_of_key(self, key):
    raise NotImplementedError

  def _store_data(self):
    raise NotImplementedError

  def plot(self, key):
    raise NotImplementedError
