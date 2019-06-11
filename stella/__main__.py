"""
Main script of overall visualization

Supported Keywords in SWD file
  MASS = 'logarith of Lagrangean mass from surface lgm'
  R = 'logarith of radius cm lgr'
  V = 'velocity in 1e8 cm/s v8'
  T = 'lg T'
  TRAD = 'lg Trad  7 when nonzero'
  RHO = 'lg rho in 1e-6 gcc'
  P = 'lg P'
  QV = 'lg qv artificial viscosity'
  ENG = 'lg eng12 in 1e12'
  LUM = 'luminosity L_r lum40 in units 1e40 erg/s'
  KAPPA_ROSSELAND = 'kappa_Rosseland cap'

Supported Keywords in ABN file
  H = 'hydrogen',
  He = 'helium',
  C = 'Carbon',
  N = 'nitrogen',
  O = 'Oxygen',
  Ne = 'Neon',
  Mg = 'magnesium',
  Si = 'Silicon',
  S = 'Sulfur',
  Ar = 'Argon',
  Ca = 'calcium',
  Fe = 'iron',
  Ni = 'Nickel'
"""
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import argparse
import matplotlib as mpl

from matplotlib import pyplot as plt

from stella.core.plot import get_plotter

from stella.utils.config import SWD
from stella.utils.config import ABN


def main(args):
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
          you must type title (cannot auto-inference) in latex format
  """

  # this is example configuration
  # actually, you do not have to type all configurations
  #   (can skip some keywords or leave just empty dictionary)
  configuration = {
      'log_time': False,
      'log_mass': False,
      'photosphere': True,
      'magnitude': True,
      'log_time_mag': False,
      'transparency': 0.6,
      'title': r'$0.5 V^{2}$',
      # do not modify below configurations
      'save': args.save,
  }

  if not args.save:
    plt.ion()

  if args.path is None:
    raise ValueError('Must pass path')
  elif args.path[-1] == '/':
    args.path = args.path[:-1]

  if args.prefix is None:
    args.prefix = args.path.split('/')[-1]

  plotter = get_plotter(root=args.path, prefix=args.prefix)
  plotter.plot(0.5 * SWD.V**2, **configuration)
  plotter.plot_abn_data(ABN.H, threshold=0.2, **configuration)
  plotter.plot_abn_data((ABN.C, ABN.O), threshold=0.1, **configuration)
  plotter.plot_abn_data((ABN.Ni, ABN.O, ABN.C), threshold=0.7, **configuration)

  if not args.save:
    input('Press Enter to exit ')
  else:
    figname = args.figname
    if figname is None:
      figname = args.path.split('/')[-1] + '.png'

    plotter.save(figname)


if __name__ == "__main__":
  # command line argument parser
  parser = argparse.ArgumentParser(
      prog='python -m stella',
      description='stella simulation data visualizer',
  )
  parser.add_argument(
      '--path',
      help='root directory path of stella data',
  )
  parser.add_argument(
      '--prefix',
      help='name prefix of stella data files (default set to name of path)',
  )
  parser.add_argument(
      '--save',
      help='save figure rather than show figure',
      action='store_true',
  )
  parser.add_argument(
      '--figname',
      help='name of figure (valid if save is on)',
  )

  # global matplotlib configuration goes here
  mpl.rcParams['figure.figsize'] = [16.0, 9.0]
  mpl.rcParams['figure.dpi'] = 80
  mpl.rcParams['figure.titlesize'] = 'medium'

  mpl.rcParams['savefig.dpi'] = 100

  mpl.rcParams['font.size'] = 16

  mpl.rcParams['legend.fontsize'] = 12

  # color map
  mpl.rcParams['image.cmap'] = 'GnBu'
  main(parser.parse_args())
