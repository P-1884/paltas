from paltas.Analysis import hierarchical_inference,dataset_generation, loss_functions, conv_models
import pandas as pd
import numpy as np
import glob
import h5py
from tqdm import tqdm 
import time
import os
from load_h5_file import load_h5_file
import tensorflow as tf
def gen_network_predictions_test_set(test_folder,norm_path,learning_params,log_learning_params,loss_type,
                            loss_func,model,test_directory,
                            norm_images=True,log_norm_images=False,
                            h5_or_not=None,N_max=None,
                            diag_cov = True):
    print("Something weird here - norm_images argument doesn't seem to do anything in this function?")
    input_norm_path = norm_path
    if h5_or_not=='True':
        metadata_file = test_folder+'/metadata.csv'
        metadata_db = pd.read_csv(metadata_file)[learning_params+log_learning_params]
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
    # if loss_type !='diag':
    #     raise ValueError('loss_type not supported in this notebook')
    if N_max is not None:
        N_images = N_max #Just a quicker way to test the code
    y_test_list = [];y_pred_list = []
    std_pred_list = [];cov_pred_list = [];prec_pred_list = []
    predict_samps_list = []
    for b_i in tqdm(range(N_images)):
        if h5_or_not=='False':
            filename_i = test_data[b_i]
            metadata_file = filename_i.split('image_')[0]+'metadata.csv' 
            images = np.load(filename_i)
            images = images[np.newaxis,...,np.newaxis]
            y_test = pd.read_csv(metadata_file).loc[b_i][learning_params+log_learning_params].tolist()
        if h5_or_not=='True':
            images = image_list[b_i]
            images = images[np.newaxis,...,np.newaxis]
            y_test = np.array(metadata_db.loc[b_i])
            y_test = y_test[np.newaxis,...]
        '''Normalising the images according to their standard deviation:'''
        images=images/np.std(images)
        # use unrotated output for covariance matrix
        output = model.predict(images)
        if diag_cov: 
            y_pred, log_var_pred = loss_func.convert_output(output)
            # compute std. dev.
            std_pred = np.exp(log_var_pred/2)
            cov_mat = np.empty((len(std_pred),len(std_pred[0]),len(std_pred[0])))
            for i in range(len(std_pred)):
                assert loss_type=='diag'
                cov_mat[i] = np.diag(std_pred[i]**2)
            y_test_list.append([y_test])
            y_pred_list.append(y_pred)
            std_pred_list.append(std_pred)
            cov_pred_list.append(cov_mat)
        else: 
            y_pred, prec_pred, _ = loss_func.convert_output(output)
            y_test_list.append([y_test])
            y_pred_list.append(y_pred)
            prec_pred_list.append(prec_pred)
    if diag_cov:
        y_test = np.concatenate(y_test_list)
        y_pred = np.concatenate(y_pred_list)
        std_pred = np.concatenate(std_pred_list)
        cov_pred = np.concatenate(cov_pred_list)
    else:
        y_test = np.concatenate(y_test_list)
        y_pred = np.concatenate(y_pred_list)
        prec_pred = np.concatenate(prec_pred_list)
        cov_pred = np.linalg.inv(prec_pred)
        print('COV',cov_pred.shape)
        std_pred = np.array([np.diag(cov_pred[m_i,:,:]) for m_i in range(cov_pred.shape[0])])
        #std_pred = np.diag(cov_pred)
        print('std',std_pred.shape)
        #print(std_pred[0,:,:],std_pred[:,0,:],std_pred[:,:,0])
    if diag_cov:
        cov_pred_list_new = []
        print('ASSUMING COVARIANCE MATRIX IS DIAGONAL HERE')
        for indx_i in (range(len(cov_pred))):
            assert loss_type=='diag'
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
                            norm_images=True,log_norm_images=False,return_cov=True,h5=False,numpy_folder=False,
                            diag_cov = True):
    assert False #Need to fix the diagonal covariance stuff in this function. Have left it half done. Can I just have one function 
    #to do all of them, as they're all doing the same thing?
    assert (h5*numpy_folder)==0 #Only one of these can be true
    t1 = time.time()
    #The following code implementation here and in the hierarchical inference function below assumes a diagonal covariance matrix
    # if loss_type !='diag':
    #     raise ValueError('loss_type not supported in this notebook')

    std_pred_list = [];cov_pred_list = []
    if h5==True:
        print('Loading h5 file')
        images = load_h5_file(npy_file)
        images = images[...,np.newaxis]
        print('H5 shape',images.shape)
    elif numpy_folder ==True:
        print('Loading npy files from npy folder')
        npy_files = glob.glob(f'{npy_file}/*.npy')
        npy_files.sort()
        images = np.array([np.load(npy_file_i) for npy_file_i in tqdm(npy_files)])
        images = images[...,np.newaxis]
        #print('NPY SHAPE',images.shape)
    else: 
        print('Loading single npy file')
        images = np.load(npy_file)
        images = images[np.newaxis,...,np.newaxis]
    t2 = time.time()
    #print('SHAPE',images.shape)
    '''Normalising the images according to their standard deviation:'''
    images=images/np.std(images)
    t3 = time.time()
    # use unrotated output for covariance matrix
    output = model.predict(images)
    t4 = time.time()
    if diag_cov: 
        y_pred, log_var_pred = loss_func.convert_output(output)
        y_pred_list=[] #KEEP this in (even though it seems arbitrary) - otherwise the y_pred values aren't un-normalised and it will return the wrong answer!
        y_pred_list.append(y_pred)
        y_pred = np.concatenate(y_pred_list)
        t5 = time.time()
        # compute std. dev.
        std_pred = np.exp(log_var_pred/2)
        cov_pred = None
    else:
        y_pred_list = [];prec_pred_list = [];y_test_list = []
        y_pred, prec_pred, _ = loss_func.convert_output(output)
        y_test_list.append([y_test])
        y_pred_list.append(y_pred)
        prec_pred_list.append(prec_pred)
        y_test = np.concatenate(y_test_list)
        y_pred = np.concatenate(y_pred_list)
        prec_pred = np.concatenate(prec_pred_list)
        cov_pred = np.linalg.inv(prec_pred)
    if not return_cov and diag_cov=='diag':
        if input_norm_path is not None:
            print('Unnormalising outputs')
            dataset_generation.unnormalize_outputs(input_norm_path,learning_params+log_learning_params,
                                            y_pred,
                                            standard_dev=std_pred,cov_mat=None)
            t6 = time.time()
            if numpy_folder or h5: print({'t2-t1':t2-t1,'t3-t2':t3-t2,'t4-t3':t4-t3,'t5-t4':t5-t4,'t6-t5':t6-t5})
        return y_pred, std_pred
    if diag_cov:
        cov_mat = np.empty((len(std_pred),len(std_pred[0]),len(std_pred[0])))
        for i in range(len(std_pred)):
            assert loss_type=='diag'
            cov_mat[i] = np.diag(std_pred[i]**2)
        cov_pred_list.append(cov_mat)
        cov_pred = np.concatenate(cov_pred_list)
        cov_pred_list_new = []
        print('ASSUMING COVARIANCE MATRIX IS DIAGONAL HERE')
        for indx_i in (range(len(cov_pred))):
            assert loss_type=='diag'
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
    try:
        prec_pred = np.linalg.inv(cov_pred)
    except Exception as ex:
        print('Exception: NO LONGER RETURNING PRECISION MATRIX')
        print('RETURNING COV_PRED FOR DEBUGGING PURPOSES')
        return y_pred,std_pred,cov_pred
    return y_pred, std_pred, prec_pred

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
            assert loss_type=='diag'
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


