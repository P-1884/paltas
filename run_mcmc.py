import numpy as np
from paltas.Analysis import hierarchical_inference
import sys
import time
import numba
import pandas as pd
import emcee
import h5py

from scipy.stats import multivariate_normal

def multi_dim_gaussian(x):
    return np.log(multivariate_normal.pdf(x,mean=np.array(prior_db_indx_for_HI['mean']).tolist()+
                                                 np.array(prior_db_indx_for_HI['std']).tolist(),
                                   cov=0.01))

def hierarchical_inference_func(n_lenses,y_pred,prec_pred,train_mean,train_scatter,
                                prior_db_mean,prior_db_std,n_samps = 1e+4,lp_for_HI=None):
    """
    Returns:
        sampler object
    """
    # Load the predictions for the mean and covariance for our model. We'll have to do a little reshaping here since the code
    # expect an array of mean values and a precision matrix.
    #y_pred_hi = y_pred
    #prec_pred_hi = prec_pred

####
    y_pred_hi = np.ascontiguousarray(y_pred[:n_lenses,:len(lp_for_HI)]).reshape((n_lenses,len(lp_for_HI))).astype(np.float64)
    prec_pred_hi = np.ascontiguousarray(prec_pred[:n_lenses,:len(lp_for_HI),:len(lp_for_HI)]).reshape(
                                                  (n_lenses,len(lp_for_HI),len(lp_for_HI))).astype(np.float64)
####
    # The interim training distribution.
    mu_omega_i = np.array(train_mean)
    cov_omega_i = np.diag(np.array(train_scatter)**2)
    ndim = 2*len(learning_params_for_HI)
    gamma_indx = np.where(np.array(lp_for_HI)=='gamma')
    # uniform prior with bounds
    @numba.njit()
    def eval_func_omega(hyperparameters):
        loc_learning_params = prior_db_mean
        sig_learning_params = prior_db_std
        for i in range(len(loc_learning_params)):
            if abs(hyperparameters[i]-loc_learning_params[i])>3*sig_learning_params[i]: #Shouldn't be too small - expect some values to be outside 1 sigma.
                return -np.inf
        for h in hyperparameters[len(loc_learning_params):]:
            # penalize too narrow
            if h < -6.9: #NOTE: sigmas are in **natural** logarithm space, so this equates to e^-6.9 = 0.001.
                return -np.inf
            # penalize too wide
            if h > 0.69: #NOTE: sigmas are in **natural** logarithm space, so this equates to e^0.69 = 2
                return -np.inf
        if hyperparameters[gamma_indx]<1 or hyperparameters[gamma_indx]>3:
            return -np.inf
        # log prior for uniform in sigma space, as opposed to uniform in log space
        #PH: See perhaps this page for a starting point for this: https://stats.stackexchange.com/questions/323859/why-is-uniform-prior-on-logx-equal-to-1-x-prior-on-x
        #Update from Sydney: Should just be returning 0 here.
        return 0 #np.sum(hyperparameters[int(ndim/2):])

    # Initialize our class and then give it the network predictions. These are set to global variables in case you want to use
    # pooling.
    prob_class = hierarchical_inference.ProbabilityClassAnalytical(mu_omega_i,cov_omega_i,eval_func_omega)
    prob_class.set_predictions(mu_pred_array_input=y_pred_hi,prec_pred_array_input=prec_pred_hi)

    # Set a few of the parameters we will need to pass to emcee
    n_walkers = 40
    # Generate an initial state informed by prior range.
    # UPDATE: If these ranges are too wide (e.g. outside the training prior), I don't think the walkers will ever see anywhere with a non-zero loss (as set loss to
    # -inf above), so they won't ever evolve/walk anywhere.
    '''
    For infering toy MVN distribution:
    cur_state_mu = np.concatenate([np.random.uniform(low=-1,high=1,size=(n_walkers,1)) for elem in lp_for_HI],axis=1)
    cur_state_sigmas = np.concatenate([np.random.uniform(low=-1,high=1,size=(n_walkers,1)) for elem in lp_for_HI],axis=1)
    '''
    cur_state_mu = np.concatenate([np.random.uniform(
                                    low=prior_db_indx_for_HI.loc[elem]['mean']-2*prior_db_indx_for_HI.loc[elem]['std'],
                                    high=prior_db_indx_for_HI.loc[elem]['mean']+2*prior_db_indx_for_HI.loc[elem]['std'] ,
                                    size=(n_walkers,1)) for elem in lp_for_HI],axis=1)
    cur_state_sigmas = np.log(np.concatenate([np.random.uniform(
                                    low= 0.99*prior_db_indx_for_HI.loc[elem]['std'], #0.1% of sigma lower limit
                                    high=1.01*prior_db_indx_for_HI.loc[elem]['std'], #10-sigma upper limit
                                    #low=0.001,high=2,
                                    size=(n_walkers,1)) for elem in lp_for_HI],axis=1))
    cur_state = np.concatenate((cur_state_mu,cur_state_sigmas),axis=1)
    #Saving file
    filename = f"{model_directory}/mcmc_files/"
    #backend = emcee.backends.HDFBackend(filename+f'{int(time.time())}.h5')
    #backend.reset(int(n_walkers), int(ndim))
    sampler = emcee.EnsembleSampler(n_walkers, ndim, prob_class.log_post_omega)#,backend=backend)
    _ = sampler.run_mcmc(cur_state,n_samps,progress=True,skip_initial_state_check=True)
    print('Chain shape',np.shape(sampler.chain))
    save_time = int(time.time())
    print(f'Saving under ../mcmc_chains_{save_time}.npy')
    np.save(filename+f'/mcmc_chains_{save_time}.npy',sampler.chain)
    Acceptance_fraction = sampler.acceptance_fraction
    print(f'Acceptance fraction: {Acceptance_fraction},{len(Acceptance_fraction)}')
    Autocorr_time = sampler.get_autocorr_time(discard = int(n_samps/2))
    print(f'Autocorr time (50% Burnin): {Autocorr_time},{len(Autocorr_time)}')
    return sampler

