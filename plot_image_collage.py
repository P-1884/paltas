import numpy as np
import matplotlib.pyplot as pl
import glob
import h5py
from tqdm import tqdm
def plot_collage(image_folder,N_rows=1,N_cols=1):
    np.random.seed(1)
    N_images = int(N_rows*N_cols)
    #Only uses npy images at the moment:
    image_npy_list = glob.glob(f'{image_folder}/*.npy')
    image_h5_list = glob.glob(f'{image_folder}/*.h5')
    if len(image_npy_list)>0:
        print('Plotting from npy files')
        random_indx = np.random.choice(np.arange(len(image_list)),replace=False,size=N_images)
        image_list = [np.load(image_npy_list[random_indx[n_im]]) for n_im in range(N_images)]
    elif len(image_h5_list)>0:
        print('Plotting from h5 files')
        assert len(image_h5_list)==1 #There should only be one h5 file in the folder
        with h5py.File(image_h5_list[0],'r') as f0:
            number_of_files = f0['data'].shape[0]
            random_indx = np.random.choice(np.arange((number_of_files)),replace=False,size=N_images)
            image_list = [f0['data'][()][random_indx[n_im]] for n_im in tqdm(range(N_images))]
    fig,ax = pl.subplots(N_rows,N_cols,figsize=(5*N_cols,5*N_rows))
    for n_im in range(N_images):
        x = n_im%N_rows
        y = np.floor(n_im/N_rows).astype('int')
        ax[x,y].imshow(image_list[n_im])
    pl.tight_layout()
    pl.show()

#plot_collage('/mnt/extraspace/hollowayp/paltas_data/Example_LP_3/training/1',10,10)
