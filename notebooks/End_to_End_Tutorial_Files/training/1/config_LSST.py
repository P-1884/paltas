# Includes a PEMD deflector with external shear, and Sersic sources. 
# Designed to be similar to LSST-like images (though background noise is not yet implemented.)

import numpy as np
from scipy.stats import norm, truncnorm, uniform
#import sys
#sys.path.append(paltas_directory)
from paltas.MainDeflector.simple_deflectors import PEMDShear
from paltas.Sources.sersic import SingleSersicSource
from paltas.Substructure.subhalos_dg19 import SubhalosDG19

# Define the numerics kwargs.
kwargs_numerics = {'supersampling_factor':1}

# This is always the number of pixels for the CCD. If drizzle is used, the
# final image will be larger.
numpix = 80

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
			'mag_app':uniform(loc=25,scale=5).rvs,
			'output_ab_zeropoint':output_ab_zeropoint,
			'R_sersic':truncnorm(-2,2,loc=0.35,scale=0.05).rvs,
			'n_sersic':truncnorm(-6.,np.inf,loc=3.,scale=0.5).rvs,
			'e1':norm(loc=0.0,scale=0.1).rvs,
			'e2':norm(loc=0.0,scale=0.1).rvs,
			'center_x':norm(loc=0.0,scale=0.16).rvs,
			'center_y':norm(loc=0.0,scale=0.16).rvs}
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
	}
}