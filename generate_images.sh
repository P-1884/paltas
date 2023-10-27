#!/bin/bash
#!/usr/bin/env python3
folder_name='Example_SL_3'
config_name='config_Simpipeline.py'
#When running on glamdring, Can use normal (but not comp2 or comp4 as these are old nodes - if they are running then need to specify >30BG of ram so it selects computer nodes it can run on). Can run on blackhole (as long as it says there are '64' nodes in total - the others may be old too). Should be ok to run on any other nodes without this restriction.
for VARIABLE in {1..1..1}
do
    addqueue -c '45min' -m 8 /usr/bin/python3 ./paltas/generate.py ./paltas/Configs/Examples/$config_name /mnt/extraspace/hollowayp/paltas_data/$folder_name/validation/$VARIABLE --n 500 --tf_record --h5

done

for VARIABLE in {1..50..1}
do
    addqueue -c '45min' -m 8 /usr/bin/python3 ./paltas/generate.py ./paltas/Configs/Examples/$config_name /mnt/extraspace/hollowayp/paltas_data/$folder_name/training/$VARIABLE --n 500 --tf_record --h5

done

for VARIABLE in {50..100..1}
do
    addqueue -c '45min' -q blackhole -m 8 /usr/bin/python3 ./paltas/generate.py ./paltas/Configs/Examples/$config_name /mnt/extraspace/hollowayp/paltas_data/$folder_name/training/$VARIABLE --n 500 --tf_record --h5

done

# for VARIABLE in {25..50..1}
# do
#     addqueue -c '45min' -m 8 -n 1 -s -q blackhole /usr/bin/python3 ./paltas/generate.py ./paltas/Configs/Examples/$config_name /mnt/extraspace/hollowayp/paltas_data/$folder_name/training/$VARIABLE --n 500 --tf_record --h5

# done

# for VARIABLE in {50..75..1}
# do
#     addqueue -c '45min' -m 8 -n 1 -s -q blackhole /usr/bin/python3 ./paltas/generate.py ./paltas/Configs/Examples/$config_name /mnt/extraspace/hollowayp/paltas_data/$folder_name/training/$VARIABLE --n 500 --tf_record --h5

# done

# for VARIABLE in {75..100..1}
# do
#     addqueue -c '45min' -m 8 -n 1 -s -q blackhole /usr/bin/python3 ./paltas/generate.py ./paltas/Configs/Examples/$config_name /mnt/extraspace/hollowayp/paltas_data/$folder_name/training/$VARIABLE --n 500 --tf_record --h5

# done

# module load python
# training_directory='pscratch/sd/p/phil1884/Image_Sim_Folders/' #For NERSC
# model_directory='pscratch/sd/p/phil1884/Image_Sim_Folders/'
# paltas_directory='/global/u2/p/phil1884/paltas/'
# python ./paltas/generate.py /global/homes/p/phil1884/paltas/paltas/Configs/Examples/config_LSST.py /$training_directory/training/5 --n 100

#addqueue -c '45min' -m 8 -n 1 -s -q normal /usr/bin/python3 ./paltas/generate.py ./paltas/Configs/Examples/config_LSST.py /mnt/extraspace/hollowayp/paltas_data/Example_K/validation/1 --n 100 --tf_record --h5
