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
save_noise=True
add_RSP_background=False
# Define arguments that will be used multiple times
output_ab_zeropoint = 31.8#27.79

config_dict = {
'main_deflector':{
'class': PEMDShear,
'parameters':{
'M200': 1e13,
'z_lens':truncnorm(-1.6097,np.inf,loc=0.4878,scale=0.303).rvs,
'gamma':truncnorm(-3.7879,np.inf,loc=2.0,scale=0.264).rvs,
'theta_E':truncnorm(-3.2117,np.inf,loc=1.4151,scale=0.4406).rvs,
'e1':norm(loc=-0.0011,scale=0.1708).rvs,
'e2':norm(loc=-0.0005,scale=0.1709).rvs,
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
'z_source':truncnorm(-1.6097,np.inf,loc=0.4878,scale=0.303).rvs,
'mag_app':norm(loc=18.2981,scale=2.1232).rvs,
'output_ab_zeropoint':output_ab_zeropoint,
'R_sersic':truncnorm(-1.5478,np.inf,loc=0.9326,scale=0.6025).rvs,
'n_sersic':4.0,
'e1':norm(loc=-0.0011,scale=0.1708).rvs,
'e2':norm(loc=-0.0005,scale=0.1709).rvs,
'center_x':norm(loc=0.0,scale=0.12).rvs,
'center_y':norm(loc=0.0,scale=0.12).rvs,
}
},
'source':{
'class': SingleSersicSource,
'parameters':{
'z_source':truncnorm(-2.0527,np.inf,loc=2.1306,scale=1.038).rvs,
'mag_app':norm(loc=25.5952,scale=1.3289).rvs,
'output_ab_zeropoint':output_ab_zeropoint,
'R_sersic':truncnorm(-1.1609,np.inf,loc=0.2754,scale=0.2373).rvs,
'n_sersic':1.0,
'e1':norm(loc=0.0007,scale=0.2302).rvs,
'e2':norm(loc=-0.0023,scale=0.2286).rvs,
'center_x':norm(loc=-0.0081,scale=0.4621).rvs,
'center_y':norm(loc=0.0022,scale=0.6193).rvs,
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
'pixel_scale':0.2,'ccd_gain':2.3,'read_noise':10,
'magnitude_zero_point':output_ab_zeropoint,
'exposure_time':30,'sky_brightness':20.48,
'num_exposures':230,'background_noise':None
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
z_lens_min=0,z_lens_mean=0.4878,z_lens_std=0.303,
z_source_min=0,z_source_mean=2.1306,z_source_std=1.038)
}
}
}