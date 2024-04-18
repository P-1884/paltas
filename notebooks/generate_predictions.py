from paltas.Analysis import hierarchical_inference,dataset_generation, loss_functions, conv_models
import pandas as pd
import numpy as np
import glob
import h5py
from tqdm import tqdm 
def gen_network_predictions_test_set(test_folder,norm_path,learning_params,log_learning_params,loss_type,
                            loss_func,model,test_directory,
                            norm_images=True,log_norm_images=False,
                            h5_or_not=None,N_max=None):
    print("Something weird here - norm_images argument doesn't seem to do anything in this function?")
    input_norm_path = norm_path
    if h5_or_not=='True':
        metadata_file = test_folder+'/metadata.csv'
        metadata_db = pd.read_csv(metadata_file)[learning_params]
        print(f'Using {len(metadata_db)} images as a validation set, from {test_folder}')
        with h5py.File(f'{test_folder}/image_data.h5', "r") as f:
            image_list = f['data'][()]
        N_images=len(metadata_db)
    #
    if h5_or_not=='False':
        test_data = glob.glob(f'{test_directory}/test/**/*.npy',recursive=True)
        #This is important: it assumes the order of the ground truth in the metadata files is the same
        #as the numbers given to the .npy files (i.e. that image_0000000.npy is the first one in the metadata)
        #file:
        test_data.sort()
        print('NB: Assume .npy filenames are an ordered list.')
        print(f'Using {len(test_data)} images as a test set, from {test_folder}')
        N_images=len(test_data)
    #
    #The following code implementation here and in the hierarchical inference function below assumes a diagonal covariance matrix
    if loss_type !='diag':
        raise ValueError('loss_type not supported in this notebook')
    if N_max is not None:
        N_images = N_max #Just a quicker way to test the code
    y_test_list = [];y_pred_list = []
    std_pred_list = [];cov_pred_list = []
    predict_samps_list = []
    for b_i in tqdm(range(N_images)):
        if h5_or_not=='False':
            filename_i = test_data[b_i]
            metadata_file = filename_i.split('image_')[0]+'metadata.csv' 
            images = np.load(filename_i)
            images = images[np.newaxis,...,np.newaxis]
            y_test = pd.read_csv(metadata_file).loc[b_i][learning_params].tolist()
        if h5_or_not=='True':
            images = image_list[b_i]
            images = images[np.newaxis,...,np.newaxis]
            y_test = np.array(metadata_db.loc[b_i])
            y_test = y_test[np.newaxis,...]
        '''Normalising the images according to their standard deviation:'''
        images=images/np.std(images)
        # use unrotated output for covariance matrix
        output = model.predict(images)
        y_pred, log_var_pred = loss_func.convert_output(output)
        # compute std. dev.
        std_pred = np.exp(log_var_pred/2)
        cov_mat = np.empty((len(std_pred),len(std_pred[0]),len(std_pred[0])))
        for i in range(len(std_pred)):
            cov_mat[i] = np.diag(std_pred[i]**2)

        y_test_list.append([y_test])
        y_pred_list.append(y_pred)
        std_pred_list.append(std_pred)
        cov_pred_list.append(cov_mat)

    y_test = np.concatenate(y_test_list)
    y_pred = np.concatenate(y_pred_list)
    std_pred = np.concatenate(std_pred_list)
    cov_pred = np.concatenate(cov_pred_list)
    cov_pred_list_new = []
    print('ASSUMING COVARIANCE MATRIX IS DIAGONAL HERE')
    for indx_i in (range(len(cov_pred))):
        diag_i = np.diag(cov_pred[indx_i,:,:])
        diag_ii = diag_i.copy()
        diag_ii[diag_ii==0]=np.nan
        cov_pred_list_new.append([np.diag(diag_ii)])
    cov_pred = np.concatenate(cov_pred_list_new)
    if input_norm_path is not None:
        print('Unnormalising outputs')
        dataset_generation.unnormalize_outputs(input_norm_path,learning_params+log_learning_params,
                                        y_pred,standard_dev=std_pred,cov_mat=cov_pred)
    '''Am NOT unnormalising the y_test values here, since in this case I am taking the ground-truth
    from the metadata.csv files, which are already unnormalised:
    dataset_generation.unnormalize_outputs(input_norm_path,learning_params+log_learning_params,
                                        y_test)
    '''
    prec_pred = np.linalg.inv(cov_pred)
    return y_test, y_pred, std_pred, prec_pred

def gen_network_predictions_single(npy_file,input_norm_path,learning_params,log_learning_params,loss_type,
                            loss_func,model,
                            norm_images=True,log_norm_images=False,return_cov=True):
    #The following code implementation here and in the hierarchical inference function below assumes a diagonal covariance matrix
    if loss_type !='diag':
        raise ValueError('loss_type not supported in this notebook')

    std_pred_list = [];cov_pred_list = []
    images = np.load(npy_file)
    images = images[np.newaxis,...,np.newaxis]
    '''Normalising the images according to their standard deviation:'''
    images=images/np.std(images)
    # use unrotated output for covariance matrix
    output = model.predict(images)
    y_pred, log_var_pred = loss_func.convert_output(output)
    y_pred_list=[] #KEEP this in (even though it seems arbitrary) - otherwise the y_pred values aren't un-normalised and it will return the wrong answer!
    y_pred_list.append(y_pred)
    y_pred = np.concatenate(y_pred_list)
    # compute std. dev.
    std_pred = np.exp(log_var_pred/2)
    if not return_cov:
        if input_norm_path is not None:
            print('Unnormalising outputs')
            dataset_generation.unnormalize_outputs(input_norm_path,learning_params+log_learning_params,
                                            y_pred,
                                            standard_dev=std_pred,cov_mat=None)
        return y_pred, std_pred
    cov_mat = np.empty((len(std_pred),len(std_pred[0]),len(std_pred[0])))
    for i in range(len(std_pred)):
        cov_mat[i] = np.diag(std_pred[i]**2)
    cov_pred_list.append(cov_mat)
    ####
    cov_pred = np.concatenate(cov_pred_list)
    cov_pred_list_new = []
    print('ASSUMING COVARIANCE MATRIX IS DIAGONAL HERE')
    for indx_i in (range(len(cov_pred))):
        diag_i = np.diag(cov_pred[indx_i,:,:])
        diag_ii = diag_i.copy()
        diag_ii[diag_ii==0]=np.nan
        cov_pred_list_new.append([np.diag(diag_ii)])
        #print(np.shape(cov_pred_list[indx_i,0,:,:]))
    cov_pred = np.concatenate(cov_pred_list_new)
    if input_norm_path is not None:
        print('Unnormalising outputs')
        dataset_generation.unnormalize_outputs(input_norm_path,learning_params+log_learning_params,
                                        y_pred,
                                        standard_dev=std_pred,cov_mat=cov_pred)
    '''Am NOT unnormalising the y_test values here, since in this case I am taking the ground-truth
    from the metadata.csv files, which are already unnormalised:
    dataset_generation.unnormalize_outputs(input_norm_path,learning_params+log_learning_params,
                                        y_test)
    '''
    prec_pred = np.linalg.inv(cov_pred)
    return y_pred, std_pred, prec_pred
