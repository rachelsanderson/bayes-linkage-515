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


## Authors

* **Rachel Anderson **  - *Initial work* - [Github](https://github.com/rachelsanderson)


## Acknowledgments

* Many thanks to Mauricio Sadinle and Ted Enamorado for sharing data and code.
* Special thanks to [Suyash Kumar](https://github.com/suyashkumar)
