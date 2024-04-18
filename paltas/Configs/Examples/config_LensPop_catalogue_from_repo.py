# Includes a PEMD deflector with external shear, and Sersic sources. 
# Designed to be similar to LSST-like images (though background noise is not yet implemented.)


#### EDITS MADE ON 25TH JAN. WOULD NEED TO RETRIEVE VERSION FROM 24TH JAN (OR EARLIER).
import numpy as np
from scipy.stats import norm, truncnorm, uniform
paltas_directory = '/mnt/zfsusers/hollowayp/paltas'#'/Users/hollowayp/paltas/'
import sys
sys.path.append(paltas_directory)
import paltas.Sampling.distributions as dist
from paltas.MainDeflector.simple_deflectors import PEMDShear
from paltas.Sources.sersic import SingleSersicSource
from paltas.PointSource.single_point_source import SinglePointSource
from lenstronomy.Util import kernel_util
from lenstronomy.Util.param_util import phi_q2_ellipticity
import pandas as pd
import os
import paltas

# Define the numerics kwargs.
kwargs_numerics = {'supersampling_factor':1}

# This is always the number of pixels for the CCD. If drizzle is used, the
# final image will be larger.
numpix = 60

# Define arguments that will be used multiple times
catalog = True
add_RSP_background=True
RSP_cutout_folder='/mnt/zfsusers/hollowayp/paltas/RSP_Coadd_Files_100000/'
RSP_ZP = 27 #Zeropoint for the coadds
output_ab_zeropoint = 27.85 #From https://smtn-002.lsst.io/. Refers to ZP which gives 1e/s. Is fainter in ADU (when gain=0.7)
save_noise=False
Catalogue_directory = '/mnt/users/hollowayp/LensPop_Versions/LensPop_Catalogue_Orig_Config.csv'
config_dict = {
	'main_deflector':{
		'class': PEMDShear,
		'file': Catalogue_directory,
		'parameters':{
			'z_lens': 'zl',
			'gamma': 2,
			'theta_E': 'b',
			'e1': 'e1_lens', # added to catalog
			'e2': 'e2_lens', # added to catalog
			'center_x': 0,  # added to catalog
			'center_y': 0,  # added to catalog
			'gamma1': 0, # added to catalog
			'gamma2': 0, # added to catalog
			'ra_0':0.0, 'dec_0':0.0,
		}
	},
	'lens_light':{
		'class': SingleSersicSource,
		'file': Catalogue_directory,
		'parameters':{
			'z_source':'zl',
			'mag_app':'ml', # LENS APPARENT MAG
			'output_ab_zeropoint':output_ab_zeropoint,
			'R_sersic': 'rl',
			'n_sersic': 4,
			'e1': 'e1_lens', # added to catalog
			'e2': 'e2_lens', # added to catalog
			'center_x':0,
			'center_y':0
			}
	},
	'source':{
		'class': SingleSersicSource,
		'file':Catalogue_directory,
		'parameters':{
			'z_source': 'zs',
			'mag_app': 'ms', # SOURCE APPARENT MAG
			'output_ab_zeropoint':output_ab_zeropoint,
			'R_sersic': 'rs',
			'n_sersic': 1,
			'e1':'e1_source', # added to catalog
			'e2':'e2_source', # added to catalog
			'center_x': 'xs',
			'center_y': 'ys'
		}
	},
	'cosmology':{
		'file': None,
		'parameters':{
			'cosmology_name': 'planck18'
		}
	},
	'psf':{
'file': None,
'parameters':{
'psf_type':'GAUSSIAN',
'fwhm':0.71# None
}
},
# Currently using the lenstronomy values:
'detector':{
'file':None,
'parameters':{
'pixel_scale':0.2,'ccd_gain':0.7,'read_noise':0, #Noise is added from RSP. Gain from here https://community.lsst.org/t/dp0-zeropoints-adding-poisson-noise/8230/7, correct for DP0
'magnitude_zero_point':output_ab_zeropoint,
'exposure_time':30,'sky_brightness':100, #Sky needs to be faint, as added in from RSP. Exposure time must = 30 for RSP.
'num_exposures':None,'background_noise':None

}
},
'lens_subtraction':True,
}
assert add_RSP_background==True #Otherwise need to update read_noise and sky-brightness (and maybe gain too).
print(config_dict)