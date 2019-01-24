# Bayesian Record Linkage

Code for implementing the analysis performed in "Bayesian Record Linkage" by Rachel Anderson (2019).

## Python scripts

* *json_writer.py* - Takes as input parameters length of comparison vector (*L*), size of files (*n1,n2*), and initial parameters for Gibbs sampler.  Outputs JSON file "param_" + *ext* and saves in Input folder

* *gen_data.py* - Takes as inputs "true" (*pM, pML, pUL*) and generates a DataFrame with record pair identifiers *i,j*, true match status, and comparison vector *gamma*.    

* *simple_gibbs.py* - Performs Gibbs sampling according to mixture model of record linkage.  Outputs frequency of matches as a text file and a .csv file of parameter values for (*pM, pML, pUL*).

* *bpm_gibbs.py* - Performs Gibbs sampling according to the bipartite matching model in Sadinle (2017) using the steps outlined in Larsen (2005).  Outputs .csv files for *Z_trace* and *trace* which contain draws for the matching labeling *Z* and (*pM,pML,pUL*).


## SLURM

## How to run this code

```
# writes JSON file with desired params
python json_writer.py L n1 n2 pM pML pUL

# analyze draws w/mixture model
python simple_gibbs.py ./Input/Gamma_nMXX_LXX.csv niters

# perform beta record linkage
python bpm_gibbs.py ./Input/param_nMXX_LXX.json ./Input/Gamma_nMXX_LXX.csv niters
```

## Outputs from code

One Paragraph of project description goes here

## Running code on the Adroit cluster

First, do this locally (may require Duo verification and entering password)

```
scp simple_gibbs.py bpm_gibbs.py json_writer.py gen_data.py NET_ID@adroit.princeton.edu:~
```

Then ssh into the cluster by typing in

```
ssh NET_ID@adroit.princeton.edu
```
To run the code on the cluster, type:
```
# loads modules for scipy, etc.
module load python
module load anaconda3/5.3.1
```
and then follow the steps above.

## SLURM on the cloud

My code includes a number of slurm files (suffix .sh) which can be used to submit batches to the cluster.  I use this for my large computations.

## Authors

* **Rachel Anderson **  - *Initial work* - [Github](https://github.com/rachelsanderson)


## Acknowledgments

* Many thanks to Mauricio Sadinle and Ted Enamorado for sharing data and code.
* Special thanks to [Suyash Kumar](https://github.com/suyashkumar) for the technical and moral support
