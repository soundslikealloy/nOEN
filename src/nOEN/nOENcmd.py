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

from getData import loadData, createDict, writeResults
from stats import nOEN

# Command Line Interface (CLI)
parser = argparse.ArgumentParser(description = '> n-Order Ecological Network platform (nOEN). Statistical platform to identify and map pairwise and higher-order interactions.')
# Arguments
parser.add_argument('-filename', dest = 'fileName', required = True, action = 'store',
                    help = '[str] Name of file with data and info (REQUIRED & CASE-SENSITIVE).')
parser.add_argument('-dim', dest = 'dim', default = 0, nargs = '+', type = int, action = 'store',
                    help = '[list] Dimensions we want to test. Numbers separated by spaces without parenthesis or brakets (Default: 0 -> \'All\').')
parser.add_argument('-infoinocula', dest = 'infoInocula', default = False, action = 'store_true',
                    help = '[bool] Information of inocula (or time 0) provided (Default: False).')
parser.add_argument('-noExcel', dest = 'noExcel', default = True, action = 'store_false',
                    help = '[bool] Only save nOEN results in .npy format (Default: True).')
parser.add_argument('-onlyExcel', dest = 'onlyExcel', default = False, action = 'store_true',
                    help = '[bool] Create Excel file with existing nOEN results (Default: False).')
parser.add_argument('-varSelect', dest = 'varSelect', default = 0, nargs = '+', action = 'store',
                    help = '[list] Variables we want to write and/or plot. Name of variables separated by spaces without parenthesis or brakets (Default: 0 -> \'All\'; CASE-SENSITIVE).')
parser.add_argument('-onlysig', dest = 'onlySig', default = False, action = 'store_true',
                    help = '[bool] Only significant results (p < 0.05) are written and/or plotted (Default: False).')
# parser.add_argument('-nofigure', dest = 'noFigure', default = True, action = 'store_true',
#                     help = '[bool] No plotting, only outcomes from nOEN are saved.')
# parser.add_argument('-onlyfigure', dest = 'figureOnly', default = True, action = 'store_true',
#                     help = '[bool] Only plotting of existing results.')
# parser.add_argument('-plottype', dest = 'plotType', default = 'All', action = 'store',
#                     help = '[str] Select plotting style of nOEN outcomes ['squarePlot', 'concentricPlot', 'getNetwork'].')
args = parser.parse_args()

fileName = args.fileName
dim = args.dim
infoInocula = args.infoInocula
excel = args.noExcel
onlyExcel = args.onlyExcel
varSelect = args.varSelect
onlySig = args.onlySig
# noFigure = args.noFigure
# figureOnly = args.figureOnly
# plotType = args.plotType

#-DEBUGGING (argparse)
# print('>> Arguments')
# print(' > Dims: ' + str(dim))
# print(' > InfoInocula: ' + str(infoInocula))
# print(' > CreateExcelWithResults: ' + str(excel))
# print(' > OnlyExcel (read previous results): ' + str(onlyExcel))
# print(' > varWrite: ' + str(varSelect))
# print(' > OnlySignifiative: ' + str(onlySig))
# print('')
#----------

if not onlyExcel:
    # Read data from Excel and create nested dictionary
    loadDict = loadData(fileName)
    # Run nOEN
    leDict = nOEN(loadDict, dim, infoInocula)
    # Save results in .pyn
    createDict('saveDict', leDict, fileName)
# Create Excel file with results
if excel:
    writeResults(fileName, dim, varSelect, onlySig)
    
