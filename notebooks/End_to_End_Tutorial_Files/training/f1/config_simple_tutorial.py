# Includes a PEMD deflector with external shear, and Sersic sources. Includes 
# a simple observational effect model that roughly matches HST effects for
# Wide Field Camera 3 (WFC3) IR channel with the F160W filter.

import numpy as np
from scipy.stats import norm, truncnorm, uniform
paltas_directory = '/Users/hollowayp/paltas/'
import os
os.chdir(paltas_directory)
#import sys
#sys.path.append(paltas_directory)
from paltas.MainDeflector.simple_deflectors import PEMDShear
from paltas.Sources.sersic import SingleSersicSource
from paltas.Substructure.subhalos_dg19 import SubhalosDG19

# Define the numerics kwargs.
kwargs_numerics = {'supersampling_factor':1}

# This is always the number of pixels for the CCD. If drizzle is used, the
# final image will be larger.
numpix = 60

# Define some general image kwargs for the dataset
mask_radius = 0#0.5
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
	'detector':{
		'parameters':{
			'pixel_scale':0.18,'ccd_gain':4.5,'read_noise':10/4.5,
			'magnitude_zero_point':output_ab_zeropoint,
			'exposure_time':6000,'sky_brightness':20.1,
			'num_exposures':100,'background_noise':None
		}
	}
}
###^^ Currently modelling in i-band (i.e. using exposure time, sky_brightness specific to i-band, according to Collett 2015 values).
###^^ Haven't yet included any background noise.