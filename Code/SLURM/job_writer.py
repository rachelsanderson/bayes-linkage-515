# import pandas
import os
import sys

header = ["#!/bin/sh\n", "#SBATCH --nodes=1\n","#SBATCH --ntasks-per-node=1\n",\
    "#SBATCH --time=10:01:00\n", "#SBATCH --mail-type=begin\n", "#SBATCH --mail-type=end\n",\
    "#SBATCH --mail-user=rachelsa@princeton.edu\n", "module load python\n", "module load anaconda3/5.3.1 \n"]

def write_file(line, niters):
        inputs = line.replace(',', ' ')
        temp = line.split(",")
        L = temp[0]
        nM = int(int(temp[1])*float(temp[3]))
        ext = 'nM' + str(nM) + '_L' + L

        paramFile = "./Input/param_" + ext + ".json"
        gammaFile = "./Input/Gamma_" + ext + ".csv"
        jobFile = "job_" + ext

        file = open(jobFile+'.sh', 'w')

        file.writelines(header)
        file.writelines("python json_writer.py " + ext + " " + inputs + "\n")
        file.writelines("python gen_data.py " + paramFile + " " + ext + "\n")
        file.writelines("python simple_gibbs.py " + gammaFile + " " + ext + " " + str(niters) + "  >> ./Output/simple_gibbs_" + ext + '.txt \n')
        file.writelines("python bpm_gibbs.py " + paramFile + " " + gammaFile + " " + str(niters) +  "\n")
        file.close()

if __name__ == '__main__':
    filePath = sys.argv[1]
    niters = sys.argv[2]
    with open(filePath) as inputFile:
        line=inputFile.readline()
        cnt = 0
        while line:
            print("line {}: {}".format(cnt,line.strip()))
            if (cnt != 0 ):
                write_file(line, niters)
            line = inputFile.readline()
            cnt+=1
        # write_file()
