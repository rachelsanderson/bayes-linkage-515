import numpy as np
import pandas as pd
import json
import sys

dir = '.'
inputDir = dir + '/Input/'

### returns true BPM and Gamma matrix for calculations
def make_Gamma(pM, pML, pUL, n1, n2, L):

    Z = make_Z(pM,n1,n2) # true BPM

    iVals, jVals, Zvals = make_pairs(Z, n1,n2) # for i,j column
    Gamma = pd.DataFrame({'i': iVals, 'j':jVals, 'Z': Zvals})
    Gamma['match'] = False
    Gamma.loc[Gamma['Z']==Gamma['j'], 'match'] = True

    # make actual comparison vectors
    Gamma['gamma'] = Gamma['match'].apply((lambda x: make_gamma(pML,pUL,x)))

    return Z, Gamma

#### makes true BPM configuration
def make_Z(pM, n1, n2):

    # Assign match status to nM = pM * n2 records
    nM = int(pM * n2)
    matchX2 = np.random.choice(n2, nM, replace=False)

    # Select nM records from n1 and assign those to matches
    matchX1 = np.random.choice(n1, nM, replace=False)

    Z = [i + n1 for i in np.arange(n2)]
    for (index, j) in enumerate(matchX2):
        Z[j] = matchX1[index]

    return Z

#### makes i,j, Z columns in Gamma df
def make_pairs(Z,n1,n2):

    i = [[i]*n1 for i in range(n2)]
    iVals = []
    for x in i:
        iVals += x
    jVals = [j for j in range(n1)] * n2
    Zvals = [Z[x] for x in iVals]
    return iVals, jVals, Zvals

## makes comparison vector gamma for each i,j pair
def make_gamma(pML, pUL, x):
    L = len(pML)
    if x == True:
        return np.random.binomial(1,pML, size=L)
    else:
        return np.random.binomial(1,pUL, size=L)

## CALL THIS FROM THE COMMAND LINE:

if __name__ == "__main__":
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        params = json.load(f)

    # read in params
    L= params['L']
    n1 = params['n1']
    n2 = params['n2']
    pML = params['pML']
    pUL = params['pUL']
    pM = params['pM']

    Z_true, Gamma = make_Gamma(pM, pML, pUL, n1, n2, L)

    # Save it for future analysis
    ext = sys.argv[2]
    gammaName = 'Gamma_' + ext + '.csv'
    Zname = 'Ztrue_' + ext + '.csv'
    Gamma.to_csv(inputDir+gammaName, mode='w')
    pd.DataFrame(Z_true).to_csv(inputDir+Zname, mode='w')
