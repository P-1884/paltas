import numpy as np
import pandas as pd

def make_val_databases(network_predictions_dict,key,training_directory,learning_params,log_learning_params):
    val_or_test_HI = 'val'
    try: del test_data_db,test_data_db_sum
    except: pass
    final_epoch = key#max(list(network_predictions_dict.keys()))
    network_means = network_predictions_dict[final_epoch][1][:,:].astype('float64')              
    network_prec = network_predictions_dict[final_epoch][3][:,:,:].astype('float64')
    metadata_val = pd.read_csv(training_directory+'/validation/2/metadata.csv')

    final_epoch_n = key#np.max(list(network_predictions_dict.keys()))
    network_truth_db = pd.DataFrame(network_predictions_dict[final_epoch_n][0],columns=learning_params+log_learning_params)
    network_pred_mu_db = pd.DataFrame(network_predictions_dict[final_epoch_n][1],columns=learning_params+log_learning_params)
    network_std_db = pd.DataFrame(network_predictions_dict[final_epoch_n][2],columns=learning_params+log_learning_params)

    bright_source_indx = np.where(metadata_val['source_parameters_mag_app']<25)[0]
    #Assert that the true parameters from the metadata are equal to those I'm getting from gen_network_predictions, to make sure there hasn't been any reshuffling
    #and to make sure I'm comparing the properties of the same objects. The 'round' is to remove the problem of some being saved as float32 and others as float64 files.
    db_a = np.round(network_truth_db[learning_params].astype('float32'),3)
    db_b = np.round(metadata_val[learning_params].astype('float32'),3)
    print('DB Comparison',len(db_a),len(db_b),len(db_a.columns),len(db_b.columns))
    assert (db_a==db_b).all().all()
    return metadata_val,network_truth_db,network_pred_mu_db,network_std_db,bright_source_indx

def make_test_databases(network_predictions_test_dict,key,training_directory,learning_params,log_learning_params):
    val_or_test_HI='test'
    try: del bright_source_indx
    except: pass
    final_epoch = max(list(network_predictions_test_dict.keys()))
    network_means = network_predictions_test_dict[final_epoch][1][:,:].astype('float64')              
    network_prec = network_predictions_test_dict[final_epoch][3][:,:,:].astype('float64')
    metadata_val = pd.DataFrame(network_predictions_test_dict[0][0],columns=learning_params+log_learning_params)
    
    final_epoch_n = np.max(list(network_predictions_test_dict.keys()))
    network_truth_db = pd.DataFrame(network_predictions_test_dict[final_epoch_n][0],columns=learning_params+log_learning_params)
    network_pred_mu_db = pd.DataFrame(network_predictions_test_dict[final_epoch_n][1],columns=learning_params+log_learning_params)
    network_std_db = pd.DataFrame(network_predictions_test_dict[final_epoch_n][2],columns=learning_params+log_learning_params)

    test_data_db = metadata_val.copy()
    test_data_db_sum = test_data_db.describe()
    #Assert that the true parameters from the metadata are equal to those I'm getting from gen_network_predictions, to make sure there hasn't been any reshuffling
    #and to make sure I'm comparing the properties of the same objects. The 'round' is to remove the problem of some being saved as float32 and others as float64 files.
    db_a = network_truth_db[learning_params].astype('float32')
    db_b = metadata_val[learning_params].astype('float32')
    print('DB Comparison',len(db_a),len(db_b),len(db_a.columns),len(db_b.columns))
    assert (np.round(db_a,3)==np.round(db_b,3)).all().all()
    return metadata_val,network_truth_db,network_pred_mu_db,network_std_db