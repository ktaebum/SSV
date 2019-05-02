"""
Main script of overall visualization
"""
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from matplotlib import pyplot as plt

from core.plot import Plotter

from utils.config import SWD, TT

import numpy as np


def main():
  plotter = Plotter(root='./data/p600_BliNi2')
  plotter = Plotter(root='./data/p600_PolyEnv_alpha0.8_2')
  plotter = Plotter(root='./data/p600_PolyEnv_alpha3.0_2')
  while True:
    #  plotter.plot_key(SWD.V)
    #  plotter.plot_key(SWD.R)
    plotter.plot_key(TT.R)
    plotter.plot_key(TT.RLAST_SC)
    input()

  pass


if __name__ == "__main__":
  # interactive on
  plt.ion()

  main()
