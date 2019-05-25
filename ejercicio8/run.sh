#!/bin/bash

#SBATCH --job-name=red_neuronal_1
#SBATCH --ntasks=1
#SBATCH --mem=16384
#SBATCH --time=48:00:00
#SBATCH --tmp=16G
#SBATCH --partition=normal
#SBATCH --mail-type=ALL
#SBATCH --mail-user=ignacioferre@gmail.com

source /python_env/bin/activate

cd AA/aa2019-lab5/ejercicio8
python3 Training.py Training.conf
