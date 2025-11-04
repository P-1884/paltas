import os
from importlib import import_module 
#paltas_directory = './'
#training_directory = '/home/runner/work/notebooks/End_to_End_Tutorial_Files/' #For github actions
#model_directory = '/home/runner/work/notebooks/End_to_End_Tutorial_Files/'
#training_directory = '/global/u2/p/phil1884/paltas/notebooks/End_to_End_Tutorial_Files' #For NERSC
#model_directory = '/global/u2/p/phil1884/paltas/notebooks/End_to_End_Tutorial_Files'
#paltas_directory = '/global/u2/p/phil1884/paltas/'

folder_number = 19
analysis_folder = 'paltas.Analysis.AnalysisConfigs'
training_directory = f'/mnt/extraspace/hollowayp/paltas_data/Example_LP_{folder_number}_goodseeing/' #For Glamdring (in extraspace)
training_config_directory = f'{analysis_folder}.train_config_LSST_Lenspop_goodseeing'#_no_subtr' #Keep Updated!
test_directory = f'/mnt/extraspace/hollowayp/paltas_data/Example_LP_{folder_number}_goodseeing/'
model_directory = f'/mnt/extraspace/hollowayp/paltas_data/Example_LP_{folder_number}_goodseeing/'

# training_directory = '/mnt/zfsusers/hollowayp/paltas/extraspace_files/Example_LP_12/'
# test_directory = '/mnt/zfsusers/hollowayp/paltas/extraspace_files/Example_LP_12/'
# model_directory = '/mnt/zfsusers/hollowayp/paltas/extraspace_files/Example_LP_12/'

# training_directory = '/mnt/extraspace/hollowayp/paltas_data/Example_Eu_2/'
# test_directory = '/mnt/extraspace/hollowayp/paltas_data/Example_Eu_2/'
# model_directory = '/mnt/extraspace/hollowayp/paltas_data/Example_Eu_2/'

paltas_directory = '/mnt/zfsusers/hollowayp/paltas/'
os.chdir(paltas_directory)

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

from paltas.Analysis import hierarchical_inference,dataset_generation, loss_functions, conv_models
from IPython.display import display,Pretty
import matplotlib.patches as mpatches
import matplotlib.pyplot as pl
from scipy.stats import norm
import tensorflow as tf
from tqdm import tqdm
import pandas as pd
import numpy as np
import corner
import emcee
import numba
import h5py
import glob
import sys
import datetime
random_seed = 4
np.random.seed(random_seed)
tf.random.set_seed(random_seed)

title_dict = {
    'main_deflector_parameters_gamma':'Density Slope, $\gamma$',
    'main_deflector_parameters_theta_E':'Einstein radius, $\\theta_E$',
    'main_deflector_parameters_e1':'Lens Ellipticity, $e_1$',
    'main_deflector_parameters_e2':'Lens Ellipticity, $e_2$',
    'main_deflector_parameters_gamma1':'Lens Shear,$\gamma_1$',
    'main_deflector_parameters_gamma2':'Lens Shear,$\gamma_2$',
    'main_deflector_parameters_center_x':'Lens Center, x',
    'main_deflector_parameters_center_y':'Lens Center, y',
    'lens_light_parameters_mag_app':'$mag_i$ (Lens)',
    'source_parameters_mag_app':'$mag_i$ (Source)',
    'main_deflector_parameters_z_lens':'$z_L$',
    'source_parameters_z_source':'$z_S$',
    'lens_light_parameters_R_sersic':'Lens Light: $R_{eff}$',
    'source_parameters_R_sersic':'Source Light: $R_{eff}$',
    'lens-source_separation':'Lens-Source Separation',
    'Magnification':'Magnification'
}

