"""
Main script of overall visualization
"""
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import matplotlib as mpl

from matplotlib import pyplot as plt

from core.plot import Plotter

from utils.config import SWD
from utils.config import ABN


def main():
  #  write plot configuration
  configuration = {
      'log_time': False,
      'log_mass': False,
      'photosphere': True,
      'magnitude': False,
  }

  plotter = Plotter(root='./data/p600_BliNi2')
  plotter.plot(SWD.V, **configuration)
  plotter.plot_abn_data(ABN.H, ratio=0.2, **configuration)
  plotter.plot_abn_data((ABN.C, ABN.O), ratio=0.1, **configuration)
  plotter.plot_abn_data((ABN.NI, ABN.O, ABN.C), ratio=0.7, **configuration)
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

  #  mpl.rcParams['legend.fontsize'] = 'large'

  mpl.rcParams['image.cmap'] = 'GnBu'
  main()
