# -*- coding: utf-8 -*-
# Copyright 2023 by Eloi Martinez-Rabert.  All rights reserved.
# This code is part of the Python-dna distribution and governed by its
# license.  Please see the LICENSE.txt file that should have been included
# as part of this package.
# doctest: +NORMALIZE_WHITESPACE
# doctest: +SKIP

"""
This module contain functions to get data for various purposes.

- :func:`createDict` creates and saves the dictionary with all information and data sets from Excel File (nameFile.xlsx).

- :func:`loadData` for getting the whole information and data sets from Excel file (nameFile.xlsx). Please see README file for more information.

- :func:`loadResults` for getting the nOEN outcomes of the data set already analysed and plot them.

"""

import os.path
import pandas as pd
import numpy as np
from itertools import combinations as _comb
from itertools import compress

def createDict(mainKeyName, iDict, info):
    """
    - :input:`mainKeyName` (str). Mode of dictionary creation ['data', 'comb', 'coeff', 'saveDict'].
    - :input:`iDict` (dict). Dictionary file.
    - :input:`info` (dict). New information included into dictionary file (iDict).

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
            cDict = loadResults(info)
            if cDict['data']['results'] == True:
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
            np.save(fullPathSave, iDict)
            print(' > Data structure saved - `' + info +'.npy`.')
    else:
        print(' > No expected Structure: `' + mainKeyName + '`')


def loadData(fileName):
    """
    - :input:`fileName` (str). Name of file with data and info.

    """  
    print('\n>> Loading data...')
    path = '../../Results/'
    fullPathFile = path + fileName + '.npy'
    if os.path.isfile(fullPathFile) == True:
        print(' > File `' + fileName + '.npy` with results.')
        rDict = loadResults(fileName)
    else:
        print(' > New file .npy.')
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
        leDict = createDict('data', leDict, {'inocula': di, 'final': df, 'varNames': varNames, 'numVar': numVar, 'results': False})
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
        rDict = loadResults(fileName)
    
    return rDict


def loadResults(fileName):
    path = '../../Results/'
    fullPathSave = path + fileName + '.npy'
    readResults = np.load(fullPathSave, allow_pickle = 'TRUE').item()

    return readResults


def writeResults(fileName, Dim = 0, varSelect = 0):
    """
    - :input:`fileName` (str). Name of file with data and info.
    - :input:`Dim` (list). List with dimensions we want to write (default: 0 -> 'All').

    """
    path = '../../Results/'
    fullPathFile = path + fileName + '.npy'
    fullPathSave = path + fileName + '_results.xlsx'
    if os.path.isfile(fullPathFile) == True:
        if os.path.isfile(fullPathSave) == True:
            val = input(' > Do you want to overwrite `' + fileName + '_results.xlsx`? [Y/N]: ')
        else:
            val = 'Y'
        if val == 'Y' or val == 'y':
            rDict = loadResults(fileName)
            D = rDict['data']['numVar']
            numComb = rDict['comb']['numcoeff']
            print('\n>> Writing results ' + '`' + fileName + '.npy` to `' + fileName + '_results.xlsx`.')
            # Data Sheet
            data = rDict['data']['final']
            varNames = rDict['data']['varNames']
            nd = data.shape[0]
            df = pd.DataFrame(data, columns = varNames.tolist(), index = np.arange(1, nd+1))
            if not varSelect == 0:
                # Check if variable name(s) exists
                cvarNames = np.isin(varSelect, varNames)
                getnotNames = list(compress(varSelect, ~cvarNames))
                if getnotNames:
                    print(' > Variable(s) `' + ' '.join(getnotNames) + '` not found.')
            with pd.ExcelWriter(fullPathSave) as writer:
                df.to_excel(writer, sheet_name='Data')
                if Dim == 0:
                    vD = np.arange(2, D+1)
                else:
                    vD = Dim
                for d in vD:
                    sName = 'D' + str(d)
                    infoR = pd.DataFrame(np.array(['· Dimension ' + str(d), '· Reliable point: ' + str(2/(2**d)), '· Number of observations: ' + str(nd), '· Total number of var combinations: ' + str(numComb[d-2])]))
                    infoR.to_excel(writer, sheet_name = sName, index = False, header = False)
                    headR = ['[ ' + '± ' * d + ']', '[ ' + '∓ ' * d + ']', 'δ coefficients', '𝜏 coefficients', 'p-values']
                    for c in rDict['comb'][sName]:
                        if not varSelect == 0:
                            # Check if variable(s) is present in combination `c`
                            ind = np.array(np.where(np.isin(varNames, varSelect)), dtype = int) + 1
                            checkVar = any(np.isin(c, ind))
                            if checkVar == False:
                                continue
                        sRow = writer.sheets[sName].max_row
                        jvarName = "_".join(varNames[c - 1])
                        dvarName = pd.DataFrame([jvarName])
                        dvarName.to_excel(writer, sheet_name = sName, startrow = sRow+1, index = False, header = False)
                        r = rDict['coeff'][sName][jvarName]['coeffInfo']
                        if d == 2:
                            rM = [r['signs1'][0], r['signs2'][0], '-', r['RKtau'], r['RKt_pval']]
                            R = pd.DataFrame([rM], columns = headR)
                        else:
                            rM = np.array([r['signs1'], r['signs2'], r['deltas'], r['RKtau'], r['RKt_pval']]).T
                            R = pd.DataFrame(rM, columns = headR)
                        R.to_excel(writer, sheet_name = sName, startrow = sRow+2, index = False)
            print('>> Writing done.')
        else:
            print(' > Results not written. If you don\'t want to lose existing results files, change the name of existing Excel or make a copy into another folder before.')
    else:
        print(' > `' + fileName + '.npy` does not exist.')


#-DEBUGGING
# Load results
# loadData('data-py')
# results = loadResults('data-py')
# print(results)
# Write results to Excel
# writeResults('data-py')
#----------