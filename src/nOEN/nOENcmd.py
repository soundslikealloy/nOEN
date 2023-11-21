# -*- coding: utf-8 -*-
# Copyright 2023 by Eloi Martinez-Rabert.  All rights reserved.
# This code is part of the Python-dna distribution and governed by its
# license.  Please see the LICENSE.txt file that should have been included
# as part of this package.
# doctest: +NORMALIZE_WHITESPACE
# doctest: +SKIP

"""
This module contain functions to run nOEN in Command Prompt.

"""

import argparse

from getData import loadResults, loadData, createDict
from stats import nOEN

# Command Line Interface (CLI)
parser = argparse.ArgumentParser(description = 'n-Order Ecological Network platform (nOEN). Statistical platform to identify pairwise and higher-order interactions.')

parser.add_argument('-dim', dest = 'dim', default = 'All', action = 'store',
                    help = '[list] or [str] Dimensions we want to test.Write `All` if you want to test all of them (default: `All`).')
# parser.add_argument('-infoinocula', dest = 'infoInocula', default = False, action = 'store_true',
#                     help = '[bool] Information of inocula (or time 0) provided.')
# parser.add_argument('-nofigure', dest = 'noFigure', default = False, action = 'store_true',
#                     help = '[bool] No plotting, only outcomes from nOEN are saved.')
# parser.add_argument('-onlyfigure', dest = 'figureOnly', default = False, action = 'store_true',
#                     help = '[bool] Only plotting of existing results.')
# parser.add_argument('-plottype', dest = 'plotType', default = 'All', action = 'store',
#                     help = '[str] Select plotting style of nOEN outcomes ['squarePlot', 'concentricPlot', 'getNetwork'].')
args = parser.parse_args()
dims = args.dim
# infoInocula = args.infoInocula
# noFigure = args.noFigure
# figureOnly = args.figureOnly
# plotType = args.plotType

# Lorem ipsum...