# Includes a PEMD deflector with external shear, and Sersic sources. 
# Designed to be similar to LSST-like images (though background noise is not yet implemented.)

import numpy as np
from scipy.stats import norm, truncnorm, uniform
paltas_directory = '/Users/hollowayp/paltas/'
import sys
sys.path.append(paltas_directory)

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
'z_lens':0.292,
'gamma': truncnorm(-20,np.inf,loc=2.0,scale=0.1).rvs,
'theta_E':1.65,
'e1': norm(loc=0.0,scale=0.1).rvs,
'e2': norm(loc=0.0,scale=0.1).rvs,
'center_x':0.0,
'center_y':0.0,
'gamma1': norm(loc=0.0,scale=0.05).rvs,
'gamma2': norm(loc=0.0,scale=0.05).rvs,
'ra_0':0.0, 'dec_0':0.0
}
},
'source':{
'class': SingleSersicSource,
'parameters':{
'z_source':1.329,
'mag_app':26.03,
'output_ab_zeropoint':output_ab_zeropoint,
'R_sersic':0.16,
'n_sersic':truncnorm(-6.,np.inf,loc=3.,scale=0.5).rvs,
'e1':-0.11629218949940744,
'e2':-0.5873184743057911,
'center_x':-0.26,
'center_y':0.81,
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
}
}


