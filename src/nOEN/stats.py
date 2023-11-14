# -*- coding: utf-8 -*-
# Copyright 2023 by Eloi Martinez-Rabert.  All rights reserved.
# This code is part of the Python-dna distribution and governed by its
# license.  Please see the LICENSE.txt file that should have been included
# as part of this package.
# doctest: +NORMALIZE_WHITESPACE
# doctest: +SKIP

"""
This module contain functions to perform multivariate rank correlation coefficient.

- :func:`formalism_Oh` for the computation of the summation of individual data trend coefficient calculation

- :func:`multivarcorr` for the calculus of Tau-N coefficients

- :func:`nOEN` for n-Order Ecological Network analysis (nOEN)

"""

import numpy as np
import math
from scipy.stats import norm, gmean
from itertools import product, permutations

from getData import loadResults, createDict

def formalism_Oh(N, numObs, dataset, paired_Oh, binomial):
    """
    - :input:`N` (int). Number of paired orthants and delta coefficients
    - :input:`numObs` (int). Number of observations
    - :input:`paired_Oh` (np.array). Signs of each paired orthant
    - :input:`binomial` (int). Binomial coefficient

    """
    # Definition of variables
    F = np.empty((0), int)
    symbolMatrix_up = np.empty((0), str)
    symbolMatrix_down = np.empty((0), str)
    # Summation
    for i in range(0, N):
        binomial_untied = int(binomial)
        i_pOh = np.vstack((paired_Oh[0, i, :], paired_Oh[1, i, :]))        
        f = 0
        for jj in range(1, numObs):
            for ii in range(0, jj):
                diff = dataset[jj, :] - dataset[ii, :]
                # Tied data detection
                if not all(diff):
                    binomial_untied -= 1
                    continue
                f += int(np.logical_or(all(np.equal(i_pOh[0, :], np.greater(diff, 0))), all(np.equal(i_pOh[1, :], np.greater(diff, 0)))))
        F = np.append(F, [f])
        # Symbol assignment
        s_up = np.char.replace(str(i_pOh[0, :]), '1', '+'); 
        s_up = np.char.replace(s_up, '0', '-')
        s_down = np.char.replace(str(i_pOh[1, :]), '1', '+')
        s_down = np.char.replace(s_down, '0', '-')
        symbolMatrix_up = np.append(symbolMatrix_up, [s_up])
        symbolMatrix_down = np.append(symbolMatrix_down, [s_down])

    return (F, symbolMatrix_up, symbolMatrix_down, binomial_untied)


def multivarcorr(D, dataset, numObs):
    """
    - :input:`D` (int). Dimension/number of joint variables
    - :input:`dataset` (np.array).
    - :input:`numObs` (int). Number of observations

    """
    binomial = math.comb(numObs, 2)                                 # Binomial coeficient
    N = int(2**D/2)                                                 # Number of paired orthants and delta coefficients
    # Signs permutations with repetitions
    signs = [1, 0]                                                  # 1: Positive / 0: Negative
    sC = np.fliplr(np.array(list(product(signs, repeat=D))))        # np.fliplr() to have same sign order as MATLAB
    # Paired orthants matrix (3D: [2xNxD])
    pOh1 = sC[0:N, :]
    pOh2 = np.flipud(sC[-N:])
    paired_Oh = np.stack([pOh1, pOh2])
    # Delta coefficients
    F, symbolMatrix_up, symbolMatrix_down, binomial_untied = formalism_Oh(N, numObs, dataset, paired_Oh, binomial)
    deltas = (1 / binomial_untied) * F
    # p-value (deltas)
    var = (2 * (2 * numObs + 5)) / (9 * numObs * (numObs - 1))
    d_Zt = deltas / math.sqrt(var)
    d_pval = 2 * norm.cdf(-abs(d_Zt))
    # Rabert-Kendall's Tau
    if D == 2:
        RKtau = deltas[0] - deltas[1]
    else:
        RKtau_comb = np.empty([0, 2], dtype=int)
        for t in np.array(list(product(np.arange(0, N, dtype=int), repeat=2))):
            if not np.all(t == t[0]):
                RKtau_comb = np.append(RKtau_comb, [t], axis=0)     # Combinations of paired orthants
        d_diff = (1 + (deltas[RKtau_comb[:, 0]] - deltas[RKtau_comb[:, 1]]))
        deltas_diff = d_diff.reshape(N-1, N, order='F').copy()
        RKtau = (gmean(deltas_diff)-1).transpose()
    RK_Zt = RKtau / math.sqrt(var)
    RKt_pval = 2 * norm.cdf(-abs(RK_Zt))

    return (RKtau, RKt_pval, deltas, d_pval, symbolMatrix_up, symbolMatrix_down)


def nOEN(dDict, Dim = 'All', infoInocula = False):
    """
    - :input:`dDict` (dict). Dictionary with dataset and information
    - :input:`Dim` (list). List with dimensions we want to test (default: 'All')
    - :input:`infoInocula` (bool). Boolen to indicate if dataset include information at time 0 (i.e., inocula)
    
    """
    print('\n>> Running nOEN...')
    # Access data
    numVar = dDict['data']['numVar']
    varNames = dDict['data']['varNames']
    
    if Dim == 'All' or Dim == 'all':
        vD = np.arange(2, numVar+1)
    else:
        vD = Dim
    for d in vD:
        D_field = 'D' + str(d)
        combi = dDict['comb'][D_field]
        nCombi = combi.shape[0]
        for c in range(0, nCombi):
            iVar = list(dDict['coeff'][D_field].keys())[c]
            iCombi = combi[c] - 1       # Python arrays starts with position 0, not 1
            nameK3_comb = "_".join(varNames[iCombi])
            data = dDict['data']['final'][:, iCombi]
            if infoInocula:
                # Select those observations with all variables in inocula
                dataInocula = dDict['data']['inocula'][:, iCombi]
                data = data[np.all(dataInocula, axis = 1), :]
            numObs = data.shape[0]
            if numObs < 2:
                print('!UserWarning: Not enough number of observations in ' + iVar +' dataset (D=' + str(d) +')')
            else:
                RKtau, RKt_pval, deltas, d_pval, symbolMatrix_up, symbolMatrix_down = multivarcorr(d, data, numObs)
                dDict['coeff'][D_field][nameK3_comb]['numObs'] = numObs
                dDict['coeff'][D_field][nameK3_comb]['coeffInfo']['signs1'] = symbolMatrix_up
                dDict['coeff'][D_field][nameK3_comb]['coeffInfo']['signs2'] = symbolMatrix_down
                dDict['coeff'][D_field][nameK3_comb]['coeffInfo']['deltas'] = deltas
                dDict['coeff'][D_field][nameK3_comb]['coeffInfo']['d_pval'] = d_pval
                dDict['coeff'][D_field][nameK3_comb]['coeffInfo']['RKtau'] = RKtau
                dDict['coeff'][D_field][nameK3_comb]['coeffInfo']['RKt_pval'] = RKt_pval
    print('>> nOEN done.')
    
    return dDict


#-DEBUGGING
# # Load data and nOEN execution
# results = loadResults('data-py')
# leDict = nOEN(results, 'All', True)
# # Save structure
# createDict('saveDict', leDict, 'data-py')
# print(leDict)
#----------