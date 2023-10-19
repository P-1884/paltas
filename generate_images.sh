#!/bin/bash
module load python
training_directory='pscratch/sd/p/phil1884/Image_Sim_Folders/' #For NERSC
model_directory='pscratch/sd/p/phil1884/Image_Sim_Folders/'
paltas_directory='/global/u2/p/phil1884/paltas/'
python ./paltas/generate.py /global/homes/p/phil1884/paltas/paltas/Configs/Examples/config_LSST.py /$training_directory/training/5 --n 100