import sys
from importlib import reload
try: reload(sys.modules['load_model'])
except: pass
from load_model import load_model,load_model_weights_list,return_final_epoch_weights,return_list_of_weight_files

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
    '/mnt/extraspace/hollowayp/paltas_data/Example_LP_19/':'/mnt/extraspace/hollowayp/paltas_data/Example_LP_19/model_weights/40--1.02.h5',
    '/mnt/extraspace/hollowayp/paltas_data/Example_LP_19_goodseeing/':'/mnt/extraspace/hollowayp/paltas_data/Example_LP_19_goodseeing/model_weights/40--0.23.h5'
}
def epoch_func(model_directory):
    try: return model_epoch_dict[model_directory]
    except: print('Epoch not specified: Just using final epoch');return None

#Import training configs
sys.path.append('/mnt/extraspace/hollowayp/paltas/paltas/Analysis/AnalysisConfigs')

corner_param_print= [elem.replace('main_deflector_parameters_','').replace('subhalo_parameters_','').\
                     replace('theta','\Theta').replace('gamma','\gamma') for elem in learning_params]

model_dict = {} 
if epoch_func(model_directory) is None:
    model_epoch = return_list_of_weight_files(model_directory)[-1]
else: 
    model_epoch = epoch_func(model_directory)

for ii,epoch_i_weights in tqdm(enumerate([model_epoch])): #Just getting the most recent epoch
#for ii,epoch_i_weights in tqdm(enumerate(return_list_of_weight_files(model_directory))): #Just getting the most recent epoch
    if ii==0:
        #If this errors, check the model directory has been specified correctly!
        model,loss_func,num_params = load_model(epoch_i_weights,loss_function,learning_params=learning_params,\
                             log_learning_params=log_learning_params,model_type=model_type,img_size=img_size)
        model_dict[ii]=model
    else: 
        model,_,_ = load_model(epoch_i_weights,loss_function,learning_params=learning_params,\
                        log_learning_params=log_learning_params,model_type=model_type,img_size=img_size)
        model_dict[ii]=model

def gen_network_predictions(test_folder,norm_path,learning_params,log_learning_params,loss_type,
                            loss_func,model,shuffle=True,
                            norm_images=True,log_norm_images=False,
                            N_batch = None):
    """
    Generate neural network predictions given a paltas generated folder of images

    Args:
        test_folder (string): Path to folder of paltas generated images, 
            containing a data.tfrecord file
        norm_path (string): Path to .csv containing normalization of parameters
            applied during training of network
        learning_params (list(string)): Names of parameters learned
        loss_type (string): only 'diag' currently supported for this notebook
        loss_func (paltas.Analysis.loss_function): Loss function object, (needs
            draw_samples() and convert_output() functionality)
        model (paltas.Analysis.conv_models): Trained neural network with weights
            loaded
        shuffle (bool, default=True): If True, the order of the test set is shuffled
            when generating predictions
        norm_images (bool, default=True): If True, normalize test set images
        log_norm_images (bool, default=False): If True, test set imags are
            log-normalized and rescaled to range (0,1)

    Returns:
        y_test, y_pred, std_pred, prec_pred
    """

    tfr_test_path = os.path.join(test_folder,'data.tfrecord')
    input_norm_path = norm_path
    #The following code implementation here and in the hierarchical inference function below assumes a diagonal covariance matrix
    if loss_type !='diag':
        raise ValueError('loss_type not supported in this notebook')
    tf_dataset_test = dataset_generation.generate_tf_dataset(tf_record_path = tfr_test_path,\
                                                             learning_params = learning_params,
                                                             batch_size = 3,\
                                                             n_epochs = 1,\
                                                             norm_images=norm_images,
                                                             kwargs_detector=None,\
                                                             input_norm_path=input_norm_path,
                                                             log_learning_params=log_learning_params,\
                                                             shuffle=shuffle)

    y_test_list = [];y_pred_list = []
    std_pred_list = [];cov_pred_list = []
    predict_samps_list = []
    n_batch = 0
    for batch in (tf_dataset_test):
        images = batch[0].numpy()
        y_test = batch[1].numpy()
        # use unrotated output for covariance matrix
        output = model.predict(images)
        y_pred, log_var_pred = loss_func.convert_output(output)

        # compute std. dev.
        std_pred = np.exp(log_var_pred/2)
        cov_mat = np.empty((len(std_pred),len(std_pred[0]),len(std_pred[0])))
        for i in range(len(std_pred)):
            cov_mat[i] = np.diag(std_pred[i]**2)

        y_test_list.append(y_test)
        y_pred_list.append(y_pred)
        std_pred_list.append(std_pred)
        cov_pred_list.append(cov_mat)
        n_batch+=1
        if N_batch is not None:
            if n_batch>=N_batch: break
    y_test = np.concatenate(y_test_list)
    y_pred = np.concatenate(y_pred_list)
    std_pred = np.concatenate(std_pred_list)
    cov_pred = np.concatenate(cov_pred_list)

    if input_norm_path is not None:
        dataset_generation.unnormalize_outputs(input_norm_path,learning_params+log_learning_params,
                                        y_pred,standard_dev=std_pred,cov_mat=cov_pred)
        dataset_generation.unnormalize_outputs(input_norm_path,learning_params+log_learning_params,
                                        y_test)
    prec_pred = np.linalg.inv(cov_pred)
   
    return y_test, y_pred, std_pred, prec_pred


