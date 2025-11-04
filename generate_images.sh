#!/bin/bash
#!/usr/bin/env python3

#When running on glamdring, Can use normal (but not comp2 or comp4 as these are old nodes - if they are running then need to specify >30BG of ram so it selects computer nodes 
#it can run on). Can run on blackhole (as long as it says there are '64' nodes in total - the others may be old too). 
#Should be ok to run on any other nodes without this restriction.

###Affix list: "_mu3_B_gamma_-10pct" "_mu3_B_gamma_-1pct" "_mu3_B_theta_E_-10pct" "_mu3_B_theta_E_-1pct" #"_mu3_B_theta_E_1pct" #"_no_subtr_LS_light_mu3" "_goodseeing_mu3" "_no_RSP_mu3" "_no_subtr_mu3" "_mu3" #"_no_subtr_LS_light" #"_goodseeing"  #"_no_RSP" "_no_subtr" "" s

# THIS MUST BE RUN ONE AT A TIME. I CANNOT PUT THIS INTO A FOR-LOOP AS IT WILL CRASH GLAMDRING.
queue='redwood'
affix="_mu3_B_theta_E_-1pct"
addqueue  -c '3hr' -m 80 -q $queue --requeue -g ImGen$affix ./generate_images_sequentially.sh $affix

# $python ./paltas/generate.py ./paltas/Configs/Examples/$test_config_name$affix.py ./quick_image_checks --n 10 --tf_record --h5
# $python ./paltas/generate.py ./paltas/Configs/Examples/config_LensPop_catalogue_no_RSP.py ./quick_image_checks --n 10000 --tf_record --h5
