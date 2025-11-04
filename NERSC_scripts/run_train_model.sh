#!/bin/bash
#SBATCH -C gpu
#SBATCH -q shared
#SBATCH -t 5
#SBATCH -n 1
#SBATCH -c 32
#SBATCH --gpus-per-task=1
export SLURM_CPU_BIND="cores"
for V in {1..1..1}
do
srun /global/u2/p/phil1884/paltas/train_model.sh
done

