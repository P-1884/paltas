#!/bin/bash
#SBATCH -A m1727
#SBATCH -C cpu
#SBATCH --qos=regular
#SBATCH --time=120
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
for V in {1..1..1}
do
srun /global/u2/p/phil1884/paltas/generate_images.sh
done
