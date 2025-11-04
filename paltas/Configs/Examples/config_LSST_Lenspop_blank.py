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
mask_radius = 0
mag_cut = 0.0
catalog = False
save_noise=False
add_RSP_background = 'TBD'
RSP_cutout_folder= 'TBD' #'/mnt/zfsusers/hollowayp/paltas/RSP_Coadd_Files_100000/'
RSP_ZP = 'TBD' #27 #Zeropoint for the coadds
output_ab_zeropoint = 'TBD' #27.85 #From https://smtn-002.lsst.io/. Refers to ZP which gives 1e/s. Is fainter in ADU (when gain=0.7)

config_dict = {
'main_deflector':{
'class': PEMDShear,
'parameters':{
'M200': 1e13,
'z_lens':'TBD',
'gamma':'TBD',
'theta_E':'TBD',
'e1':'TBD',
'e2':'TBD',
'center_x':'TBD',
'center_y':'TBD',
'gamma1':'TBD',
'gamma2':'TBD',
'ra_0':0.0, 'dec_0':0.0
}
},
'lens_light':{
'class': SingleSersicSource,
'parameters':{
'z_source':'TBD',
'mag_app':'TBD',
'output_ab_zeropoint':output_ab_zeropoint,
'R_sersic':'TBD',
'n_sersic':'TBD',
'e1':'TBD',
'e2':'TBD',
'center_x':'TBD',
'center_y':'TBD',
}
},
'source':{
'class': SingleSersicSource,
'parameters':{
'z_source':'TBD',
'mag_app':'TBD',
'output_ab_zeropoint':output_ab_zeropoint,
'R_sersic':'TBD',
'n_sersic':'TBD',
'e1':'TBD',
'e2':'TBD',
'center_x':'TBD',
'center_y':'TBD',
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
'fwhm': 'TBD'

}
},
'detector':{
'parameters':{
'pixel_scale':0.2,'ccd_gain':'TBD','read_noise':'TBD', #Noise is added from RSP. Gain from here https://community.lsst.org/t/dp0-zeropoints-adding-poisson-noise/8230/7, correct for DP0
'magnitude_zero_point':output_ab_zeropoint,
'exposure_time':'TBD','sky_brightness':'TBD', #Sky needs to be faint, as added in from RSP. Exposure time must = 30 for RSP.
'num_exposures':'TBD','background_noise':None
}
},
'lens_subtraction':'TBD',
}