#!/bin/bash
#!/usr/bin/env python3

survey="LSST" #'Euclid_VIS' # #
for affix in "_no_subtr_LS_light" "" "_no_RSP" "_no_subtr"
do 
    folder_name="Example_LP_17${affix}" #"Example_Eu_2"
    config_name="config_${survey}_Lenspop${affix}.py"
    test_config_name="config_LensPop_catalogue${affix}.py"
    test_image_dir="/mnt/extraspace/hollowayp/paltas_data/${folder_name}/test"
    python="/mnt/users/hollowayp/python11_env_new/bin/python3.11"
    N_test=200 #Need to run LensPop for longer to get more subjects.
    addqueue -c '1hr' -m 12 -q normal  /mnt/users/hollowayp/python11_env_new/bin/python3.11 ./paltas/generate.py ./paltas/Configs/Examples/$test_config_name $test_image_dir --n $N_test
    #When running on glamdring, Can use normal (but not comp2 or comp4 as these are old nodes - if they are running then need to specify >30BG of ram so it selects computer nodes it can run on). Can run on blackhole (as long as it says there are '64' nodes in total - the others may be old too). Should be ok to run on any other nodes without this restriction.
    #FAR FASTER TO RUN THIS ON REDWOOD (~5-20MIN EACH) OR BERG (~4-20MIN) THAN NORMAL (~1.5HR EACH) OR BLACKHOLE (4HR EACH).
    for VARIABLE in {1..1..1}
    do
        addqueue -c '5mins' -m 12 -q normal $python ./paltas/generate.py ./paltas/Configs/Examples/$config_name /mnt/extraspace/hollowayp/paltas_data/$folder_name/validation/$VARIABLE --n 5000 --tf_record --h5
    done
    for VARIABLE in {1..10..1}
    do
        addqueue -c '1hr' -m 12 -q normal $python ./paltas/generate.py ./paltas/Configs/Examples/$config_name /mnt/extraspace/hollowayp/paltas_data/$folder_name/training/$VARIABLE --n 50000 --tf_record --h5
    done
done