def gen_network_predictions_general(test_folder,norm_path,learning_params,log_learning_params,loss_type,
                            loss_func,model,
                            norm_images=True,log_norm_images=False,
                            h5_or_not=None,N_max=None,
                            diag_cov = True,
                            specific_file_with_no_ground_truth=False,return_prec=True,return_loss_value = False):
    assert not log_norm_images #Not exactly sure what this variable means, but it isn't implemented/has no effect here!
    input_norm_path = norm_path
    if h5_or_not=='True':
        metadata_file = test_folder+'/metadata.csv'
        metadata_db = pd.read_csv(metadata_file)[learning_params+log_learning_params]
        print(f'Using {len(metadata_db)} images as a validation set, from {test_folder}')
        with h5py.File(f'{test_folder}/image_data.h5', "r") as f:
            image_list_0 = f['data'][()]
        N_images=len(metadata_db)
    #
    if h5_or_not=='False':
        test_data = glob.glob(f'{test_folder}/**/*.npy',recursive=True)
        #This is important: it assumes the order of the ground truth in the metadata files is the same
        #as the numbers given to the .npy files (i.e. that image_0000000.npy is the first one in the metadata)
        #file:
        test_data.sort()
        print('NB: Assume .npy filenames are an ordered list.')
        print(f'Using {len(test_data)} images as a test set, from {test_folder}')
        N_images=len(test_data)
    if specific_file_with_no_ground_truth:
        N_images = 1
        test_data = [test_folder]
    if N_max is not None:
        N_images = N_max #Just a quicker way to test the code
    image_list = []
    y_test_list = [];y_pred_list = []
    std_pred_list = [];cov_pred_list = [];prec_pred_list = []
    predict_samps_list = []
    if h5_or_not=='False':
        filename_0 = test_data[0]
        metadata_file = filename_0.split('image_')[0]+'metadata.csv' 
        y_test_db = pd.read_csv(metadata_file)
    for b_i in tqdm(range(N_images)):
        if h5_or_not=='False':
            t1 = time.time()
            filename_i = test_data[b_i]
            t2 = time.time()
            t3 = time.time()
            images = np.load(filename_i)
            t4 = time.time()
            # images = images[np.newaxis,...]
            # print('SHAPE',images.shape)
            y_test = y_test_db.loc[b_i][learning_params+log_learning_params].tolist()
            t5 = time.time()
        if h5_or_not=='True':
            images = image_list_0[b_i]
            # images = images[np.newaxis,...]
            y_test = np.array(metadata_db.loc[b_i])
            y_test = y_test[np.newaxis,...]
        if specific_file_with_no_ground_truth:
            images = np.load(test_folder)
            # images = images[np.newaxis,...]
        '''Normalising the images according to their standard deviation:'''
        if norm_images: images=images/np.std(images)
        t6 = time.time()
        image_list.append(images)
        t7 = time.time()
        if not specific_file_with_no_ground_truth: y_test_list.append([y_test])
        t8 = time.time()
        # print('Time taken:',{'t2-t1':t2-t1,'t3-t2':t3-t2,'t4-t3':t4-t3,'t5-t4':t5-t4,'t6-t5':t6-t5,'t7-t6':t7-t6,'t8-t7':t8-t7})
        # use unrotated output for covariance matrix
    image_list = np.array(image_list)
    if not specific_file_with_no_ground_truth: y_test_list = np.array(y_test_list)
    # print('Y_test',y_test.shape)
    output = model.predict(image_list)
    if return_loss_value:
        # print(output.shape)
        # print(norm_path)
        # print(y_test_list.shape)
        # print(loss_func)
        # print(loss_type)
        norm_values = pd.read_csv(input_norm_path)
        # print('NORM',norm_values)
        normalised_ground_truth = (y_test_list[:, 0, 0, :]-norm_values['mean'].to_numpy())/norm_values['std'].to_numpy()
        # print('ngt',normalised_ground_truth.shape)
        loss_value = loss_func.loss((normalised_ground_truth),(output))
        # print(loss_value)
        # print(dir(loss_value))
        return np.array(loss_value)
    # print('images shape',images.shape)
    # print('image list shape',image_list.shape)
    # print('y_test shape',y_test.shape)
    # print('output shape',output.shape)
    if diag_cov: 
        y_pred, log_var_pred = loss_func.convert_output(output)
        std_pred = np.exp(log_var_pred/2)
        cov_mat = np.empty((len(std_pred),len(std_pred[0]),len(std_pred[0])))
        for i in range(len(std_pred)):
            assert loss_type=='diag'
            cov_mat[i] = np.diag(std_pred[i]**2)
        cov_pred = cov_mat.copy()
        # print('y_pred',y_pred)
        # print('std_pred',std_pred)
        # print('cov_pred',cov_pred)
        # cov_pred_list_new = []
        # print('ASSUMING COVARIANCE MATRIX IS DIAGONAL HERE')
        # for indx_i in (range(len(cov_pred))):
        #     assert loss_type=='diag'
        #     diag_i = np.diag(cov_pred[indx_i,:,:])
        #     diag_ii = diag_i.copy()
        #     diag_ii[diag_ii==0]=np.nan
        #     cov_pred_list_new.append([np.diag(diag_ii)])
        # cov_pred = np.concatenate(cov_pred_list_new)
    else:
        y_pred, prec_pred, _ = loss_func.convert_output(output)
        cov_pred = np.linalg.inv(prec_pred)
        std_pred = np.array([np.diag(cov_pred[m_i,:,:])**0.5 for m_i in range(cov_pred.shape[0])])
        # print('std shape',std_pred.shape)
        # print('y_pred',y_pred)
        # print('std_pred',std_pred)
        # print('cov_pred',cov_pred)
        # print('prec_pred',prec_pred)
    y_pred = np.array(y_pred).copy()
    if input_norm_path is not None:
        print('Unnormalising outputs')
        dataset_generation.unnormalize_outputs(input_norm_path,learning_params+log_learning_params,
                                        y_pred,standard_dev=std_pred,cov_mat=cov_pred)
    '''Am NOT unnormalising the y_test values here, since in this case I am taking the ground-truth
    from the metadata.csv files, which are already unnormalised:
    dataset_generation.unnormalize_outputs(input_norm_path,learning_params+log_learning_params,
                                        y_test)
    '''
    if return_prec: prec_pred = np.linalg.inv(cov_pred)
    # print('Unnormalised y_pred',y_pred)
    # print('Unnormalised std_pred',std_pred)
    # print('Unnormalised cov_pred',cov_pred)
    # print('Unnormalised prec_pred',prec_pred)
    print(np.array(y_test_list).shape)
    if specific_file_with_no_ground_truth:
        if return_prec: return y_pred,std_pred,prec_pred
        else: return y_pred,std_pred
    else:
        if return_prec: 
            print('returning prec')
            return y_test_list, y_pred, std_pred, prec_pred
        else: return y_test_list, y_pred, std_pred