#!/bin/bash
#SBATCH -p test
#SBATCH -N 1
#SBATCH -n 6
#SBATCH -t 6:00:00
#SBATCH --mem-per-cpu 12000
#SBATCH --job-name preprocess_re5pe3

. $HOME/miniconda_new/etc/profile.d/conda.sh
conda activate vtki

# -u flushes print() buffer so we can see output during processing

#python -u ./preprocess_vtk.py --case re5pe1 --thin 5 2>&1 > preprocess_re5pe1.log
python -u ./preprocess_vtk.py --case re5pe3 --thin 5  2>&1 > preprocess_re5pe3.log

#python -u ./preprocess_vtk.py --case re10pe1 --thin 5  2>&1 > preprocess_re10pe1.log
#python -u ./preprocess_vtk.py --case re10pe3 --thin 5  2>&1 > preprocess_re10pe3.log
