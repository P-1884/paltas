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
# Define arguments that will be used multiple times
output_ab_zeropoint = 27.79

config_dict = {
'main_deflector':{
'class': PEMDShear,
'parameters':{
'M200': 1e13,
'z_lens':'abc',#truncnorm(-2,np.inf,loc=0.5,scale=0.25).rvs,
'gamma':truncnorm(-4,np.inf,loc=2.0,scale=0.25).rvs,
'theta_E':truncnorm(-3,np.inf,loc=1.5,scale=0.5).rvs,
'e1':0.0,
'e2':0.0,
'center_x':0.0,
'center_y':0.0,
'gamma1':0.0,
'gamma2':0.0,
'ra_0':0.0, 'dec_0':0.0
}
},
'lens_light':{
'class': SingleSersicSource,
'parameters':{
'z_source':'def',#truncnorm(-2,np.inf,loc=0.5,scale=0.25).rvs,
'mag_app':norm(loc=18,scale=2).rvs,
'output_ab_zeropoint':output_ab_zeropoint,
'R_sersic':truncnorm(-2,np.inf,loc=1,scale=0.5).rvs,
'n_sersic':4.0,
'e1':0.0,
'e2':0.0,
'center_x':0.0,
'center_y':0.0,
}
},
'source':{
'class': SingleSersicSource,
'parameters':{
'z_source':truncnorm(-2,np.inf,loc=1,scale=0.5).rvs,
'mag_app':norm(loc=25,scale=1).rvs,
'output_ab_zeropoint':output_ab_zeropoint,
'R_sersic':truncnorm(-1,np.inf,loc=0.25,scale=0.25).rvs,
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
z_lens_min=0,z_lens_mean=0.5,z_lens_std=0.25,
z_source_min=0,z_source_mean=1,z_source_std=0.5)
}
}
}