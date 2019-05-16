"""
Main script of overall visualization
"""
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import matplotlib as mpl

from matplotlib import pyplot as plt
from core.plot import Plotter
from utils.config import SWD, TT


def main():
  plotter = Plotter(root='./data/p600_BliNi2')
  #  plotter = Plotter(root='./data/p600_PolyEnv_alpha0.8_2')
  #  plotter = Plotter(root='./data/p600_PolyEnv_alpha3.0_2')
  plotter.plot_key(SWD.T, logx=False, logy=False)
  #  plotter.plot_key(SWD.R)
  #  plotter.plot_key(TT.R)
  input('Press Enter to exit')


if __name__ == "__main__":
  # interactive on
  plt.ion()

  # global matplotlib configuration goes here
  mpl.rcParams['figure.figsize'] = [16.0, 9.0]
  mpl.rcParams['figure.dpi'] = 80
  mpl.rcParams['figure.titlesize'] = 'medium'

  mpl.rcParams['savefig.dpi'] = 100

  mpl.rcParams['font.size'] = 16

  mpl.rcParams['legend.fontsize'] = 'large'

  mpl.rcParams['image.cmap'] = 'GnBu'

  main()
