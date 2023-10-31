import glob
import numpy as np
import h5py
from tqdm import tqdm
import sys

argv = sys.argv

def image_generation_check(directory):
    def image_counter(train_or_val_directory,training_or_validation):
        Total_number_of_images = 0
        Total_number_of_h5_files = 0
        Total_number_of_npy_files = 0 
        for training_folder_i in tqdm(train_or_val_directory):
            if len(glob.glob(f'{training_folder_i}/image_data.h5'))>=1:
                assert len(glob.glob(f'{training_folder_i}/image_data.h5'))==1 #Only allow one h5 file in the folder
                image_file_i = glob.glob(f'{training_folder_i}/image_data.h5')[0]
                with h5py.File(image_file_i,'r') as f0: number_of_files = f0['data'].shape[0]
                Total_number_of_images+=number_of_files
                Total_number_of_h5_files+=1
            elif len(glob.glob(f'{training_folder_i}/*.npy'))>=1:
                number_of_files = len(glob.glob(f'{training_folder_i}/*.npy'))
                Total_number_of_images+=number_of_files
                Total_number_of_npy_files+=number_of_files
        print(f'Found a total of {Total_number_of_images} {training_or_validation} images, comprising of {Total_number_of_h5_files} h5 files and {Total_number_of_npy_files} npy files '+
            f'retrieved from {len(train_or_val_directory)} folders')
    image_counter(glob.glob(f'{directory}/training/*'),'training')
    image_counter(glob.glob(f'{directory}/validation/*'),'validation')

image_generation_check(argv[1])