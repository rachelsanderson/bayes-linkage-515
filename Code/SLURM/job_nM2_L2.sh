#!/bin/sh
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=10:01:00
#SBATCH --mail-type=begin
#SBATCH --mail-type=end
#SBATCH --mail-user=rachelsa@princeton.edu
module load python
module load anaconda3/5.3.1 
python json_writer.py nM2_L2 2 10 10 0.2 0.9 0.2

python gen_data.py ./Input/param_nM2_L2.json nM2_L2
python simple_gibbs.py ./Input/Gamma_nM2_L2.csv nM2_L2 100000  >> ./Output/simple_gibbs_nM2_L2.txt 
python bpm_gibbs.py ./Input/param_nM2_L2.json ./Input/Gamma_nM2_L2.csv 100000
