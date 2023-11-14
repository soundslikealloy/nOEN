# -*- coding: utf-8 -*-
# Copyright 2023 by Eloi Martinez-Rabert.  All rights reserved.
# This code is part of the Python-dna distribution and governed by its
# license.  Please see the LICENSE.txt file that should have been included
# as part of this package.
# doctest: +NORMALIZE_WHITESPACE
# doctest: +SKIP

"""
This module contain functions to get data for various purposes.

- :func:`loadData` for getting the whole information and data sets from Excel file (nameFile.xlsx). Please see README file for more information.

- :func:`loadResults` for getting the nOEN outcomes of the data set already analysed and plot them

"""

import os.path
import pandas as pd
import numpy as np
from itertools import combinations as _comb

def createDict(mainKeyName, iDict, info):
    """
    - :input:`mainKeyName` (str). Mode of dictionary creation ['data', 'comb', 'coeff', 'saveDict']
    - :input:`iDict` (dict). Dictionary file
    - :input:`info` (dict). New information included into dictionary file (iDict)

    """
    if mainKeyName == 'data':
        iDict['data'] = info 
        print(' > Structure dataset: Done.')
        return iDict      
    elif mainKeyName == 'comb':
        iDict['comb'] = info 
        print(' > Structure comb: Done.')
        return iDict
    elif mainKeyName == 'coeff':
        iDict['coeff'] = info 
        print(' > Structure coeff: Done.')
        return iDict
    elif mainKeyName == 'saveDict':
        path = '../../Results/'
        fullPathSave = path + info + '.npy'
        if os.path.isfile(fullPathSave) == True:
            val = input(' > Do you want to overwrite `' + info + '.npy`? [Y/N]: ')
            if val == 'Y' or val == 'y':
                np.save(fullPathSave, iDict) 
                print(' > Data structure saved - `' + info +'.npy`.')
            else:
                print(' > Data structure not saved. If you don\'t want to overwrite results files, use another name for data Excel.')
        else:
            np.save(fullPathSave, iDict)
            print(' > Data structure saved - `' + info +'.npy`.')
    else:
        print(' > No expected Structure: `' + mainKeyName + '`')
    print('')

def loadData(fileName):
    """
    - :input:`fileName` (str). Name of file where data and info are collected

    """  
    print('\n>> Loading data...')
    # Path name of Data
    path = '../../Data/'
    fullPath = path + fileName + '.xlsx'
    # Initialization 
    leDict = {}             # Full dictionary (`data` + `comb` + `coeff`)
    combDict = {}           # Dictionary of combinations (`comb`)
    coeffDict = {}          # Dictionary of Tau-N coefficients (`coeff`)
    # Structure dataset (data)
    di = pd.read_excel(fullPath, sheet_name = 't_0')
    df = pd.read_excel(fullPath, sheet_name = 't_max')
    varNames = np.array(df.keys())
    di = np.array(di)
    df = np.array(df)
    numVar = len(varNames)
    leDict = createDict('data', leDict, {'inocula': di, 'final': df, 'varNames': varNames, 'numVar': numVar})
    # Structures combinations & Tau-N coefficients (`comb`, `coeff`)
    v = np.arange(1, numVar+1)
    nCoef = []
    for i in range(2, numVar+1):
        nameK2 = 'D' + str(i)
        relP = 2/(2**i)     # Reliable point (relP = 2/2^D)
        ## Combinations (`comb`)
        c = np.array(list(_comb(v, i)))
        nc = c.shape[0]
        nCoef.append(nc)
        combDict[nameK2] = c
        ## Coefficients (`coeff`)
        coeffDict[nameK2] = {}
        for i_c in c:
            nameK3_comb = "_".join(varNames[i_c - 1])
            coeffDict[nameK2][nameK3_comb] = {'iD': i_c, 'D': i, 'reliablePoint': relP, 'numObs': [], 'coeffInfo': {'signs1': [], 'signs2': [], 'deltas': [], 'd_pval': [], 'RKtau': [], 'RKt_pval': []}}
    combDict['numcoeff'] = nCoef
    leDict = createDict('comb', leDict, combDict)
    leDict = createDict('coeff', leDict, coeffDict)
    # Save structure
    createDict('saveDict', leDict, fileName)
    print('>> Loading done.')


def loadResults(fileName):
    print('\n>> Loading results ' + '`' + fileName + '.npy`...')
    path = '../../Results/'
    fullPathSave = path + fileName + '.npy'
    readResults = np.load(fullPathSave, allow_pickle = 'TRUE').item()
    print('>> Loading done.')

    return readResults


#-DEBUGGING
# loadData('data-py')
# results = loadResults('data-py')
# print(results)
#----------