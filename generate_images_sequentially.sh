#!/bin/bash
#!/usr/bin/env python3

#FAR FASTER TO RUN THIS ON REDWOOD (~5-20MIN EACH) OR BERG (~4-20MIN) THAN NORMAL (~1.5HR EACH) OR BLACKHOLE (4HR EACH).
affix=$1
python="/mnt/users/hollowayp/python114_archive/bin/python3.11"
survey="LSST" #'Euclid_VIS'
folder_name="Example_LP_40"
config_name=config_LSST_Lenspop
test_config_name="config_LensPop_catalogue"
N_test=24249

# #Test Set:
# echo "Starting to generate images for test set $test_config_name $folder_name $affix"
# $python ./paltas/generate.py ./paltas/Configs/Examples/$test_config_name$affix.py /mnt/extraspace/hollowayp/paltas_data/$folder_name$affix/test/ --n $N_test --tf_record --h5

#THESE LOOPS ARE PURPOSELY RUN SEQUENTIALLY SO AS NOT TO CRASH GLAMDRING.
for VARIABLE in {1..1..1}
do
# #Validation Set:
    echo "Starting to generate images for validation set $config_name $folder_name $affix $VARIABLE"
    $python ./paltas/generate.py ./paltas/Configs/Examples/$config_name$affix.py /mnt/extraspace/hollowayp/paltas_data/$folder_name$affix/validation/$VARIABLE --n 50000 --tf_record --h5
done

for VARIABLE in {1..10..1}
do
# #Training Set:
    echo "Starting to generate images for training set $config_name $folder_name $affix $VARIABLE"
    $python ./paltas/generate.py ./paltas/Configs/Examples/$config_name$affix.py /mnt/extraspace/hollowayp/paltas_data/$folder_name$affix/training/$VARIABLE --n 50000 --tf_record --h5
done