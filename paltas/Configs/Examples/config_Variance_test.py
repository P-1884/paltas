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
numpix = 101
mask_radius = 0
mag_cut = 0.0
catalog = False
save_noise=True
add_RSP_background=True
RSP_cutout_folder='/mnt/zfsusers/hollowayp/paltas/RSP_Coadd_Files_100/'
RSP_ZP = 27 #Zeropoint for the coadds
# Define arguments that will be used multiple times
output_ab_zeropoint = 27.85 #From https://smtn-002.lsst.io/. Refers to ZP which gives 1e/s. Is fainter in ADU (when gain=0.7)

config_dict = {
'main_deflector':{
'class': PEMDShear,
'parameters':{
'M200': 1e13,
'z_lens':0.5,
'gamma':2.0,
'theta_E':1.0,
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
'z_source':0.5,
'mag_app':20,
'output_ab_zeropoint':output_ab_zeropoint,
'R_sersic':1.0,
'n_sersic':4,
'e1':0.0,
'e2':0.0,
'center_x':0.0,
'center_y':0.0,
}
},
'source':{
'class': SingleSersicSource,
'parameters':{
'z_source':1.0,
'mag_app':50,
'output_ab_zeropoint':output_ab_zeropoint,
'R_sersic':10.0,
'n_sersic':1.0,
'e1':0.0,
'e2':0.0,
'center_x':0.0,
'center_y':0.0,
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
'pixel_scale':0.2,'ccd_gain':0.7,'read_noise':0.0, #Gain from here https://community.lsst.org/t/dp0-zeropoints-adding-poisson-noise/8230/7, correct for DP0
'magnitude_zero_point':output_ab_zeropoint,
'exposure_time':30,'sky_brightness':50,#20.48, #Image flux is per second. It doesn't scale with exposure time.
'num_exposures':None,'background_noise':None
}
},
'lens_subtraction':False,
'cross_object':{
'parameters':{
('main_deflector:center_x,main_deflector:center_y,lens_light:center_x,lens_light:center_y'):
dist.DuplicateXY(
x_dist=norm(loc=0.0,scale=0.01).rvs, 
y_dist=norm(loc=0.0,scale=0.01).rvs),
'main_deflector:z_lens,source:z_source':dist.RedshiftsTruncNorm( 
z_lens_min=0,z_lens_mean=0.5,z_lens_std=0.01,
z_source_min=0,z_source_mean=1.0,z_source_std=0.01)
}
}
}