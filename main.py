"""
Main script of overall visualization
"""
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import matplotlib as mpl

from matplotlib import pyplot as plt

from stella.core.plot import get_plotter

from stella.utils.config import SWD
from stella.utils.config import ABN


def main():
  #  write plot configuration
  """
  Possible Configurations
    1. log_time (bool): log scale of time in contour if True
    2. log_mass (bool): log (M_tot - M_r) if True
    3. photosphere (bool): plot photosphere if True
    4. magnitude (bool): plot Mbol, Mu... magnitude if True
    5. log_time_mag (bool): log scale of time in magnitude plot if True
    6. transparency (0.0 - 1.0): transparency of contour (default 0.6)
        0.0 is the most transparent
    7. title: title of plot
        if empty, it automatically parse from target key
        if you use arithmetic operation like SWD.V * 2,
          you must type title (cannot auto-inference)
  """
  configuration = {
      'log_time': False,
      'log_mass': False,
      'photosphere': True,
      'magnitude': True,
      'log_time_mag': False,
      'transparency': 0.6,
      'title': r'$0.5 V^{2}$',
  }

  plotter = get_plotter(root='./data/p600_PolyEnv_alpha3.0_2')
  plotter.plot(0.5 * SWD.V**2, **configuration)
  plotter.plot_abn_data(ABN.H, threshold=0.2, **configuration)
  plotter.plot_abn_data((ABN.C, ABN.O), threshold=0.1, **configuration)
  plotter.plot_abn_data((ABN.Ni, ABN.O, ABN.C), threshold=0.7, **configuration)

  input('Press Enter to exit ')


if __name__ == "__main__":
  # interactive on
  plt.ion()

  # global matplotlib configuration goes here
  mpl.rcParams['figure.figsize'] = [16.0, 9.0]
  mpl.rcParams['figure.dpi'] = 80
  mpl.rcParams['figure.titlesize'] = 'medium'

  mpl.rcParams['savefig.dpi'] = 100

  mpl.rcParams['font.size'] = 16

  mpl.rcParams['legend.fontsize'] = 12

  # color map
  mpl.rcParams['image.cmap'] = 'GnBu'
  main()
