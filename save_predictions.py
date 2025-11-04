from importlib import import_module 
import sys
import os
paltas_directory = '/mnt/users/hollowayp/paltas/'
sys.path.append('/mnt/users/hollowayp/paltas')
sys.path.append('/')
os.chdir(paltas_directory)
argv = sys.argv
print(argv)

folder_number = int(argv[1])
model_folder_number = int(argv[2])
model_affix = argv[3] #"", "_goodseeing", "_no_RSP", "no_subtr"
cov_matrix = argv[4] #full, diag
train_dir_affix = argv[5]
test_dir_affix = argv[6]
if model_affix=="''": model_affix=''
if train_dir_affix=="''": train_dir_affix=''
if test_dir_affix=="''": test_dir_affix=''

cov_dict = {'diag':"",'full':'_fullcov'}
cov_str = cov_dict[cov_matrix]
training_directory = f'/mnt/extraspace/hollowayp/paltas_data/Example_LP_{folder_number}{train_dir_affix}/' #For Glamdring (in extraspace)
test_directory = f'/mnt/extraspace/hollowayp/paltas_data/Example_LP_{folder_number}{test_dir_affix}/'
model_directory = f'/mnt/extraspace/hollowayp/paltas_data/Example_LP_{model_folder_number}{model_affix}{cov_str}/'
training_config_directory = f'{model_directory.replace("/",".")[1:-1]}.model_weights.train_config_LSST_Lenspop{model_affix}{cov_str}'

training_config = import_module(training_config_directory)
learning_params = training_config.learning_params
log_learning_params = training_config.log_learning_params
batch_size = training_config.batch_size
flip_pairs = training_config.flip_pairs
n_epochs = training_config.n_epochs
random_seed = training_config.random_seed
norm_images = training_config.norm_images
loss_function = training_config.loss_function
model_type = training_config.model_type
img_size = training_config.img_size
npy_folders_train = training_config.npy_folders_train

from load_model import load_model,load_model_weights_list,return_final_epoch_weights,return_list_of_weight_files
from paltas.Analysis import hierarchical_inference,dataset_generation, loss_functions, conv_models
from parameter_dicts import truth_range_dict,title_dict,title_dict_short,Error_range_dict
from make_databases import make_val_databases,make_test_databases
from generate_predictions import gen_network_predictions_general
import matplotlib.patches as mpatches
import matplotlib.pyplot as pl
from scipy.stats import norm
from importlib import reload
import tensorflow as tf
from tqdm import tqdm
import pandas as pd
import numpy as np
import corner
import h5py
import glob
import sys
import datetime

random_seed = 4
np.random.seed(random_seed)
tf.random.set_seed(random_seed)

try:reload(sys.modules['parameter_dicts'])
except:pass
try:reload(sys.modules['make_databases'])
except: pass
try:reload(sys.modules['load_model'])
except: pass
try: reload(sys.modules['generate_predictions'])
except: pass

final_weights_filename = return_final_epoch_weights(model_directory)

def retrieve_training_prior():
    prior_path = glob.glob(f'{training_directory}/**/norm*',recursive=True)[0]
    print(f'Retrieving prior path from {prior_path}')
    training_prior_db = pd.read_csv(prior_path)
    return training_prior_db

prior_db = retrieve_training_prior()
prior_db_indx = prior_db.set_index(prior_db['parameter'])
print('NOTE: This training prior should really encompass all the training images, not just a subset (i.e. not just one folder of them)')

#Insert the model epoch to use in cases where the model begins to overfit to the training data: 

