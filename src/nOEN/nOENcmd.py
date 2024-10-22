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

from stats import nOEN
from getData import loadData, loadResults, createDict, writeResults
from plotting import ecologicalGrid

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
parser.add_argument('-onlyRead', dest = 'onlyRead', default = False, action = 'store_true',
                    help = '[bool] Export results with existing nOEN results (Default: False).')
parser.add_argument('-varSelect', dest = 'varSelect', default = 0, nargs = '+', action = 'store',
                    help = '[list] Variables we want to write and/or plot. Name of variables separated by spaces without parenthesis or brakets (Default: 0 -> \'All\'; CASE-SENSITIVE).')
parser.add_argument('-onlysig', dest = 'onlySig', default = False, action = 'store_true',
                    help = '[bool] Only significant results (p < 0.05) are written and/or plotted (Default: False).')
parser.add_argument('-noFigures', dest = 'noFigure', default = True, action = 'store_false',
                    help = '[bool] No plotting, only outcomes from nOEN are saved in Excel.')
parser.add_argument('-onlyFigures', dest = 'figureOnly', default = False, action = 'store_true',
                    help = '[bool] Only plotting results.')
# parser.add_argument('-plottype', dest = 'plotType', default = 'All', action = 'store',
#                     help = '[str] Select plotting style of nOEN outcomes ['squarePlot', 'concentricPlot', 'getNetwork'].')
args = parser.parse_args()

fileName = args.fileName
dim = args.dim
infoInocula = args.infoInocula
excel = args.noExcel
onlyRead = args.onlyRead
varSelect = args.varSelect
onlySig = args.onlySig
figure = args.noFigure
figureOnly = args.figureOnly
# plotType = args.plotType

#-DEBUGGING-#
# print('>> Arguments')
# print(' > Dims: ' + str(dim))
# print(' > InfoInocula: ' + str(infoInocula))
# print(' > CreateExcelWithResults: ' + str(excel))
# print(' > OnlyRead (read previous results): ' + str(onlyRead))
# print(' > varWrite: ' + str(varSelect))
# print(' > OnlySignifiative: ' + str(onlySig))
# print(' > Figure: ' + str(figure))
# print(' > OnlyFigures: ' + str(figureOnly))
#-----------#
if figureOnly:
    excel = False
if not onlyRead:
    # Read data from Excel and create nested dictionary
    loadDict = loadData(fileName)
    # Run nOEN
    leDict = nOEN(loadDict, dim, infoInocula)
    # Save results in .pyn
    createDict('saveDict', leDict, fileName)
# Create Excel file with results
if excel:
    writeResults(fileName, dim, varSelect, onlySig)
if figure:
    if onlyRead:
        leDict = loadResults(fileName)
    ecologicalGrid(fileName, leDict, dim, varSelect, onlySig)
