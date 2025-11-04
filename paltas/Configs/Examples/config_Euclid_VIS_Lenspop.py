# Includes a PEMD deflector with external shear, and Sersic sources. 

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
numpix = 120
mask_radius = 0
mag_cut = 0.0
catalog = False
save_noise=False
add_RSP_background=False
# Define arguments that will be used multiple times
output_ab_zeropoint = 25.5

config_dict = {
'main_deflector':{
'class': PEMDShear,
'parameters':{
'M200': 1e13,
'z_lens':truncnorm(-1.615,np.inf,loc=0.7106,scale=0.44).rvs,
'gamma':truncnorm(-3.7879,np.inf,loc=2.0,scale=0.264).rvs,
'theta_E':truncnorm(-1.5312,np.inf,loc=0.7345,scale=0.4797).rvs,
'e1':norm(loc=-0.0001,scale=0.1955).rvs,
'e2':norm(loc=-0.002,scale=0.1956).rvs,
'center_x':norm(loc=0.0,scale=0.12).rvs,
'center_y':norm(loc=0.0,scale=0.12).rvs,
'gamma1':norm(loc=0.0,scale=0.078).rvs,
'gamma2':norm(loc=0.0,scale=0.078).rvs,
'ra_0':0.0, 'dec_0':0.0
}
},
'lens_light':{
'class': SingleSersicSource,
'parameters':{
'z_source':truncnorm(-1.615,np.inf,loc=0.7106,scale=0.44).rvs,
'mag_app':norm(loc=21.0459,scale=3.0078).rvs,
'output_ab_zeropoint':output_ab_zeropoint,
'R_sersic':truncnorm(-1.6216,np.inf,loc=0.5951,scale=0.367).rvs,
'n_sersic':4.0,
'e1':norm(loc=-0.0001,scale=0.1955).rvs,
'e2':norm(loc=-0.002,scale=0.1956).rvs,
'center_x':norm(loc=0.0,scale=0.12).rvs,
'center_y':norm(loc=0.0,scale=0.12).rvs,
}
},
'source':{
'class': SingleSersicSource,
'parameters':{
'z_source':truncnorm(-1.8547,np.inf,loc=1.9469,scale=1.0497).rvs,
'mag_app':norm(loc=25.515,scale=1.3961).rvs,
'output_ab_zeropoint':output_ab_zeropoint,
'R_sersic':truncnorm(-0.928,np.inf,loc=0.1588,scale=0.1712).rvs,
'n_sersic':1.0,
'e1':norm(loc=-0.0024,scale=0.2315).rvs,
'e2':norm(loc=-0.0008,scale=0.2299).rvs,
'center_x':norm(loc=0.0007,scale=0.2748).rvs,
'center_y':norm(loc=0.0034,scale=0.3658).rvs,
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
'fwhm': 0.18

}
},


'detector':{
'parameters':{
'pixel_scale':0.1,'ccd_gain':3.1,'read_noise':4.2,
'magnitude_zero_point':25.5,
'exposure_time':565,'sky_brightness':22.35,
'num_exposures':4,'background_noise':None
}
},
'lens_subtraction':True,
'cross_object':{
'parameters':{
('main_deflector:center_x,main_deflector:center_y,lens_light:center_x,lens_light:center_y'):
dist.DuplicateXY(
x_dist=norm(loc=0.0,scale=0.12).rvs, 
y_dist=norm(loc=0.0,scale=0.12).rvs),
'main_deflector:z_lens,source:z_source':dist.RedshiftsTruncNorm( 
z_lens_min=0,z_lens_mean=0.7106,z_lens_std=0.44,
z_source_min=0,z_source_mean=1.9469,z_source_std=1.0497)
}
}
}