model_epoch_dict = {
    # '/mnt/extraspace/hollowayp/paltas_data/Example_LP_19/':'/mnt/extraspace/hollowayp/paltas_data/Example_LP_19/model_weights/40--1.02.h5',
    # '/mnt/extraspace/hollowayp/paltas_data/Example_LP_19_goodseeing/':'/mnt/extraspace/hollowayp/paltas_data/Example_LP_19_goodseeing/model_weights/40--0.23.h5',
    # '/mnt/extraspace/hollowayp/paltas_data/Example_LP_28_no_RSP/':'/mnt/extraspace/hollowayp/paltas_data/Example_LP_28_no_RSP/model_weights/11--5.24.h5',
    # '/mnt/extraspace/hollowayp/paltas_data/Example_LP_31_no_RSP_fullcov/':'/mnt/extraspace/hollowayp/paltas_data/Example_LP_31_no_RSP_fullcov/model_weights/36--7.07.h5',
    # '/mnt/extraspace/hollowayp/paltas_data/Example_LP_32/':'/mnt/extraspace/hollowayp/paltas_data/Example_LP_32//model_weights/17--1.89.h5',
    # '/mnt/extraspace/hollowayp/paltas_data/Example_LP_32_fullcov/':'/mnt/extraspace/hollowayp/paltas_data/Example_LP_32_fullcov//model_weights/21--2.45.h5',
    # '/mnt/extraspace/hollowayp/paltas_data/Example_LP_32_goodseeing/':'/mnt/extraspace/hollowayp/paltas_data/Example_LP_32_goodseeing//model_weights/17--1.65.h5',
    # '/mnt/extraspace/hollowayp/paltas_data/Example_LP_32_goodseeing_fullcov/':'/mnt/extraspace/hollowayp/paltas_data/Example_LP_32_goodseeing_fullcov//model_weights/18--2.13.h5',
    # '/mnt/extraspace/hollowayp/paltas_data/Example_LP_32_no_RSP/':'/mnt/extraspace/hollowayp/paltas_data/Example_LP_32_no_RSP//model_weights/24--4.63.h5',
    # '/mnt/extraspace/hollowayp/paltas_data/Example_LP_32_no_RSP_fullcov/':'/mnt/extraspace/hollowayp/paltas_data/Example_LP_32_no_RSP_fullcov//model_weights/34--6.04.h5',
    # '/mnt/extraspace/hollowayp/paltas_data/Example_LP_32_no_subtr/':'/mnt/extraspace/hollowayp/paltas_data/Example_LP_32_no_subtr//model_weights/111--6.36.h5',
    # '/mnt/extraspace/hollowayp/paltas_data/Example_LP_32_no_subtr_fullcov/':'/mnt/extraspace/hollowayp/paltas_data/Example_LP_32_no_subtr_fullcov//model_weights/134--5.90.h5',
    # '/mnt/extraspace/hollowayp/paltas_data/Example_LP_32_centred_no_shear/':'/mnt/extraspace/hollowayp/paltas_data/Example_LP_32_centred_no_shear//model_weights/11--1.07.h5',
    # '/mnt/extraspace/hollowayp/paltas_data/Example_LP_37/':'/mnt/extraspace/hollowayp/paltas_data/Example_LP_37//model_weights/109--4.37.h5',
    # '/mnt/extraspace/hollowayp/paltas_data/Example_LP_36/':'/mnt/extraspace/hollowayp/paltas_data/Example_LP_36//model_weights/136--1.26.h5',
}

db_WandB = pd.read_csv('WandB Loss Evolution.csv')
for file_n in ['Example_LP_40']:
    for cov in [{'diag':"",'full':"_fullcov"}[cov_matrix]]:#['','_fullcov']:
        for affix in [model_affix]:#'',"_no_subtr","_no_RSP","_goodseeing",'_no_subtr_LS_light']:
            min_val_loss_step = np.where(db_WandB[f'{file_n}{affix}{cov} - Val Loss']==db_WandB[f'{file_n}{affix}{cov} - Val Loss'].min())[0][0]
            min_val_loss_epoch = min_val_loss_step+1
            model_epoch_dict[f'/mnt/extraspace/hollowayp/paltas_data/{file_n}{affix}{cov}/'] = glob.glob(f'/mnt/extraspace/hollowayp/paltas_data/{file_n}{affix}{cov}/model_weights/{min_val_loss_epoch}-*.h5')[0]

print('MODEL EPOCH DICT')
print(model_epoch_dict)

print('Model directory:',model_directory)
def epoch_func(model_directory):
    try: return model_epoch_dict[model_directory]
    except: print('Epoch not specified: Just using final epoch');return None

#Import training configs
model_dict = {} 
if epoch_func(model_directory) is None:
    model_epoch = return_list_of_weight_files(model_directory)[-1]
else: 
    model_epoch = epoch_func(model_directory)

for ii,epoch_i_weights in tqdm(enumerate([model_epoch])): #Just getting the most recent epoch
    print('Model epoch',model_epoch)
    if ii==0:
        #If this errors, check the model directory has been specified correctly!
        model,loss_func,num_params = load_model(epoch_i_weights,loss_function,learning_params=learning_params,\
                             log_learning_params=log_learning_params,model_type=model_type,img_size=img_size)
        model_dict[ii]=model
    else: 
        model,_,_ = load_model(epoch_i_weights,loss_function,learning_params=learning_params,\
                        log_learning_params=log_learning_params,model_type=model_type,img_size=img_size)
        model_dict[ii]=model

