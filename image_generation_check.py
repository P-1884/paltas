import glob
import numpy as np
import h5py
from tqdm import tqdm
import sys
from tensorflow.data import TFRecordDataset
argv = sys.argv

def image_generation_check(directory):
    def image_counter(train_or_val_directory,training_or_validation):
        Total_number_of_images = 0
        Total_number_of_h5_files = 0
        Total_number_of_npy_files = 0 
        Total_number_of_tfrecord_entries = 0
        tf_record_fail_list = []
        for training_folder_i in tqdm(train_or_val_directory):
            if len(glob.glob(f'{training_folder_i}/image_data.h5'))>=1:
                assert len(glob.glob(f'{training_folder_i}/image_data.h5'))==1 #Only allow one h5 file in the folder
                image_file_i = glob.glob(f'{training_folder_i}/image_data.h5')[0]
                try:
                    with h5py.File(image_file_i,'r') as f0: 
                        number_of_files = f0['data'].shape[0]
                        Total_number_of_images+=number_of_files
                except:
                    print('Exception',image_file_i)
                Total_number_of_h5_files+=1
            elif len(glob.glob(f'{training_folder_i}/*.npy'))>=1:
                number_of_files = len(glob.glob(f'{training_folder_i}/*.npy'))
                Total_number_of_images+=number_of_files
                Total_number_of_npy_files+=number_of_files
            try:
                if len(glob.glob(f'{training_folder_i}/data.tfrecord'))>=1:
                    assert len(glob.glob(f'{training_folder_i}/data.tfrecord'))==1 #Only allow one tfrecord file in the folder
                    tf_record_i = TFRecordDataset(f'{training_folder_i}/data.tfrecord')
                    for tf_entry in tf_record_i:
                        Total_number_of_tfrecord_entries+=1
            except Exception as ex:
                print('Exception when retrieving tf record:',ex)
                tf_record_fail_list.append(training_folder_i)
        print(f'Found a total of {Total_number_of_images} {training_or_validation} images,'+\
              f'comprising of {Total_number_of_h5_files} h5 files and {Total_number_of_npy_files} npy files '+\
              f'retrieved from {len(train_or_val_directory)} folders.'+'\n'+\
              f'Found a total of {Total_number_of_tfrecord_entries} tfrecord entries from the {training_or_validation} '+\
              f'folder. Failed to retrieve tf records from the following {len(tf_record_fail_list)} directories: {tf_record_fail_list}')
    image_counter(glob.glob(f'{directory}/training/*'),'training')
    image_counter(glob.glob(f'{directory}/validation/*'),'validation')

image_generation_check(argv[1])
