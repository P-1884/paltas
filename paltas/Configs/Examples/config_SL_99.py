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
'z_lens':0.182,
'gamma':2.0,
'theta_E':1.4,
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
'z_source':0.182,
'mag_app':16.35,
'output_ab_zeropoint':output_ab_zeropoint,
'R_sersic':1.92,
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
'z_source':1.615,
'mag_app':23.37,
'output_ab_zeropoint':output_ab_zeropoint,
'R_sersic':0.4,
'n_sersic':1.0,
'e1':0.3299154941553713,
'e2':0.10086528885189236,
'center_x':-0.26,
'center_y':-0.12,
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
'exposure_time':15,'sky_brightness':20.48,
'num_exposures':460,'background_noise':None
}
},
'lens_subtraction':True,
}
