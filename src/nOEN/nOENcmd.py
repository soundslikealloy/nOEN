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

from getData import loadResults, loadData, createDict
from stats import nOEN

# Command Line Interface (CLI)
parser = argparse.ArgumentParser(description = 'n-Order Ecological Network platform (nOEN). Statistical platform to identify pairwise and higher-order interactions.')

parser.add_argument('-dim', dest = 'dim', default = 'All', action = 'store',
                    help = '[list] or [str] Dimensions we want to test.Write `All` if you want to test all of them (default: `All`).')
# parser.add_argument('-nomismatches', dest = 'noMismatches', default = False, action = 'store_true',
#                     help = '[bool] No mismatches analysis is performed.')
# parser.add_argument('-onlymismatches', dest = 'figureOnly', default = False, action = 'store_true',
#                     help = '[bool] Only mismatches results are saved. FASTA and alignment files are not saved.')
args = parser.parse_args()
dims = args.dim
# noMismatches = args.noMismatches
# figureOnly = args.figureOnly

# Lorem ipsum...