network_predictions_dict = {}
key_indx = [len(model_dict.keys())-1]#np.linspace(0,len(model_dict.keys())-1,20).astype('int') #Just retrieving 1 epochs, including the last. 
for epoch_i in tqdm(np.array(list(model_dict.keys()))[key_indx]):
#    if epoch_i in network_predictions_dict.keys(): continue #Ignore existing keys
    network_predictions_dict[epoch_i] = gen_network_predictions(\
                        test_folder=training_directory+'/validation/2',\
                        norm_path=glob.glob(f'{training_directory}/**/norm*',recursive=True)[0],
                        #norm_path = training_directory+'/training/1/norms.csv',\
                        learning_params=learning_params,\
                        log_learning_params = log_learning_params,\
                        loss_type=loss_function,
                        loss_func=loss_func,\
                        model=model_dict[epoch_i],
                        shuffle=False, #NOT shuffling here, so the network outputs can be compared with other parameters in the test set.
                        norm_images=norm_images,
                        log_norm_images=False,
                        N_batch = None) #This reduces the total number of images predicted. This should be 'None' if all images are to be predicted.

train_mean = np.array(pd.read_csv(glob.glob(f'{training_directory}/**/norm*',recursive=True)[0])['mean']) 
train_scatter = np.array(pd.read_csv(glob.glob(f'{training_directory}/**/norm*',recursive=True)[0])['std']) 

#Since we are using a diagonal covariance matrix, the precision matrix is the diagonal matrix of
#the (elementwise) values of 1/std^2. In general however it is inv(cov_matrix).

def make_val_databases(network_predictions_dict,key):
    val_or_test_HI = 'val'
    try: del test_data_db,test_data_db_sum
    except: pass
    final_epoch = key#max(list(network_predictions_dict.keys()))
    network_means = network_predictions_dict[final_epoch][1][:,:].astype('float64')              
    network_prec = network_predictions_dict[final_epoch][3][:,:,:].astype('float64')
    metadata_val = pd.read_csv(training_directory+'/validation/2/metadata.csv')

    final_epoch_n = key#np.max(list(network_predictions_dict.keys()))
    network_truth_db = pd.DataFrame(network_predictions_dict[final_epoch_n][0],columns=learning_params+log_learning_params)
    network_pred_mu_db = pd.DataFrame(network_predictions_dict[final_epoch_n][1],columns=learning_params+log_learning_params)
    network_std_db = pd.DataFrame(network_predictions_dict[final_epoch_n][2],columns=learning_params+log_learning_params)

    bright_source_indx = np.where(metadata_val['source_parameters_mag_app']<25)[0]
    #Assert that the true parameters from the metadata are equal to those I'm getting from gen_network_predictions, to make sure there hasn't been any reshuffling
    #and to make sure I'm comparing the properties of the same objects. The 'round' is to remove the problem of some being saved as float32 and others as float64 files.
    db_a = np.round(network_truth_db[learning_params+log_learning_params].astype('float32'),3)
    db_b = np.round(metadata_val[learning_params+log_learning_params].astype('float32'),3)
    assert (db_a==db_b).all().all()
    return metadata_val,network_truth_db,network_pred_mu_db,network_std_db,bright_source_indx

