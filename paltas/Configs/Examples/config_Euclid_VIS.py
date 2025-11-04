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
			'z_lens': UPDATE,
			'gamma': UPDATE,
			'theta_E': UPDATE,
			'e1': UPDATE,
			'e2': UPDATE,
			'center_x': UPDATE,
			'center_y': UPDATE,
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
			'psf_type':'GAUSSIAN',
			'fwhm': 0.18
			
		}
	},
#From Lenspop: https://github.com/tcollett/LensPop/blob/master/Surveys.py
# self.pixelsize=0.1
# self.zeropoints=[25.5]
# self.zeroexposuretime=1.
# self.skybrightnesses=[22.2]
# self.exposuretimes=[1610]
# self.gains=[1]
# self.seeing=[.2]
# self.nexposures=4
# self.degrees_of_survey=20000
# self.readnoise=(4.5)

#From Lenstronomy (vs LensPop in brackets): 
# read_noise: 4.2 #electrons (vs 4.5)
# pixel_scale: 0.101 #arcsec/pixel (vs 0.1)
# ccd_gain: 3.1 # electrons/ADU (vs 1)
# exposure_time: 565 (vs 1610) #Also supported by https://arxiv.org/pdf/2108.01201.pdf which gives t_exp~570s.
# sky_brightness:22.35 (vs 22.2)
# magnitude_zero_point: 24 (vs 25.5) #=> Don't really trust the lenstronomy's cited derivation for this, though very useful for other properties. See https://www.aanda.org/articles/aa/pdf/2019/07/aa35187-19.pdf below Figure 6. This paper (https://arxiv.org/pdf/2202.09475.pdf) suggests ZP=25.58. For the time being, will therefore use ZP=25.5 (i.e. the LensPop value, so it is citeable). This may also change depending on what simulations I put behind it. 
# num_exposures: 4 (vs 4)
# seeing: 0.16 (vs 0.2) Will use 0.18 (an average) taken from here: https://www.euclid-ec.org/public/mission/vis/

#Currently using the lenstronomy values:
	'detector':{
		'parameters':{
			'pixel_scale':0.1,'ccd_gain':3.1,'read_noise':4.2,
			'magnitude_zero_point':25.5,
			'exposure_time':565,'sky_brightness':22.35,
			'num_exposures':4,'background_noise':None
		}
	},
	'lens_subtraction':True,
}