# -*- coding: utf-8 -*-
# Copyright 2023 by Eloi Martinez-Rabert.  All rights reserved.
# This code is part of the Python-dna distribution and governed by its
# license.  Please see the LICENSE.txt file that should have been included
# as part of this package.
# doctest: +NORMALIZE_WHITESPACE
# doctest: +SKIP

"""
This module contain functions for plotting the outcomes from nOEN analysis.

- :func:`ecologicalGrid` for ...

- :func:`ecologicalMap` for ...

"""

import warnings
warnings.simplefilter('ignore')

import sys
import os
import shutil

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from getData import extractResults

def ecologicalGrid(fileName, dictR, D = 0, only_sign = False):
    print('\n>> Plotting...')
    path = '../../Results/'
    nameResults = fileName + '_ecologicalGrid'
    fullPath = path + nameResults + '/'
    plotting = True
    if os.path.exists(fullPath):
        val = input(f' > Do you want to overwrite existing plots of `{fullPath}`? [Y/N]: ')
        if val == 'Y' or val == 'y':
            shutil.rmtree(fullPath, ignore_errors=True)
            os.makedirs(fullPath)
        else:
            print(' > Plotting was stopped by the user.')
            return
    else:
        os.makedirs(fullPath)
    if not plotting:
        pass
    print(' > Creating and saving plots...')
    # Extract general data
    nameVar = dictR['data']['varNames']
    numVar = dictR['data']['numVar']
    # Plotting options
    cmap = colors.LinearSegmentedColormap.from_list('', ['orangered', 'white', 'forestgreen'])
    # cmap = plt.colormaps['RdYlGn']
    nTicks = np.arange(0.5, numVar+0.5)
    if D == 0:
        vD = np.arange(2, numVar+1)
    elif isinstance(D, int):
        vD = [D]
    else:
        print(D)
        D.sort()
        vD = list(set(D))
        print(vD)
    for iD in vD:
        D_field = 'D' + str(iD)
        # Extract combinations
        iNumCoeff = dictR['comb']['numcoeff'] 
        combs = dictR['comb'][D_field]
        if iD-1 > len(iNumCoeff):
            print('Error: Requested dimension higher than number of variables.')
            sys.exit()
        if iD == 2:
            # Extract results
            mIota = np.zeros((numVar, numVar))
            mPval = 999.0*np.ones((numVar, numVar))
            mNumObs = -999*np.ones((numVar, numVar), dtype=int)
            for iComb in combs:
                iComb = iComb - 1
                iota, pval, num_obs, _, _, _ = extractResults(dictR, 2, iComb)
                mIota[tuple(iComb)] = iota
                mPval[tuple(iComb)] = pval
                mNumObs[tuple(iComb)] = num_obs
            mIota = mIota.T
            mPval = mPval.T
            mNumObs = mNumObs.T
            # Check if correlation(s) are significative
            check_sign = (mPval[mPval != 0] < 0.051).any()
            if not check_sign and only_sign:
                print(f' > No significant pairwise data trends were found ({iD})' )
            else:
                # p-value labels
                plabels = np.zeros(mPval.shape, dtype = object)
                plabels[mPval == 999.0] = ''
                plabels[mPval > 0.051] = ''
                plabels[(mPval < 0.051) & (mPval > 0.01)] = "▪";
                plabels[(mPval < 0.01) & (mPval > 0.001)] = "▪ ▪";
                plabels[mPval < 0.001] = "▪ ▪ ▪";
                # Number of observations
                mNumObs = np.array(mNumObs, dtype=str)
                mNumObs = np.char.replace(mNumObs, '-999', '')         
                # Plotting Iota (2D)
                fig, ax = plt.subplots()
                # Borders
                for i in range(numVar):
                    plt.plot(np.arange(numVar-(i-1)), i*np.ones(numVar-(i-1)), c = 'k', linewidth = '1.0')
                    plt.plot(i*np.ones(numVar-(i-1)), np.arange(numVar-(i-1)), c = 'k', linewidth = '1.0')
                x = np.arange(numVar + 1)
                y = np.flip(x)
                colormesh = ax.pcolormesh(x, y, mIota.astype(float), cmap = cmap, vmin = -1, vmax = 1)
                cbar = fig.colorbar(colormesh)
                cbar.set_label('$ι_{2}$')
                plt.xticks(nTicks, nameVar)
                plt.yticks(nTicks, np.flip(nameVar))
                # p-values labels
                for i in range(numVar):
                    for j in range(numVar):
                        fig.text((i+0.5)/(numVar), (numVar-j-1+0.5)/numVar, plabels[j,i], horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
                fig.tight_layout()
                fig.savefig(fullPath + f'ecoGrid_{D_field}_iota', bbox_inches='tight')
                plt.close()
                # Plot number of observations
                fig, ax = plt.subplots()
                # Borders
                for i in range(numVar):
                    plt.plot(np.arange(numVar-(i-1)), i*np.ones(numVar-(i-1)), c = 'grey', linewidth = '1.0')
                    plt.plot(i*np.ones(numVar-(i-1)), np.arange(numVar-(i-1)), c = 'grey', linewidth = '1.0')
                mZ = np.zeros(mIota.shape)
                colormesh = ax.pcolormesh(x, y, mZ.astype(float), cmap = cmap, vmin = -1, vmax = 1)
                plt.xticks(nTicks, nameVar)
                plt.yticks(nTicks, np.flip(nameVar))
                for i in range(numVar):
                    for j in range(numVar):
                        fig.text((i+0.5)/(numVar), (numVar-j-1+0.5)/numVar, mNumObs[j,i], horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
                fig.tight_layout()
                fig.savefig(fullPath + f'ecoGrid_{D_field}_numObs', bbox_inches='tight')
                plt.close()
        else:
            num_Oh = int(2**(iD) / 2);
            nTicks = np.arange(0.5, num_Oh+0.5)
            for iComb in combs:
                iComb = iComb - 1
                iNames = nameVar[iComb].astype(str)
                cleanNames = str(iNames)
                cleanNames = cleanNames.replace('[', '')
                cleanNames = cleanNames.replace(']', '')
                cleanNames = cleanNames.replace("'", '')
                mIota, mPval, num_obs, _, mSymU, mSymD = extractResults(dictR, iD, iComb)
                # Check if correlation(s) are significative
                check_sign = (mPval[mPval != 0] < 0.051).any()
                if not check_sign and only_sign:
                    print(f' > No significant data trends were found for [{cleanNames}] (D{iD}) | min(p-value) = {min(mPval)}; n = {num_obs}.' )
                else:
                    mSym = [mSymU, mSymD]
                    mSym = np.char.replace(mSym, ['['], [''])
                    mSym = np.char.replace(mSym, [']'], [''])
                    mSym = np.char.replace(mSym, ['+'], ['↑'])
                    mSym = np.char.replace(mSym, ['-'], ['↓'])
                    mSymU = mSym[0, :]
                    mSymD = mSym[1, :]
                    # Plot labels
                    leftLSym = []
                    rightLSym = []
                    for i in range(len(mSymU)):
                        SymU = mSymU[i].split()
                        SymD = mSymD[i].split()
                        leftLSym.append(''.join(i+j+' ' for i, j in zip(SymU, iNames)))
                        rightLSym.append(''.join(i+j+' ' for i, j in zip(SymD, iNames)))
                    LSym = []
                    for i in range(num_Oh):
                        LSym.append(leftLSym[i] + '\n' + rightLSym[i])
                    plabels = np.zeros(mPval.shape, dtype = object)
                    plabels[mPval > 0.051] = ''
                    plabels[(mPval < 0.051) & (mPval > 0.01)] = "▪";
                    plabels[(mPval < 0.01) & (mPval > 0.001)] = "▪ ▪";
                    plabels[mPval < 0.001] = "▪ ▪ ▪";
                    # Title
                    title_ = f'{cleanNames} | # observations: {num_obs}'
                    # Plotting Iota (nD)
                    fig, ax = plt.subplots(figsize=(2, num_Oh*1.45))
                    colormesh = ax.pcolormesh(np.array([mIota.astype(float)]).T, cmap = cmap, vmin = -1, vmax = 1)
                    cbar = fig.colorbar(colormesh, pad = 0.1)
                    cbar.set_label('$ι_{2}$')
                    ax.invert_yaxis()
                    plt.title(title_, fontweight="bold", pad = 15)
                    plt.yticks(nTicks, LSym)
                    plt.tick_params(axis='x', which='both', bottom=False, top=False,labelbottom=False)
                    # Borders
                    for i in range(num_Oh):
                        plt.hlines(i, 0.0, 1.0, colors = 'k', linewidth=1)
                    # p-values labels
                    for i in range(num_Oh):
                            fig.text(0.5, (num_Oh-i-1+0.5)/num_Oh, plabels[i], horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
                    fig.tight_layout()
                    fileNames = cleanNames.replace(' ', '_')
                    fig.savefig(fullPath + f'ecoGrid_{D_field}_{fileNames}.png', bbox_inches='tight')
                    plt.close()
    print('>> Plotting done.')