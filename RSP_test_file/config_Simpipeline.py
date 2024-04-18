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
mag_cut = 0.0

# Define arguments that will be used multiple times
output_ab_zeropoint = 27.79

config_dict = {
'main_deflector':{
'class': PEMDShear,
'parameters':{
'M200': 1e13,
'z_lens':truncnorm(1.7499441321204543,np.inf,loc=0.5133573511241993,scale=0.2933564230431462).rvs,
'gamma':truncnorm(-3.7878787878787876,np.inf,loc=2.0,scale=0.264).rvs,
'theta_E':truncnorm(3.5108421707933872,np.inf,loc=1.403716841776175,scale=0.3998233966350473).rvs,
'e1':norm(loc=-0.0051898045247532,scale=0.1297500463949897).rvs,
'e2':norm(loc=0.0621089767937572,scale=0.1104575763829624).rvs,
'center_x':norm(loc=0.00398962859148,scale=0.1139341558531491).rvs,
'center_y':norm(loc=-0.0022187928677997,scale=0.1205197272539364).rvs,
'gamma1':norm(loc=-0.0010897291623189,scale=0.0793725368739587).rvs,
'gamma2':norm(loc=-0.0011964962466028,scale=0.0824584817881597).rvs,
'ra_0':0.0, 'dec_0':0.0
}
},
'lens_light':{
'class': SingleSersicSource,
'parameters':{
'z_source':truncnorm(1.7499441321204543,np.inf,loc=0.5133573511241993,scale=0.2933564230431462).rvs,
'mag_app':norm(loc=20.815668330226963,scale=1.8939116478460856).rvs,
'output_ab_zeropoint':output_ab_zeropoint,
'R_sersic':truncnorm(0.834287670140835,np.inf,loc=0.4409457178260933,scale=0.5285295871047188).rvs,
'n_sersic':4.0,
'e1':norm(loc=-0.0068971195502699,scale=0.1077556577984413).rvs,
'e2':norm(loc=0.0656396501783146,scale=0.077287149879285).rvs,
'center_x':norm(loc=0.00398962859148,scale=0.1139341558531491).rvs,
'center_y':norm(loc=-0.0022187928677997,scale=0.1205197272539364).rvs,
}
},
'source':{
'class': SingleSersicSource,
'parameters':{
'z_source':truncnorm(2.0719370511253583,np.inf,loc=2.6812382040555054,scale=1.2940731971558737).rvs,
'mag_app':norm(loc=24.64559091885439,scale=1.1136574857839725).rvs,
'output_ab_zeropoint':output_ab_zeropoint,
'R_sersic':truncnorm(1.5208784742357893,np.inf,loc=0.5176383281974857,scale=0.3403548258236665).rvs,
'n_sersic':1.0,
'e1':norm(loc=-0.0029803765818974,scale=0.2497935151046365).rvs,
'e2':norm(loc=-0.0089688465821498,scale=0.2519964152069817).rvs,
'center_x':norm(loc=0.0159162806858803,scale=0.6337352565811993).rvs,
'center_y':norm(loc=0.0035004374446817,scale=0.6058876321648844).rvs,
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
'exposure_time':30,'sky_brightness':20.48,
'num_exposures':230,'background_noise':None
}
},
'lens_subtraction':True,
'add_RSP_background':True,
'RSP_cutout_folder':'/mnt/zfsusers/hollowayp/sim-pipeline/Coadd_files',
'cross_object':{
'parameters':{
('main_deflector:center_x,main_deflector:center_y,lens_light:center_x,lens_light:center_y'):
dist.DuplicateXY(
x_dist=norm(loc=0.00398962859148,scale=0.1139341558531491).rvs, 
y_dist=norm(loc=-0.0022187928677997,scale=0.1205197272539364).rvs),
'main_deflector:z_lens,source:z_source':dist.RedshiftsTruncNorm( 
z_lens_min=0,z_lens_mean=0.5133573511241993,z_lens_std=0.2933564230431462,
z_source_min=0,z_source_mean=2.6812382040555054,z_source_std=1.2940731971558737)
}
}
}