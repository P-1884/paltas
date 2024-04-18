import numpy as np
import h5py
import glob
def load_h5_file(filename):
    if filename[-2:]!='h5':
        filename_list = glob.glob(filename+'/*.h5')
        if len(filename_list)==1:
            filename = filename_list[0]
            print(f'Loading {filename}')
        else:
            print('No h5 file located in this folder')
            return
    with h5py.File(filename,'r') as f0:
        h5_file_array = f0['data'][()]
    return h5_file_array