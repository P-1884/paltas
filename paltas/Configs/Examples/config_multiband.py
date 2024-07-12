# Includes a PEMD deflector with external shear, and Sersic sources. Includes 
# a simple observational effect model that roughly matches HST effects for
# Wide Field Camera 3 (WFC3) IR channel with the F160W filter.

import numpy as np
from scipy.stats import norm, truncnorm, uniform
from paltas.MainDeflector.simple_deflectors import PEMDShear
from paltas.Sources.sersic import SingleSersicSource
import paltas.Sampling.distributions as dist

# Define the numerics kwargs.
kwargs_numerics = {'supersampling_factor':1}

# This is always the number of pixels for the CCD. If drizzle is used, the
# final image will be larger.
numpix = 128

# Define some general image kwargs for the dataset
mask_radius = 0.5
mag_cut = 2.0

# Define arguments that will be used multiple times
output_ab_zeropoint = 25.127

multiband = True
filter_list = ['g','r']
filter_dependent_properties = ['source_parameters_R_sersic','source_parameters_magnitude','lens_light_parameters_magnitude']

config_dict = {
	'main_deflector':{
		'class': PEMDShear,
		'parameters':{
			'M200': 1e13,
			'z_lens': 0.5,
			'gamma': truncnorm(-20,np.inf,loc=2.0,scale=0.1).rvs,
			'theta_E': truncnorm(-1.1/0.15,np.inf,loc=1.1,scale=0.15).rvs,
			'e1': norm(loc=0.0,scale=0.1).rvs,
			'e2': norm(loc=0.0,scale=0.1).rvs,
			'center_x': norm(loc=0.0,scale=0.16).rvs,
			'center_y': norm(loc=0.0,scale=0.16).rvs,
			'gamma1': norm(loc=0.0,scale=0.05).rvs,
			'gamma2': norm(loc=0.0,scale=0.05).rvs,
			'ra_0':0.0, 'dec_0':0.0
		}
	},
	'source':{
		'class': SingleSersicSource,
		'parameters':{
			'z_source':truncnorm(-5,np.inf,loc=2.,scale=0.4).rvs,
			'magnitude':{'g':uniform(loc=20,scale=5).rvs,'r':uniform(loc=20,scale=5).rvs},
			'output_ab_zeropoint':output_ab_zeropoint,
			'R_sersic':{'g':truncnorm(-2,2,loc=0.35,scale=0.05).rvs,'r':truncnorm(-2,2,loc=0.35,scale=0.05).rvs},
			'n_sersic':truncnorm(-6.,np.inf,loc=3.,scale=0.5).rvs,
			'e1':norm(loc=0.0,scale=0.1).rvs,
			'e2':norm(loc=0.0,scale=0.1).rvs,
			'center_x':norm(loc=0.0,scale=0.16).rvs,
			'center_y':norm(loc=0.0,scale=0.16).rvs}
	},
	'lens_light':{
		'class': SingleSersicSource,
		'parameters':{
			'z_source':0.5,
			'magnitude':{'g':uniform(loc=19,scale=2).rvs,'r':uniform(loc=19,scale=2).rvs},
			'output_ab_zeropoint':output_ab_zeropoint,
			'R_sersic':truncnorm(-1.333,np.inf,loc=0.8,scale=0.15).rvs,
			'n_sersic':truncnorm(-2.,np.inf,loc=3,scale=0.5).rvs,
			'e1,e2':dist.EllipticitiesTranslation(
				q_dist=truncnorm(-np.inf,1.,loc=0.85,scale=0.15).rvs,
				phi_dist=uniform(loc=-np.pi/2,scale=np.pi).rvs),
			'center_x':0.0,
			'center_y':0.0}
    },
	'cosmology':{
		'parameters':{
			'cosmology_name': 'planck18'
		}
	},
	'psf':{
		'parameters':{
			'psf_type':'GAUSSIAN',
			'fwhm': 0.03
		}
	},
	'detector':{
		'parameters':{
			'pixel_scale':0.040,'ccd_gain':1.58,'read_noise':3.0,
			'magnitude_zero_point':output_ab_zeropoint,
			'exposure_time':1380,'sky_brightness':21.83,
			'num_exposures':4,'background_noise':None
		}
	}
}
