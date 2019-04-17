"""
Main script of overall visualization
"""
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from matplotlib import pyplot as plt

from parser.mrt import MRTParser
from parser.tt import TTParser

from core.plot import Plotter

import time
import numpy as np


def main():
  """
  plt.figure()
  while True:
    print('CMD: ', end='')
    input()
  """
  x = np.arange(100)
  y = np.sin(x)

  mrt = MRTParser('./data/p600_BliNi2')
  tt = TTParser('./data/p600_BliNi2')
  plotter = Plotter(mrt=mrt, tt=tt)
  while True:
    plotter.plot_key('R(tau2/3)', log_y=True)
    plotter.plot_key('Teff', log_y=True)
    input()

  pass


if __name__ == "__main__":
  # interactive on
  plt.ion()

  main()
