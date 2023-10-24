#!/bin/bash
#!/usr/bin/env python3

for VARIABLE in {1..2..1}
do
    addqueue -c '45min' -m 8 -n 1 -s -q normal /usr/bin/python3 ./paltas/generate.py ./paltas/Configs/Examples/config_simple.py /mnt/extraspace/hollowayp/paltas_data/Example_A/validation/$VARIABLE --n 500 --tf_record --h5

done

for VARIABLE in {1..50..1}
do
    addqueue -c '45min' -m 8 -n 1 -s -q normal /usr/bin/python3 ./paltas/generate.py ./paltas/Configs/Examples/config_simple.py /mnt/extraspace/hollowayp/paltas_data/Example_A/training/$VARIABLE --n 500 --tf_record --h5

done

for VARIABLE in {25..50..1}
do
    addqueue -c '45min' -m 8 -n 1 -s -q redwood /usr/bin/python3 ./paltas/generate.py ./paltas/Configs/Examples/config_simple.py /mnt/extraspace/hollowayp/paltas_data/Example_A/training/$VARIABLE --n 500 --tf_record --h5

done

for VARIABLE in {50..75..1}
do
    addqueue -c '45min' -m 8 -n 1 -s -q blackhole /usr/bin/python3 ./paltas/generate.py ./paltas/Configs/Examples/config_simple.py /mnt/extraspace/hollowayp/paltas_data/Example_A/training/$VARIABLE --n 500 --tf_record --h5

done

for VARIABLE in {75..100..1}
do
    addqueue -c '45min' -m 8 -n 1 -s -q cmb /usr/bin/python3 ./paltas/generate.py ./paltas/Configs/Examples/config_simple.py /mnt/extraspace/hollowayp/paltas_data/Example_A/training/$VARIABLE --n 500 --tf_record --h5

done


#for v in {683786..683836..1}
#do
#  echo $v
#  scancel $v
#done
module load python
training_directory='pscratch/sd/p/phil1884/Image_Sim_Folders/' #For NERSC
model_directory='pscratch/sd/p/phil1884/Image_Sim_Folders/'
paltas_directory='/global/u2/p/phil1884/paltas/'
python ./paltas/generate.py /global/homes/p/phil1884/paltas/paltas/Configs/Examples/config_LSST.py /$training_directory/training/5 --n 100
