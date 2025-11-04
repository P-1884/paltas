queue='gpulong' #'cmbgpu' # #'blackhole' #'cmbgpu' #
gputype='--gputype rtx2080with12gb --gpus 2'  #'--gputype rtx3090with24gb --gpus 1' #
memory='-m 6 -n 1x4' #'-m 20'
python='/mnt/users/hollowayp/python114_tensorflow/bin/python3.11'
for affix in "_mu3_B_gamma_-10pct" "_mu3_B_gamma_-1pct" "_mu3_B_theta_E_-10pct" "_mu3_B_theta_E_-1pct" #"_mu3_B_theta_E_10pct" "_mu3_B_gamma_1pct" #"_mu3_B_theta_E_1pct" #"_no_subtr_LS_light_mu3" "_no_subtr_mu3" "_mu3" "_no_RSP_mu3" "_goodseeing_mu3" #"_no_subtr_LS_light" #"_no_subtr" "" "_no_RSP" "_goodseeing"
do
for cov_matrix in "" #"_fullcov"
do
addqueue -c '1day' $memory -s -q $queue $gputype -g Model$affix$cov_matrix $python /mnt/users/hollowayp/paltas/paltas/Analysis/train_model.py /mnt/users/hollowayp/paltas/paltas/Analysis/AnalysisConfigs/train_config_LSST_Lenspop$affix$cov_matrix.py --h5
done
done

# """
# queue='gpulong' #'blackhole' #'cmbgpu' #
# gputype='--gputype rtx2080with12gb --gpus 1' #'' #'--gputype rtx3090with24gb' #
# memory='-m 6 -n 1x4' #'-m 40' #
# python='/mnt/users/hollowayp/python114_tensorflow/bin/python3.11'
# addqueue -c '3days' $memory -s -q $queue $gputype -g Model_500k $python /mnt/users/hollowayp/paltas/paltas/Analysis/train_model.py /mnt/users/hollowayp/paltas/paltas/Analysis/AnalysisConfigs/train_config_LSST_Lenspop_500k.py --h5
# """