def make_test_databases(network_predictions_test_dict,key):
    val_or_test_HI='test'
    try: del bright_source_indx
    except: pass
    final_epoch = max(list(network_predictions_test_dict.keys()))
    network_means = network_predictions_test_dict[final_epoch][1][:,:].astype('float64')              
    network_prec = network_predictions_test_dict[final_epoch][3][:,:,:].astype('float64')
    metadata_val = pd.DataFrame(network_predictions_test_dict[0][0],columns=learning_params)
    
    final_epoch_n = np.max(list(network_predictions_test_dict.keys()))
    network_truth_db = pd.DataFrame(network_predictions_test_dict[final_epoch_n][0],columns=learning_params)
    network_pred_mu_db = pd.DataFrame(network_predictions_test_dict[final_epoch_n][1],columns=learning_params)
    network_std_db = pd.DataFrame(network_predictions_test_dict[final_epoch_n][2],columns=learning_params)

    test_data_db = metadata_val.copy()
    test_data_db_sum = test_data_db.describe()
    #Assert that the true parameters from the metadata are equal to those I'm getting from gen_network_predictions, to make sure there hasn't been any reshuffling
    #and to make sure I'm comparing the properties of the same objects. The 'round' is to remove the problem of some being saved as float32 and others as float64 files.
    db_a = network_truth_db[learning_params].astype('float32')
    db_b = metadata_val[learning_params].astype('float32')
    assert (db_a==db_b).all().all()
    return metadata_val,network_truth_db,network_pred_mu_db,network_std_db


def plot_histograms(ax,Truth,Pred,Uncertainty,image_property,color='darkblue'):
    t_range = truth_range_dict[image_property]
    e_range = Error_range_dict[image_property]
    u_range = Uncertainty_range_dict[image_property]
    hist_dict = {'density':True,'fill':'False','edgecolor':'k','alpha':0.5}
    ax[0].hist(Truth,bins=np.linspace(t_range[0],t_range[1],20),**hist_dict,label='Truth',color=color)
    ax[0].hist(Pred,bins=np.linspace(t_range[0],t_range[1],20),**hist_dict,label='Pred',color='darkgreen')
    ax[0].legend(fontsize=12)
    ax[1].hist(Uncertainty,bins=np.linspace(0,u_range,20),**hist_dict,color=color)
    ax[2].hist(Truth-Pred,bins=np.linspace(e_range[0],e_range[1],20),**hist_dict,color=color)
    ax[0].set_xlabel(title_dict[image_property],fontsize=15)
    ax[1].set_xlabel('Network Uncertainty',fontsize=15)
    ax[2].set_xlabel('Truth-Pred',fontsize=15)
    ax[2].set_ylim(0,Error_prob_density_dict[image_property])
    ax[1].set_ylim(0,Uncertainty_prob_density_dict[image_property])
    for i in range(3):
        ax[i].tick_params(labelsize=12)
        ax[i].set_ylabel('Probability Density',fontsize=15)
    pl.tight_layout()