argv = sys.argv
#NOTE, ADDING FURTHER ARGUMENTS TO THE END OF THE ADDQUEUE STATEMENT WILL CHANGE WHAT INDICES THESE SHOULD BE:
num_params = int(argv[-1])
n_samps = int(argv[-2])
model_directory = argv[-3]

network_means = np.load(model_directory+'/mcmc_files/network_means.npy') #[system_no, parameter]
network_prec = np.load(model_directory+'/mcmc_files/network_prec.npy') #[system_no, parameter, parameter]
train_mean = np.load(model_directory+'/mcmc_files/train_mean.npy') #[parameter]
train_scatter = np.load(model_directory+'/mcmc_files/train_scatter.npy') #[parameter]
learning_params = np.load(model_directory+'/mcmc_files/learning_params.npy') #[parameter]
prior_db_indx = pd.read_csv(model_directory+'/mcmc_files/prior_db_indx.csv',index_col=0)
print('prior_db_indx',prior_db_indx)

learning_params_for_HI = ['main_deflector_parameters_theta_E','main_deflector_parameters_gamma',
                          #'main_deflector_parameters_gamma1','main_deflector_parameters_gamma2']
                          #'main_deflector_parameters_center_x','main_deflector_parameters_center_y',
                          'main_deflector_parameters_e2']
learning_params_indx = [np.where(np.array(learning_params)==elem)[0][0] for elem in learning_params_for_HI]
network_means_for_HI = network_means[:,learning_params_indx]
network_prec_for_HI = np.nan*np.zeros((len(network_prec[:,0,0]),len(learning_params_indx),len(learning_params_indx)))
train_mean_for_HI = train_mean[learning_params_indx]
train_scatter_for_HI = train_scatter[learning_params_indx]
prior_db_indx_for_HI = prior_db_indx.loc[learning_params_for_HI]
                                              
#Cropping network precision matrix:
for i in range(len(network_prec_for_HI[:,0,0])):
    network_prec_i = network_prec[i,:,:]
    assert np.count_nonzero(network_prec_i - np.diag(np.diagonal(network_prec_i)))==0 #Assert precision matrix is diagonal, otherwise this indexing code won't work.
    diag_i = np.diag(network_prec_i)[learning_params_indx]
    network_prec_for_HI[i,:,:]=np.diag(diag_i)

assert np.sum(np.isnan(network_prec_for_HI))==0 #Assert no nan's in precision matrix.

print(f'Infering {len(learning_params_for_HI)} parameters, with n_samps:{n_samps} and model_directory:{model_directory}')

n_lenses = 1000
sampler = hierarchical_inference_func(n_lenses,
                                    network_means_for_HI,
                                    network_prec_for_HI,\
                                    train_mean_for_HI.astype('float64'),
                                    train_scatter_for_HI.astype('float64'),
                                    prior_db_mean=np.array(prior_db_indx_for_HI['mean']),
                                    prior_db_std=np.array(prior_db_indx_for_HI['std']),
                                    n_samps=n_samps,
                                    lp_for_HI=learning_params_for_HI)
