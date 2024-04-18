import h5py
import numpy as np
import os
import glob
import matplotlib.pyplot as pl
from tqdm import tqdm
import json

def load_RSP(folder_name):
    print('Loading RSP Images')
    file_names = glob.glob(f'{folder_name}/**image_data.h5')
    image_dict = {}
    exp_dict = {}
    psf_dict = {}
    var_dict = {}
    for filename_i in tqdm(file_names):
        exp_file = filename_i.replace('image_data','Nexp_data')
        psf_file = filename_i.replace('image_data','psf_data')
        var_file = filename_i.replace('image_data','var_data')        
        with h5py.File(filename_i,'r') as f0: 
            image_dict[filename_i] = f0['data'][()]
        with h5py.File(exp_file,'r') as e0: 
            exp_dict[filename_i] = e0['data'][()]
        with h5py.File(psf_file,'r') as p0: 
            psf_dict[filename_i] = p0['data'][()]
        with h5py.File(var_file,'r') as v0:
            var_dict[filename_i]= v0['data'][()]
    with open(f'{folder_name}/Noise_dict.json','r') as f0:
        Noise_property_dict = json.load(f0)
    return image_dict, exp_dict, psf_dict, var_dict, Noise_property_dict

def sample_RSP_from_dict(keys,N_im_per_file):
    random_file = np.random.choice(keys)
    random_index = np.random.choice(np.arange(N_im_per_file))
    print(f'Selecting RSP image from: {random_file}, Index: {random_index}')
    return random_file,random_index

def sample_RSP(folder_name,n_images=1):
    print('SLOW NOTE: Note: This section (sample_RSP.py) may need speeding up as it opens many h5 files individually')
    file_names = glob.glob(f'{folder_name}/**image_data.h5')
    cutout_im_list = [];N_exp_list = [];psf_list = [];var_list=[]
    for n_im in range(n_images):
        random_file = np.random.choice(file_names)
        exp_file = random_file.replace('image_data','Nexp_data')
        psf_file = random_file.replace('image_data','psf_data')
        var_file = random_file.replace('image_data','var_data')
        with h5py.File(random_file,'r') as f0: 
            cutout_files = f0['data']
            random_cutout = np.random.choice(np.arange(cutout_files.shape[0]))
            random_image = cutout_files[()][random_cutout]
        with h5py.File(exp_file,'r') as e0: 
            exp_files = e0['data']
            random_exp= exp_files[()][random_cutout]
        with h5py.File(psf_file,'r') as p0: 
            psf_files = p0['data']
            random_psf = psf_files[()][random_cutout]
        with h5py.File(var_file,'r') as v0:
            var_files = v0['data']
            random_var = var_files[()][random_cutout]
        if n_images==1: return random_image,random_exp,random_psf,random_var
        else: 
            cutout_im_list.append(random_image)
            N_exp_list.append(random_exp)
            psf_list.append(random_psf)
            var_list.append(random_var)
    return np.array(cutout_im_list),N_exp_list,psf_list,np.array(var_list)

#sample_RSP('/mnt/zfsusers/hollowayp/paltas/RSP_Coadd_Files_2000',10)