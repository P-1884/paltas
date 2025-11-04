# Includes a PEMD deflector with external shear, and Sersic sources. 
# Designed to be similar to LSST-like images (though background noise is not yet implemented.)

import numpy as np
from scipy.stats import norm, truncnorm, uniform
paltas_directory = '/Users/hollowayp/paltas/'
import os
os.chdir(paltas_directory)
from paltas.MainDeflector.simple_deflectors import PEMDShear
from paltas.Sources.sersic import SingleSersicSource
from paltas.Substructure.subhalos_dg19 import SubhalosDG19

# Define the numerics kwargs.
kwargs_numerics = {'supersampling_factor':1}

# This is always the number of pixels for the CCD. If drizzle is used, the
# final image will be larger.
numpix = 60

# Define some general image kwargs for the dataset
mask_radius = 0
mag_cut = 3.0

# Define arguments that will be used multiple times
output_ab_zeropoint = 25

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
			'magnitude':uniform(loc=-26,scale=5).rvs, #WHY DO THE MAGNITUDES NEED TO BE NEGATIVE, and why is -20 fainter than -26?
			'output_ab_zeropoint':output_ab_zeropoint,
			'R_sersic':truncnorm(-2,2,loc=0.35,scale=0.05).rvs,
			'n_sersic':truncnorm(-6.,np.inf,loc=3.,scale=0.5).rvs,
			'e1':norm(loc=0.0,scale=0.1).rvs,
			'e2':norm(loc=0.0,scale=0.1).rvs,
			'center_x':norm(loc=0.0,scale=0.16).rvs,
			'center_y':norm(loc=0.0,scale=0.16).rvs}
	},
    	'lens_light':{
		'class': SingleSersicSource,
		'parameters':{
			'z_source':None,
			'magnitude':truncnorm(-1.5,2.0,loc=-22.5,scale=2).rvs,
			'output_ab_zeropoint':output_ab_zeropoint,
			'R_sersic':truncnorm(-1.333,np.inf,loc=0.8,scale=0.15).rvs,
			'n_sersic':truncnorm(-2.,np.inf,loc=3,scale=0.5).rvs,
			'e1':None,
			'e2':None,
			'center_x':None,
			'center_y':None}
	},
	'cross_object':{
		'parameters':{
			('main_deflector:center_x,lens_light:center_x'):dist.Duplicate(
			dist=uniform(loc=0.0,scale=0.16).rvs),
			('main_deflector:center_y,lens_light:center_y'):dist.Duplicate(
			dist=uniform(loc=0.0,scale=0.16).rvs),
			('main_deflector:z_lens,lens_light:z_source'):dist.Duplicate(
			dist=truncnorm(-2,np.inf,loc=0.5,scale=0.25).rvs),
			('main_deflector:e1,lens_light:e1'):dist.Duplicate(
			dist=norm(loc=0.0,scale=0.1).rvs),
			('main_deflector:e2,lens_light:e2'):dist.Duplicate(
			dist=norm(loc=0.0,scale=0.1).rvs)}
	'cosmology':{
		'parameters':{
			'cosmology_name': 'planck18'
		}
	},
	'psf':{
		'parameters':{
			'psf_type':'GAUSSIAN',
			'fwhm': 0.67 #Using value from https://www.lsst.org/scientists/keynumbers
		}
	},
	'detector':{
		'parameters':{
			'pixel_scale':0.18,'ccd_gain':4.5,'read_noise':10/4.5,
			'magnitude_zero_point':output_ab_zeropoint,
			'exposure_time':6000,'sky_brightness':20.1,
			'num_exposures':100,'background_noise':None
		}
	}
}
###^^ Haven't yet included any background noise.