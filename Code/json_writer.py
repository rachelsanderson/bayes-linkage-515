import json
import sys

dir = '.'
inputDir = dir + '/Input/'

def write_params(ext, L,n1,n2,pM,pML,pUL):
    params = {}
    params['L'] = L
    params['init'] = {"pM": 0.5,
                      "pML": [0.5]*L,
                       "pUL": [0.5]*L}
    params['hypers'] = {"aM": 1,
                "bM": 1,
                "aML": [1]*L,
                "bML": [1]*L,
                "aUL": [1]*L,
                "bUL": [1]*L}
    params['n1'] = n1
    params['n2'] = n2
    params['pM'] = pM
    params['pML'] = [pML] * L
    params['pUL'] = [pUL] * L

    fileName = inputDir + 'param_' + ext + '.json'

    with open(fileName,'w') as outfile:
        json.dump(params,outfile)
    return fileName

if __name__ == '__main__':
    ext = sys.argv[1]
    L  = int(sys.argv[2])
    n1 = int(sys.argv[3])
    n2 = int(sys.argv[4])
    pM = float(sys.argv[5])
    pML = float(sys.argv[6])
    pUL = float(sys.argv[7])
    write_params(ext,L,n1,n2,pM,pML,pUL)
