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
add_RSP_background=False
RSP_cutout_folder='/mnt/zfsusers/hollowayp/paltas/RSP_Coadd_Files_100000/'
RSP_ZP = 27 #Zeropoint for the coadds
output_ab_zeropoint = 27.85 #From https://smtn-002.lsst.io/. Refers to ZP which gives 1e/s. Is fainter in ADU (when gain=0.7)

#Asserting this as otherwise need to update read_noise and sky-brightness (and maybe gain too):
#assert add_RSP_background==True

config_dict = {
'main_deflector':{
'class': PEMDShear,
'parameters':{
'M200': 1e13,
'z_lens':0.5,
'gamma':2,
'theta_E':1,
'e1':0,
'e2':0,
'center_x':1,
'center_y':2,
'gamma1':0,
'gamma2':0,
'ra_0':0.0, 'dec_0':0.0
}
},
'lens_light':{
'class': SingleSersicSource,
'parameters':{
'z_source':1,
'mag_app':17,
'output_ab_zeropoint':output_ab_zeropoint,
'R_sersic':1,
'n_sersic':4.0,
'e1':0,
'e2':0,
'center_x':1,
'center_y':2,
}
},
'source':{
'class': SingleSersicSource,
'parameters':{
'z_source':1,
'mag_app':24,
'output_ab_zeropoint':output_ab_zeropoint,
'R_sersic':0.4,
'n_sersic':1.0,
'e1':0,
'e2':0,
'd_center_x':0.5,
'd_center_y':0.5,
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
'pixel_scale':0.2,'ccd_gain':0.7,'read_noise':0, #Noise is added from RSP. Gain from here https://community.lsst.org/t/dp0-zeropoints-adding-poisson-noise/8230/7, correct for DP0
'magnitude_zero_point':output_ab_zeropoint,
'exposure_time':30,'sky_brightness':100, #Sky needs to be faint, as added in from RSP. Exposure time must = 30 for RSP.
'num_exposures':100,'background_noise':None
}
},
'lens_subtraction':False,
'cross_object':{
'parameters':{
('main_deflector:center_x,main_deflector:center_y,lens_light:center_x,lens_light:center_y'):
dist.DuplicateXY(
x_dist=norm(loc=1.0,scale=0.001).rvs, 
y_dist=norm(loc=2.0,scale=0.001).rvs),
'main_deflector:z_lens,source:z_source':dist.RedshiftsTruncNorm( 
z_lens_min=0,z_lens_mean=0.42,z_lens_std=0.01,
z_source_min=0,z_source_mean=1.8,z_source_std=0.01)
}
}
}