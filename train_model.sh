#addqueue -c '45min' -m 2 -n 1x4 -s -q gpulong /usr/bin/python3 ./paltas/Analysis/train_model.py ./paltas/Analysis/AnalysisConfigs/train_config_examp.py --h5
module load python

python ./paltas/Analysis/train_model.py ./paltas/Analysis/AnalysisConfigs/train_config_examp_LSST.py --h5
