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

# Define some general image kwargs for the dataset
mask_radius = 0
mag_cut = 3.0

# Define arguments that will be used multiple times
output_ab_zeropoint = 27.79

config_dict = {
	'main_deflector':{
		'class': PEMDShear,
		'parameters':{
			'M200': 1e13,
			'z_lens': UPDATE,
			'gamma': truncnorm(-20,np.inf,loc=2.0,scale=0.1).rvs,
			'theta_E': UPDATE,
			'e1': UPDATE,
			'e2': UPDATE,
			'center_x': norm(loc=0.0,scale=0.16).rvs,
			'center_y': norm(loc=0.0,scale=0.16).rvs,
			'gamma1': UPDATE,
			'gamma2': UPDATE,
			'ra_0':0.0, 'dec_0':0.0
		}
	},
	'lens_light':{
		'class': SingleSersicSource,
		'parameters':{
			'z_source':UPDATE,
			'mag_app':UPDATE,
			'output_ab_zeropoint':output_ab_zeropoint,
			'R_sersic':UPDATE,
			'n_sersic':UPDATE,
			'e1':UPDATE,
			'e2':UPDATE,
			'center_x':UPDATE,
			'center_y':UPDATE
			}
	},
	'source':{
		'class': SingleSersicSource,
		'parameters':{
			'z_source':UPDATE,
			'mag_app':UPDATE,
			'output_ab_zeropoint':output_ab_zeropoint,
			'R_sersic':UPDATE,
			'n_sersic':UPDATE,
			'e1':UPDATE,
			'e2':UPDATE,
			'center_x':UPDATE,
			'center_y':UPDATE
		}
	},
	'cosmology':{
		'parameters':{
			'cosmology_name': 'planck18'
		}
	},
	'psf':{
		'parameters':{
#Could also get value for seeing from https://www.lsst.org/scientists/keynumbers, of 0.67"
			'psf_type':'GAUSSIAN',
			'fwhm': 0.71
			
		}
	},
#From Lenspop: https://github.com/tcollett/LensPop/blob/master/Surveys.py
#self.pixelsize=0.18
#self.side=111
#self.bands=['g','r','i']
#self.zeropoints=[30,30,30]
#self.zeroexposuretime=25
#self.skybrightnesses=[21.7,20.7,20.1]
#self.exposuretimes=[3000,6000,6000]
#self.gains=[4.5,4.5,4.5]
#self.seeing=[.4,.4,.4]
#self.nexposures=100
#self.degrees_of_survey=18000
#self.readnoise=(10/4.5)

#From Lenstronomy: https://github.com/lenstronomy/lenstronomy/blob/main/lenstronomy/SimulationAPI/ObservationConfig/LSST.py:
#i_band_obs = {
#    "exposure_time": 15.0,
#    "sky_brightness": 20.48,
#    "magnitude_zero_point": 27.79,
#    "num_exposures": 460,
#    "seeing": 0.71,
#    "psf_type": "GAUSSIAN"}
#self.camera = {
#    "read_noise": 10,  # will be <10
#    "pixel_scale": 0.2,
#    "ccd_gain": 2.3}

#Currently using the lenstronomy values:
	'detector':{
		'parameters':{
			'pixel_scale':0.2,'ccd_gain':2.3,'read_noise':10,
			'magnitude_zero_point':output_ab_zeropoint,
			'exposure_time':15,'sky_brightness':20.48,
			'num_exposures':460,'background_noise':None
		}
	},
	'lens_subtraction':True,
}