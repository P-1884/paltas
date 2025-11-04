# Includes a PEMD deflector with external shear, and Sersic sources. Includes 
# a simple observational effect model that roughly matches HST effects for
# Wide Field Camera 3 (WFC3) IR channel with the F160W filter.

import numpy as np
from scipy.stats import norm, truncnorm, uniform
from paltas.MainDeflector.simple_deflectors import PEMDShear
from paltas.Sources.sersic import SingleSersicSource
from paltas.Substructure.subhalos_dg19 import SubhalosDG19
import paltas.Sampling.distributions as dist

# Define the numerics kwargs.
kwargs_numerics = {'supersampling_factor':1}

# This is always the number of pixels for the CCD. If drizzle is used, the
# final image will be larger.
numpix = 256

# Define some general image kwargs for the dataset
mask_radius = 0
mag_cut = 3

# Define arguments that will be used multiple times
output_ab_zeropoint = 25.127
centre_loc = np.nan
config_dict = {
	'main_deflector':{
		'class': PEMDShear,
		'parameters':{
			'M200': 1e14,
			'z_lens': 0.5,
			'gamma': truncnorm(-20,np.inf,loc=2.0,scale=0.01).rvs,
			'theta_E': truncnorm(-1.1/0.15,np.inf,loc=1.1,scale=0.01).rvs,
			'e1': norm(loc=0.0,scale=0.1).rvs,
			'e2': norm(loc=0.0,scale=0.1).rvs,
			'center_x': norm(loc=centre_loc,scale=0.01).rvs,
			'center_y': norm(loc=0.0,scale=0.01).rvs,
			'gamma1': norm(loc=0.0,scale=0.01).rvs,
			'gamma2': norm(loc=0.0,scale=0.01).rvs,
			'ra_0':0.0, 'dec_0':0.0
		}
	},
	'source':{
		'class': SingleSersicSource,
		'parameters':{
			'z_source':truncnorm(-5,np.inf,loc=2.,scale=0.01).rvs,
			'magnitude':uniform(loc=-32,scale=0.01).rvs,
			'output_ab_zeropoint':output_ab_zeropoint,
			'R_sersic':truncnorm(-2,2,loc=0.35,scale=0.01).rvs,
			'n_sersic':truncnorm(3.,np.inf,loc=3.,scale=0.01).rvs,
			'e1':norm(loc=0.0,scale=0.01).rvs,
			'e2':norm(loc=0.0,scale=0.01).rvs,
			'center_x':norm(loc=0.0,scale=0.01).rvs,
			'center_y':norm(loc=0.0,scale=0.01).rvs}
	},
    	'lens_light':{
		'class': SingleSersicSource,
		'parameters':{
			'z_source':None,
			'magnitude':truncnorm(-1.5,2.0,loc=-26,scale=0.01).rvs,
			'output_ab_zeropoint':output_ab_zeropoint,
			'R_sersic':truncnorm(-1.333,np.inf,loc=0.8,scale=0.01).rvs,
			'n_sersic':truncnorm(-2.,np.inf,loc=3,scale=0.01).rvs,
			'e1':None,
			'e2':None,
			'center_x':None,
			'center_y':None}
	},
	'cross_object':{
		'parameters':{
			('main_deflector:center_x,lens_light:center_x'):dist.Duplicate(
			dist=uniform(loc=0.0,scale=0.01).rvs),
			('main_deflector:center_y,lens_light:center_y'):dist.Duplicate(
			dist=uniform(loc=0.0,scale=0.01).rvs),
			('main_deflector:z_lens,lens_light:z_source'):dist.Duplicate(
			dist=truncnorm(-2,np.inf,loc=0.5,scale=0.01).rvs),
			('main_deflector:e1,lens_light:e1'):dist.Duplicate(
			dist=norm(loc=0.0,scale=0.01).rvs),
			('main_deflector:e2,lens_light:e2'):dist.Duplicate(
			dist=norm(loc=0.0,scale=0.01).rvs)}
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
			'pixel_scale':0.020,'ccd_gain':1.58,'read_noise':3.0,
			'magnitude_zero_point':output_ab_zeropoint,
			'exposure_time':1380,'sky_brightness':21.83,
			'num_exposures':4,'background_noise':None
		}
	}
}