network_predictions_test_dict = {}
network_predictions_test_dict[0] = \
    gen_network_predictions_general(
                                test_folder=f'{test_directory}/test/',
                                norm_path = glob.glob(f'{training_directory}/**/norm*',recursive=True)[0],
								learning_params=learning_params,
								log_learning_params=log_learning_params,
								loss_type=loss_function,
								loss_func=loss_func,
								model=model,
								norm_images=norm_images,
								log_norm_images=False,
								h5_or_not='True',
								N_max=None,
								diag_cov = (loss_function=='diag'),
                                return_prec=True)

#Fixing the shaping:
network_predictions_test_dict[0] = \
(network_predictions_test_dict[0][0][:,0,0,:],
# (network_predictions_test_dict[0][0][:,0,:],
network_predictions_test_dict[0][1],
network_predictions_test_dict[0][2],
network_predictions_test_dict[0][3])

# y_test_list, y_pred, std_pred, prec_pred

pd.DataFrame(network_predictions_test_dict[0][0],columns=learning_params+log_learning_params).to_csv(f'{model_directory}/groundtruth_db.csv')
pd.DataFrame(network_predictions_test_dict[0][1],columns=learning_params+log_learning_params).to_csv(f'{model_directory}/network_mu_db.csv')
pd.DataFrame(network_predictions_test_dict[0][2],columns=learning_params+log_learning_params).to_csv(f'{model_directory}/network_std_db.csv')
np.save(f'{model_directory}/network_prec_db.npy',network_predictions_test_dict[0][3]) #3D array

# folder_number model_number model_affix cov_matrix train_affix test_affix
# folder_number = int(argv[1])
# model_folder_number = int(argv[2])
# model_affix = argv[3] #"", "_goodseeing", "_no_RSP", "no_subtr"
# if model_affix=="''": model_affix=''
# cov_matrix = argv[4] #full, diag
# train_dir_affix = argv[5]
# test_dir_affix = argv[6]

''' #"''" "_no_RSP" "_no_subtr" "_goodseeing" "_no_subtr_LS_light"; do
for type in "_no_subtr_mu3" ; do
# for cov in "diag" "full"; do
for cov in "diag"; do
python3 save_predictions.py 40 40 $type $cov "_no_subtr_mu3" "_no_subtr" 
done;
done

python="/mnt/users/hollowayp/python114_archive/bin/python3.11"
queue=cmb
#addqueue -m 20 -q ${queue} ${python} save_predictions.py 40 40 "_no_subtr_mu3" "diag" "_no_subtr_mu3" "_no_subtr" 
#addqueue -m 20 -q ${queue} ${python} save_predictions.py 40 40 "_no_subtr_LS_light_mu3" "diag" "_no_subtr_LS_light_mu3" "_no_subtr_LS_light" 
#addqueue -m 20 -q ${queue} ${python} save_predictions.py 40 40 "_no_RSP_mu3" "diag" "_no_RSP_mu3" "_no_RSP" 
#addqueue -m 20 -q ${queue} ${python} save_predictions.py 40 40 "_goodseeing_mu3" "diag" "_goodseeing_mu3" "_goodseeing" 
#addqueue -m 20 -q ${queue} ${python} save_predictions.py 40 40 "_mu3" "diag" "_mu3" "''" 

addqueue -m 20 -q ${queue} ${python} save_predictions.py 40 40 "_mu3_B_gamma_-10pct" "diag" "_mu3_B_gamma_-10pct" "''" 
addqueue -m 20 -q ${queue} ${python} save_predictions.py 40 40 "_mu3_B_gamma_10pct" "diag" "_mu3_B_gamma_10pct" "''" 
addqueue -m 20 -q ${queue} ${python} save_predictions.py 40 40 "_mu3_B_gamma_-1pct" "diag" "_mu3_B_gamma_-1pct" "''"
#
addqueue -m 20 -q ${queue} ${python} save_predictions.py 40 40 "_mu3_B_theta_E_-10pct" "diag" "_mu3_B_theta_E_-10pct" "''" 
addqueue -m 20 -q ${queue} ${python} save_predictions.py 40 40 "_mu3_B_theta_E_-1pct" "diag" "_mu3_B_theta_E_-1pct" "''" 


'''
