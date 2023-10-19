import numpy as np
import matplotlib.pyplot as pl
import glob

def plot_collage(image_folder,N_rows=1,N_cols=1):
    np.random.seed(1)
    N_images = int(N_rows*N_cols)
    #Only uses npy images at the moment:
    image_list = glob.glob(f'{image_folder}/*.npy')
    random_indx = np.random.choice(np.arange(len(image_list)),replace=False,size=N_images)
    fig,ax = pl.subplots(N_rows,N_cols,figsize=(5*N_cols,5*N_rows))
    for n_im in range(N_images):
        x = n_im%N_rows
        y = np.floor(n_im/N_rows).astype('int')
        ax[x,y].imshow(np.load(image_list[random_indx[n_im]]))
    pl.tight_layout()
    pl.show()
