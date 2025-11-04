# Includes a PEMD deflector with external shear, and Sersic sources. 
# Designed to be similar to LSST-like images (though background noise is not yet implemented.)

import numpy as np
from scipy.stats import norm, truncnorm, uniform
paltas_directory = '/Users/hollowayp/paltas/'
import sys
sys.path.append(paltas_directory)
import paltas.Sampling.distributions as dist
from paltas.MainDeflector.simple_deflectors import PEMDShear
from paltas.Sources.sersic import SingleSersicSource
from paltas.Substructure.subhalos_dg19 import SubhalosDG19

# Define the numerics kwargs.
kwargs_numerics = {'supersampling_factor':1}
# This is always the number of pixels for the CCD. If drizzle is used, the
# final image will be larger.
numpix = 60
mask_radius = 0
mag_cut = 0.0
catalog = False
save_noise=False
add_RSP_background=False
RSP_cutout_folder='/mnt/zfsusers/hollowayp/paltas/RSP_Coadd_Files_100000/'
RSP_ZP = 27 #Zeropoint for the coadds
output_ab_zeropoint = 27.85 #From https://smtn-002.lsst.io/. Refers to ZP which gives 1e/s. Is fainter in ADU (when gain=0.7)

# mean_Re = 1.1
# mean_mag = 17.6
# sigma_Re = 0.1
# sigma_mag = 0.1
# sigma_offdiag = 0.9*np.sqrt(sigma_Re*sigma_mag) #0.9 of max possible covariance

# Re_mag_dist = dist.TruncatedMultivariateNormal(np.array([mean_mag,mean_Re]),
#                                                np.array([[sigma_mag**2,sigma_offdiag**2],
#                                                          [sigma_offdiag**2,sigma_Re**2]]),
#                                                np.array([0,0]),None)

config_dict = {
'main_deflector':{
'class': PEMDShear,
'parameters':{
'M200': 1e13,
'z_lens':0.5,
'gamma':uniform(loc=1.8,scale=0.4).rvs,
'theta_E':uniform(loc=2.0,scale=1.0).rvs,
'e1':uniform(loc=-0.1,scale=0.2).rvs,
'e2':uniform(loc=-0.1,scale=0.2).rvs,
'center_x':0.0,
'center_y':0.0,
'gamma1':uniform(loc=-0.1,scale=0.2).rvs,
'gamma2':uniform(loc=-0.1,scale=0.2).rvs,
'ra_0':0.0, 'dec_0':0.0
}
},
'lens_light':{
'class': SingleSersicSource,
'parameters':{
'z_source':0.5,
'mag_app':17.6,
'output_ab_zeropoint':output_ab_zeropoint,
'R_sersic':uniform(loc=1.0,scale=1.0).rvs,
'n_sersic':4.0,
'e1':uniform(loc=-0.1,scale=0.2).rvs,
'e2':uniform(loc=-0.1,scale=0.2).rvs,
'center_x':0.0,
'center_y':0.0,
}
},
'source':{
'class': SingleSersicSource,
'parameters':{
'z_source':1.0,
'mag_app':20,
'output_ab_zeropoint':output_ab_zeropoint,
'R_sersic':uniform(loc=0.1,scale=0.4).rvs,
'n_sersic':1.0,
'e1':uniform(loc=-0.1,scale=0.2).rvs,
'e2':uniform(loc=-0.1,scale=0.2).rvs,
'center_x':uniform(loc=-1.0,scale=2.0).rvs,
'center_y':uniform(loc=-1.0,scale=2.0).rvs,
}
},
'cosmology':{
'parameters':{
'cosmology_name': 'planck18'
}
},
'psf':{
'parameters':{
'psf_type':'GAUSSIAN',
'fwhm': 0.71

}
},
'detector':{
'parameters':{
'pixel_scale':0.2,'ccd_gain':2.3,'read_noise':10, #Noise is added from RSP. Gain from here https://community.lsst.org/t/dp0-zeropoints-adding-poisson-noise/8230/7, correct for DP0
'magnitude_zero_point':output_ab_zeropoint,
'exposure_time':30,'sky_brightness':20.48,
'num_exposures':100,'background_noise':None  #Number of exposures matching the DP0 coadds.
}
},
'lens_subtraction':False,
# 'cross_object':{
# 'parameters':{
# 'lens_light:mag_app,lens_light:R_sersic':Re_mag_dist}
# }
}