def plot_scatter(ax,Truth,Pred,Uncertainty,image_property,color='darkblue'):
    scatter_dict = {'alpha':0.1,'s':10}
    errorbar_dict = {'alpha':0.1,'color':color_dict[test_or_val],'markersize':10,'fmt':'.'}
    kde_dict = {'levels':levels,'alpha':0.5,'fill':True,'color':color_dict[test_or_val],'zorder':2}
    random_indx = np.random.choice(len(network_truth_db),replace=False,size=100)
    #
    ax[0].scatter(Truth,Error,**scatter_dict,c=color_dict[test_or_val])
    #ax[0].scatter(Truth[points_to_highlight],Error[points_to_highlight],**scatter_dict,c='darkred')
    ax[0].set_xlabel('Truth',fontsize=15)
    ax[0].set_ylabel('Pred-Truth',fontsize=15)
    #
    ax[1].scatter(Error,Uncertainty,**scatter_dict,color=color_dict[test_or_val])
    #ax[1].scatter(Error[points_to_highlight],Uncertainty[points_to_highlight],**scatter_dict,color='darkred')
    text_i = f'{np.round(100*np.sum(abs(Error)<Uncertainty)/len(Error),1)}%'
    ax[1].set_xlabel('Truth-Pred',fontsize=15)
    ax[1].set_ylabel('Network Uncertainty',fontsize=15)
    #
    ax[2].scatter(Truth,Pred,**scatter_dict,color=color_dict[test_or_val])
    #ax[2].scatter(Truth[points_to_highlight],Pred[points_to_highlight],**scatter_dict,color='darkred')
    ax[2].set_xlabel('Truth',fontsize=15)
    ax[2].set_ylabel('Pred',fontsize=15)
    #Setting limits:
    ax[0].set_xlim(truth_range_dict[image_property])
    ax[0].set_ylim(Error_range_dict[image_property])
    ax[1].set_xlim(Error_range_dict[image_property])  
    ax[1].set_ylim(0,Uncertainty_range_dict[image_property])
    ax[1].text(0,0.9*ax[1].get_ylim()[1],ha='center',fontsize=15,color=color_dict[test_or_val],s=text_i)
    plot_error_lines(ax[1])
    ax[2].set_xlim(truth_range_dict[image_property])
    ax[2].set_ylim(truth_range_dict[image_property])
    ax3_ylim = ax[2].get_ylim();ax3_xlim = ax[2].get_xlim()
    ax3_min = np.min([ax3_xlim[0],ax3_ylim[1]])
    ax3_max = np.max([ax3_xlim[0],ax3_ylim[1]])
    ax[2].plot([ax3_min,ax3_max],[ax3_min,ax3_max],'--',c='k')
    #kdeplot(Truth,Error,ax=ax[0],**kde_dict)
    #kdeplot(Error,Uncertainty,ax=ax[2],**kde_dict)
    for i in range(3):
        ax[i].tick_params(labelsize=12)


from seaborn import kdeplot
def plot_error_lines(ax):
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    max_val = np.max([xlim[1],ylim[1]])
    error_line_dict = {'color':'k','linestyle':'--'}
    ax.plot([0,max_val],[0,max_val],**error_line_dict)
    ax.plot([0,-max_val],[0,max_val],**error_line_dict)

property_list = [
     'main_deflector_parameters_theta_E',
    'main_deflector_parameters_gamma',
#    'lens_light_parameters_R_sersic',
#    'lens_light_parameters_mag_app' #This is natural logged.
#    'main_deflector_parameters_gamma1',
#    'main_deflector_parameters_gamma2',
#    'main_deflector_parameters_center_x',
#    'main_deflector_parameters_center_y',
#    'main_deflector_parameters_e1','main_deflector_parameters_e2'
]


Error_range_dict = {'main_deflector_parameters_theta_E':(-0.4,0.4),
                    'main_deflector_parameters_gamma':(-0.4,0.4),
                    'main_deflector_parameters_gamma1':(-0.2,0.2),
                    'main_deflector_parameters_gamma2':(-0.2,0.2),
                    'main_deflector_parameters_e1':(-0.4,0.4),
                    'main_deflector_parameters_e2':(-0.4,0.4),
                    'main_deflector_parameters_center_x':(-0.2,0.2),
                    'main_deflector_parameters_center_y':(-0.2,0.2),
                    'lens_light_parameters_R_sersic':(-0.2,0.2),
                    'lens_light_parameters_mag_app':(-1,1)
                   }
