# Includes a PEMD deflector with external shear, and Sersic sources. 
# Designed to be similar to LSST-like images (though background noise is not yet implemented.)

import numpy as np
from scipy.stats import norm, truncnorm, uniform
paltas_directory = '/mnt/zfsusers/hollowayp/paltas'#'/Users/hollowayp/paltas/'
import sys
sys.path.append(paltas_directory)
import paltas.Sampling.distributions as dist
from paltas.MainDeflector.simple_deflectors import PEMDShear
from paltas.Sources.sersic import SingleSersicSource
from paltas.PointSource.single_point_source import SinglePointSource
from lenstronomy.Util import kernel_util
from lenstronomy.Util.param_util import phi_q2_ellipticity
import pandas as pd
import os
import paltas

# Define the numerics kwargs.
kwargs_numerics = {'supersampling_factor':1}
# This is always the number of pixels for the CCD. If drizzle is used, the
# final image will be larger.
numpix = 60
mask_radius = 0
mag_cut = 3.0
catalog = False
save_noise=False
add_RSP_background=True
RSP_cutout_folder='/mnt/extraspace/hollowayp/paltas_data/Coadd_files/'
RSP_ZP = 27 #Zeropoint for the coadds
output_ab_zeropoint = 27.85 #From https://smtn-002.lsst.io/. Refers to ZP which gives 1e/s. Is fainter in ADU (when gain=0.7)

#Asserting this as otherwise need to update read_noise and sky-brightness (and maybe gain too):
assert add_RSP_background==True

config_dict = {
'main_deflector':{
'class': PEMDShear,
'parameters':{
'M200': 1e13,
'z_lens':truncnorm(-1.5154,np.inf,loc=0.42,scale=0.2771).rvs,
'gamma':truncnorm(-7.5,np.inf,loc=1.98,scale=0.264).rvs,
'theta_E':truncnorm(-3.3298,np.inf,loc=1.5157,scale=0.4552).rvs,
'e1':norm(loc=0.0012,scale=0.1593).rvs,
'e2':norm(loc=0.0015,scale=0.1595).rvs,
'center_x':norm(loc=0.0,scale=0.24).rvs,
'center_y':norm(loc=0.0,scale=0.24).rvs,
'gamma1': None,
'gamma2': None,
'ra_0':0.0, 'dec_0':0.0
}
},
'lens_light':{
'class': SingleSersicSource,
'parameters':{
'z_source':truncnorm(-1.5154,np.inf,loc=0.42,scale=0.2771).rvs,
'mag_app':norm(loc=17.6226,scale=2.0986).rvs,
'output_ab_zeropoint':output_ab_zeropoint,
'R_sersic':truncnorm(-1.463,np.inf,loc=1.0818,scale=0.7394).rvs,
'n_sersic':4.0,
'e1':norm(loc=0.0012,scale=0.1593).rvs,
'e2':norm(loc=0.0015,scale=0.1595).rvs,
'center_x':norm(loc=0.0,scale=0.24).rvs,
'center_y':norm(loc=0.0,scale=0.24).rvs,
}
},
'source':{
'class': SingleSersicSource,
'parameters':{
'z_source':truncnorm(-1.7042,np.inf,loc=1.8224,scale=1.0693).rvs,
'mag_app':norm(loc=24.4371,scale=1.2491).rvs,
'output_ab_zeropoint':output_ab_zeropoint,
'R_sersic':truncnorm(-1.4217,np.inf,loc=0.3951,scale=0.2779).rvs,
'n_sersic':1.0,
'e1':norm(loc=-0.0016,scale=0.2269).rvs,
'e2':norm(loc=-0.0004,scale=0.2271).rvs,
'd_center_x':norm(loc=-0.0021,scale=0.478).rvs,
'd_center_y':norm(loc=-0.0032,scale=0.5873).rvs,
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
'pixel_scale':0.2,'ccd_gain':0.7,'read_noise':0, #Noise is added from RSP. Gain from here https://community.lsst.org/t/dp0-zeropoints-adding-poisson-noise/8230/7, correct for DP0
'magnitude_zero_point':output_ab_zeropoint,
'exposure_time':30,'sky_brightness':100, #Sky needs to be faint, as added in from RSP. Exposure time must = 30 for RSP.
'num_exposures':None,'background_noise':None
}
},
'lens_subtraction':True,
'cross_object':{
'parameters':{
('main_deflector:center_x,main_deflector:center_y,lens_light:center_x,lens_light:center_y'):
dist.DuplicateXY(
x_dist=norm(loc=0.0,scale=0.24).rvs, 
y_dist=norm(loc=0.0,scale=0.24).rvs),
'main_deflector:z_lens,source:z_source':dist.RedshiftsTruncNorm( 
z_lens_min=0,z_lens_mean=0.42,z_lens_std=0.2771,
z_source_min=0,z_source_mean=1.8224,z_source_std=1.0693),
'main_deflector:gamma1,main_deflector:gamma2':dist.ExternalShearTranslation(
gamma_dist=norm(loc=0.09,scale=0.102).rvs, 
phi_dist=uniform(loc=0,scale=2*np.pi).rvs),
}
}
}
