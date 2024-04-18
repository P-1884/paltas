
for affix in "" "_no_RSP" "_no_subtr"
do
addqueue -c '3days' -m 6 -n 1x4 -s -q gpulong --gputype rtx2080with12gb /mnt/users/hollowayp/python11_env_new/bin/python3.11 /mnt/users/hollowayp/paltas/paltas/Analysis/train_model.py /mnt/users/hollowayp/paltas/paltas/Analysis/AnalysisConfigs/train_config_LSST_Lenspop$affix.py --h5
done