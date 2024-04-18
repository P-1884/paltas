import glob
import os
import numpy as np
from paltas.Analysis import loss_functions,conv_models

def load_model_weights_list(directory):
    """ Function to return a list of weights filenames from the network
    args: Directory containing the training, validation and weights files """
    weights_list = glob.glob(f'{directory}/model_weights/*')
    weights_list = [elem.split('model_weights/')[1] for elem in weights_list]
    return weights_list

def return_final_epoch_weights(directory):
    """ File to return the weight filename of the final trained epoch
    args: Directory containing the training, validation and weights files """
    weights_list = load_model_weights_list(directory)
    print(f'Found {weights_list} model weights')
    final_epoch =  np.max([int(elem.split('-')[0]) for elem in weights_list])
    w_filename = [x for x in weights_list if x.startswith("{:02d}".format(final_epoch)+'-')][0]
    print('FINAL EPOCH',w_filename)
    return directory+'/model_weights/'+w_filename

def return_list_of_weight_files(directory):
    '''Returns list of weight files, ordered by their creation date'''
    files = list(filter(os.path.isfile, glob.glob(f'{directory}/model_weights/*h5')))
    files.sort(key=lambda x: os.path.getmtime(x))
    return files

def load_model(model_weights_filename,loss_type,model_type,learning_params,log_learning_params,img_size):
    """ Loads the trained model
    args: 
    model_weights_filename (str): .h5 file containing the weights of the trained model.
    loss_type (str): 'full' or 'diag', depending on the type of covariance matrix chosen
    model type (str): 'xresnet34' or 'xresnet101', according to the choice of network
    learning_params (list of str): Parameters learnt by the network
    img_size (int): Dimensions of the input images"""
    print(f'Loading model from {model_weights_filename}')
    num_params = len(learning_params+log_learning_params)
    if loss_type == 'full':
        num_outputs = num_params + int(num_params*(num_params+1)/2)
        loss_func = loss_functions.FullCovarianceLoss(num_params)
    elif loss_type == 'diag':
        num_outputs = 2*num_params
        loss_func = loss_functions.DiagonalCovarianceLoss(num_params)
    if model_type == 'xresnet101':
        model = conv_models.build_xresnet101(img_size,num_outputs)
    if model_type == 'xresnet34':
        model = conv_models.build_xresnet34(img_size,num_outputs)
    try:
        print('Loading weights with by_name=True')
        model.load_weights(model_weights_filename,by_name=True,skip_mismatch=True)
    except:
        print('Loading weights without by_name kwarg')
        model.load_weights(model_weights_filename,skip_mismatch=True)
    return model,loss_func,num_params