"""
Wrapper for every parser
"""

from parser.tt import TTParser
from parser.mrt import MRTParser


class Parser:

  def __init__(self, proj_root):

    try:
      self._mrt = MRTParser(proj_root)
    except FileNotFoundError:
      self._mrt = None

    try:
      self._tt = TTParser(proj_root)
    except FileNotFoundError:
      self._tt = None
