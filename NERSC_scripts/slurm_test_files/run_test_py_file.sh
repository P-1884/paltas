#!/bin/bash
#SBATCH --qos=debug
#SBATCH --time=5
#SBATCH --nodes=1
#SBATCH --constraint=cpu
#SBATCH --ntasks-per-node=1
#SBATCH -A m1727
srun ./test_py_file.sh
