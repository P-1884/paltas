from glob import glob
import numpy as np

def load_model_weights_list(directory):
    """ Function to return a list of weights filenames from the network
    args: Directory containing the training, validation and weights files """
    weights_list = glob(f'{directory}/model_weights/*')
    weights_list = [elem.split('model_weights/')[1] for elem in weights_list]
    return weights_list

def return_final_epoch_weights(directory):
    """ File to return the weight filename of the final trained epoch
    args: Directory containing the training, validation and weights files """
    weights_list = load_model_weights_list(directory)
    print(weights_list)
    final_epoch =  np.max([int(elem.split('-')[0]) for elem in weights_list])
    w_filename = [x for x in weights_list if x.startswith("{:02d}".format(final_epoch)+'-')][0]
    print('FINAL EPOCH',w_filename)
    return directory+'/model_weights/'+w_filename