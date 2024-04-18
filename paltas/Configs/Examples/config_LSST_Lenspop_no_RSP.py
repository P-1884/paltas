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

#Asserting this as otherwise need to update read_noise and sky-brightness (and maybe gain too):
#assert add_RSP_background==True

config_dict = {
'main_deflector':{
'class': PEMDShear,
'parameters':{
'M200': 1e13,
'z_lens':truncnorm(-1.1881,np.inf,loc=0.421,scale=0.3544).rvs,
'gamma':truncnorm(-3.0303,np.inf,loc=2.0,scale=0.33).rvs,
'theta_E':truncnorm(-2.6075,np.inf,loc=1.5407,scale=0.5909).rvs,
'e1':norm(loc=0.0194,scale=0.2039).rvs,
'e2':norm(loc=0.0012,scale=0.2084).rvs,
'center_x':norm(loc=0.0,scale=0.15).rvs,
'center_y':norm(loc=0.0,scale=0.15).rvs,
'gamma1':norm(loc=0.0,scale=0.0975).rvs,
'gamma2':norm(loc=0.0,scale=0.0975).rvs,
'ra_0':0.0, 'dec_0':0.0
}
},
'lens_light':{
'class': SingleSersicSource,
'parameters':{
'z_source':truncnorm(-1.1881,np.inf,loc=0.421,scale=0.3544).rvs,
'mag_app':norm(loc=17.5732,scale=2.7737).rvs,
'output_ab_zeropoint':output_ab_zeropoint,
'R_sersic':truncnorm(-0.9474,np.inf,loc=1.144,scale=1.2076).rvs,
'n_sersic':4.0,
'e1':norm(loc=0.0194,scale=0.2039).rvs,
'e2':norm(loc=0.0012,scale=0.2084).rvs,
'center_x':norm(loc=0.0,scale=0.15).rvs,
'center_y':norm(loc=0.0,scale=0.15).rvs,
}
},
'source':{
'class': SingleSersicSource,
'parameters':{
'z_source':truncnorm(-1.3248,np.inf,loc=1.8248,scale=1.3774).rvs,
'mag_app':norm(loc=24.4683,scale=1.5905).rvs,
'output_ab_zeropoint':output_ab_zeropoint,
'R_sersic':truncnorm(-1.0747,np.inf,loc=0.4028,scale=0.3748).rvs,
'n_sersic':1.0,
'e1':norm(loc=0.0065,scale=0.2767).rvs,
'e2':norm(loc=-0.0037,scale=0.2852).rvs,
'center_x':norm(loc=-0.0358,scale=0.6046).rvs,
'center_y':norm(loc=0.0264,scale=0.7291).rvs,
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
'lens_subtraction':True,
'cross_object':{
'parameters':{
('main_deflector:center_x,main_deflector:center_y,lens_light:center_x,lens_light:center_y'):
dist.DuplicateXY(
x_dist=norm(loc=0.0,scale=0.15).rvs, 
y_dist=norm(loc=0.0,scale=0.15).rvs),
'main_deflector:z_lens,source:z_source':dist.RedshiftsTruncNorm( 
z_lens_min=0,z_lens_mean=0.421,z_lens_std=0.3544,
z_source_min=0,z_source_mean=1.8248,z_source_std=1.3774)
}
}
}