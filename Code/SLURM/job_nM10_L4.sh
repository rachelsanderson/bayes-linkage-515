#!/bin/sh
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=10:01:00
#SBATCH --mail-type=begin
#SBATCH --mail-type=end
#SBATCH --mail-user=rachelsa@princeton.edu
module load python
module load anaconda3/5.3.1 
python json_writer.py nM10_L4 4 20 20 0.5 0.9 0.2

python gen_data.py ./Input/param_nM10_L4.json nM10_L4
python simple_gibbs.py ./Input/Gamma_nM10_L4.csv nM10_L4 100000  >> ./Output/simple_gibbs_nM10_L4.txt 
python bpm_gibbs.py ./Input/param_nM10_L4.json ./Input/Gamma_nM10_L4.csv 100000
