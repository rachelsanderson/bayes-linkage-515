import numpy as np
from scipy.stats import bernoulli
import pandas as pd
import itertools
import time
import sys
import os

outputDir = './Output/'

# Functions for updating I(a,b)
def column(matrix, i):
    return [row[i] for row in matrix]

def calc_pGammaM(gammaInd,pML):
    # returns log(pGamma_ij | M)
    # assert len(gammaInd) == len(pML), 'dim do not match'
    return np.sum([gammaInd[l]*np.log(pML[l]) + (1-gammaInd[l])*np.log(1-pML[l]) for l in range(len(pML))])

def calc_pGammaU(gammaInd,pUL):
    # returns log(pGamma_ij | U)
    # assert len(gammaInd) == len(pUL), 'dim do not match'
    return np.sum([gammaInd[l]*np.log(pUL[l]) + (1-gammaInd[l])*np.log(1-pUL[l]) for l in range(len(pUL))])

def sample_I(gamma, pM, pML, pUL):
    nPairs = len(gamma)  #number of comparisons
    L = len(pML) # num categories

    prGamma_M = np.array([calc_pGammaM(pair, pML) for pair in gamma])
    prGamma_U = np.array([calc_pGammaU(pair, pML) for pair in gamma])

    num = L*np.log(pM)*np.ones(nPairs) + prGamma_M
    denom = L*np.log(1-pM)*np.ones(nPairs)+prGamma_U

    ps = np.exp(num)/(np.exp(num) + np.exp(denom))

    return np.array([np.random.binomial(1,p=ps[i]) for i in range(len(ps))])

def sample_pM(I, aM, bM):
    nM = np.sum(I)
    aNew = aM + nM
    bNew = bM + len(I) - nM
    return np.random.beta(aNew,bNew)

def sample_pML(gammaL, I, aML, bML):
    N = len(gammaL)
    assert N == len(I), 'dimensions don\'t match'
    ones = np.array([1] * N)
    aML_new = aML + np.sum(I * gammaL)
    bML_new = bML + np.sum(I * (ones-gammaL))
    return np.random.beta(aML_new,bML_new)

def sample_pUL(gammaL, I, aUL, bUL):
    N = len(gammaL)
    assert N == len(I), 'dimensions don\'t match'
    ones = np.array([1] * N)
    aUL_new = aUL + np.sum((ones-I) * gammaL)
    bUL_new = bUL + np.sum((ones-I) * (ones-gammaL))
    return np.random.beta(aUL_new,bUL_new)

def gibbs(gamma, iters, init, hypers):

    assert len(gamma[0]) == len(init["pML"]), 'not enough params' # checks sufficiently parameterized
    assert len(init["pML"]) == len(init["pUL"]), 'dimensions of pML and pUL do not match'

    pM = init["pM"]
    pML = init["pML"]
    pUL = init["pUL"]
    nPar = 1 + len(pML) + len(pUL)

    L = len(pML)
    numPair = len(gamma)

    trace = np.zeros((iters,nPar)) # trace to store values of pM, pML, pUL
    I_sum = np.zeros(numPair)      # storage for matches

    for it in range(iters):
        # print((pM, pML, pUL))
        I = sample_I(gamma, pM, pML, pUL)

        pM = sample_pM(I, hypers['aM'], hypers['bM'])
        # Need some way to correct when it goes on a spree
#         if pM > 0.99:
#             pM = 0.05
        # delete above, but need something like it
        pML = [sample_pML(column(gamma,l), I, hypers['aML'][l], hypers['bML'][l]) for l in range(L)]
        pUL = [sample_pUL(column(gamma,l), I, hypers['aUL'][l], hypers['bUL'][l]) for l in range(L)]

        # update mcmc trace
        I_sum += I
        trace[it,:] = np.append(np.append(pM, pML),pUL)

    trace = pd.DataFrame(trace)

    pML_names = ['pML_' + str(i) for i in range(1,L+1)]
    pUL_names = ['pUL_' + str(i) for i in range(1,L+1)]

    trace.columns= ['pM'] + pML_names + pUL_names

    print(I_sum)
    return trace, I_sum


if __name__ == '__main__':

    # read in gamma files
    Gamma = pd.read_csv(sys.argv[1])

    gamma = Gamma['gamma'].apply(lambda x: x.replace(" ",","))
    gamma = gamma.apply(lambda x: eval(x))
    gamma = gamma.tolist()
    L = len(gamma[0])

    ext = sys.argv[2]
    # set number of iters
    niters = int(sys.argv[3])

    # init and hypers are fixed
    init = {"pM": 0.5,
            "pML": [0.5]*L,
            "pUL": [0.5]*L}

    ## specify hyper parameters
    hypers = {"aM": 1,
              "bM": 1,
              "aML": [1]*L,
              "bML": [1]*L,
              "aUL": [1]*L,
              "bUL": [1]*L}

    start = time.time()
    trace, i = gibbs(gamma, niters, init, hypers)
    end = time.time()

    trace.to_csv(outputDir + 'trace_' + ext + '.csv', mode = 'w')
    print('Time to perform ' + str(niters) + ' for ' + str(len(gamma)) + ' pairs, L = '\
        + str(L) + ' is ' + str(round(end-start,3)) + ' seconds')
