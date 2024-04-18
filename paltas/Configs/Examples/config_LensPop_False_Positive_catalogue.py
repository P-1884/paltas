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
print('NOT ADDING RSP IMAGES HERE AT THE MOMENT')
# Define arguments that will be used multiple times
catalog = True
add_RSP_background=False
RSP_cutout_folder='/mnt/zfsusers/hollowayp/paltas/RSP_Coadd_Files_100000/'
RSP_ZP = 27 #Zeropoint for the coadds
output_ab_zeropoint = 27.85 #From https://smtn-002.lsst.io/. Refers to ZP which gives 1e/s. Is fainter in ADU (when gain=0.7)
save_noise=False
Catalogue_directory = '/mnt/zfsusers/hollowayp/paltas/datasets/LensPop_databases/LensPop_LSST_Paltas_False_Positive_Catalogue_2.csv'

config_dict = {
	'main_deflector':{
		'class': PEMDShear,
		'file': Catalogue_directory,
		'parameters':{
			'z_lens': 'zL',
			'gamma': 'defl_gamma',
			'theta_E': 'tE',
			'e1': 'defl_e1_mass', # added to catalog
			'e2': 'defl_e2_light', # added to catalog
			'center_x': 'defl_mass_x',  # added to catalog
			'center_y': 'defl_mass_y',  # added to catalog
			'gamma1': 'defl_gamma1', # added to catalog
			'gamma2': 'defl_gamma2', # added to catalog
			'ra_0':0.0, 'dec_0':0.0,
		}
	},
	'lens_light':{
		'class': SingleSersicSource,
		'file': Catalogue_directory,
		'parameters':{
			'z_source':'zL',
			'mag_app':'i_lens', # LENS APPARENT MAG
			'output_ab_zeropoint':output_ab_zeropoint,
			'R_sersic': 'Re_lens',
			'n_sersic': 'defl_Ns',
			'e1': 'defl_e1_light', # added to catalog
			'e2': 'defl_e2_light', # added to catalog
			'center_x':'defl_light_x',
			'center_y':'defl_light_y'
			}
	},
	'source':{
		'class': SingleSersicSource,
		'file':Catalogue_directory,
		'parameters':{
			'z_source': 'zS',
			'mag_app': 'i_source', # SOURCE APPARENT MAG
			'output_ab_zeropoint':output_ab_zeropoint,
			'R_sersic': 'Re_source',
			'n_sersic': 'source_Ns',
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
'detector':{
'file':None,
'parameters':{
'pixel_scale':0.2,'ccd_gain':2.3,'read_noise':10,
'magnitude_zero_point':output_ab_zeropoint,
'exposure_time':30,'sky_brightness':20.48,
'num_exposures':230,'background_noise':None
}
},
'lens_subtraction':True,
}
print(config_dict)