Uncertainty_range_dict = {'main_deflector_parameters_theta_E':0.6,
                    'main_deflector_parameters_gamma':0.4,
                    'main_deflector_parameters_gamma1':0.1,
                    'main_deflector_parameters_gamma2':0.1,
                    'main_deflector_parameters_e1':0.4,
                    'main_deflector_parameters_e2':0.4,
                    'main_deflector_parameters_center_x':0.1,
                    'main_deflector_parameters_center_y':0.1,
                    'lens_light_parameters_R_sersic':0.2,
                    'lens_light_parameters_mag_app':1
                   }

truth_range_dict = {'main_deflector_parameters_theta_E':(0,4),
                    'main_deflector_parameters_gamma':(1,3),
                    'main_deflector_parameters_gamma1':(-0.2,0.2),
                    'main_deflector_parameters_gamma2':(-0.2,0.2),
                    'main_deflector_parameters_e1':(-0.6,0.6),
                    'main_deflector_parameters_e2':(-0.6,0.6),
                    'main_deflector_parameters_center_x':(-0.2,0.2),
                    'main_deflector_parameters_center_y':(-0.2,0.2),
                    'lens_light_parameters_R_sersic':(0,1),
                    'lens_light_parameters_mag_app':(12,25)
                   }

Error_prob_density_dict = {'main_deflector_parameters_theta_E':12,
                    'main_deflector_parameters_gamma':4.5,
                    'main_deflector_parameters_gamma1':0.1,
                    'main_deflector_parameters_gamma2':0.1,
                    'main_deflector_parameters_e1':0.4,
                    'main_deflector_parameters_e2':0.4,
                    'main_deflector_parameters_center_x':0.1,
                    'main_deflector_parameters_center_y':0.1,
                    'lens_light_parameters_R_sersic':20,
                    'lens_light_parameters_mag_app':1}

Uncertainty_prob_density_dict = {'main_deflector_parameters_theta_E':15,
                    'main_deflector_parameters_gamma':6,
                    'main_deflector_parameters_gamma1':0.1,
                    'main_deflector_parameters_gamma2':0.1,
                    'main_deflector_parameters_e1':0.4,
                    'main_deflector_parameters_e2':0.4,
                    'main_deflector_parameters_center_x':0.1,
                    'main_deflector_parameters_center_y':0.1,
                    'lens_light_parameters_R_sersic':20,
                    'lens_light_parameters_mag_app':1}

levels = 1-np.array([1 - np.exp(-(2**2)/2),#% Contained within 2,1 sigma (have to do 1- as the levels does fraction *below* contour)
                     1 - np.exp(-(1**2)/2),# => See https://corner.readthedocs.io/en/latest/pages/sigmas/ for why this equation is used.
                     0])   
print(training_directory)

test_or_val = 'val'
color_dict = {'test':'darkred','val':'darkblue'}
keys_list = list(network_predictions_dict.keys())
keys_list.sort()
for n_k,key_i in enumerate(keys_list):
    assert test_or_val in ['test','val']
    if test_or_val=='val':
        metadata_val,network_truth_db,network_pred_mu_db,network_std_db,bright_source_indx =\
                make_val_databases(network_predictions_dict,key_i)
    if test_or_val=='test':
        metadata_val,network_truth_db,network_pred_mu_db,network_std_db =\
                make_test_databases(network_predictions_test_dict,key_i)

network_truth_db.to_csv(f'{model_directory}/network_truth_db.csv')
network_pred_mu_db.to_csv(f'{model_directory}/network_pred_mu_db.csv')
network_std_db.to_csv(f'{model_directory}/network_std_db.csv')
metadata_val.to_csv(f'{model_directory}/metadata_val.csv')

