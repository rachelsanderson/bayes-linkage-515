# Bayesian Record Linkage


## How to run this code

```
# writes JSON file with desired params
python json_writer.py L n1 n2 pM pML pUL

# perform bpm gibbs sampling
python bpm_gibbs.py ./Input/param_nMatchXX_LXX.json niters

# analyze draws
python something here
```

## Outputs from code

One Paragraph of project description goes here

## Running code on the Adroit cluster

First, do this locally (may require Duo verification and entering password)

```
scp bpm_gibbs.py json_writer.py gen_data.py NET_ID@adroit.princeton.edu:~
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
* Special thanks to [Suyash Kumar](https://github.com/suyashkumar)
