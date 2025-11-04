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
numpix = 200
mask_radius = 0
mag_cut = 0.0
catalog = False
save_noise=False
add_RSP_background=False
RSP_cutout_folder='/mnt/extraspace/hollowayp/paltas_data/Coadd_files/'
RSP_ZP = 27 #Zeropoint for the coadds
output_ab_zeropoint = 31.8

config_dict = {
'main_deflector':{
'class': PEMDShear,
'parameters':{
'M200': 1e13,
'z_lens':0.5,
'gamma':2.1,
'theta_E':3.0,
'e1':0.1,
'e2':0.1,
'center_x':0,
'center_y':0,
'gamma1':0,
'gamma2':0,
'ra_0':0.0, 'dec_0':0.0
}
},
'lens_light':{
'class': SingleSersicSource,
'parameters':{
'z_source':0.5,
'mag_app':21,
'output_ab_zeropoint':output_ab_zeropoint,
'R_sersic':0.4,
'n_sersic':4.0,
'e1':0.1,
'e2':0.1,
'center_x':0,
'center_y':0,
}
},
'source':{
'class': SingleSersicSource,
'parameters':{
'z_source':1,
'mag_app':22,
'output_ab_zeropoint':output_ab_zeropoint,
'R_sersic':0.4,
'n_sersic':2.0,
'e1':0,
'e2':0,
'center_x':0.4,
'center_y':0,
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
'pixel_scale':0.05,'ccd_gain':2.3,'read_noise':10,
'magnitude_zero_point':output_ab_zeropoint,
'exposure_time':30,'sky_brightness':20.48,
'num_exposures':230,'background_noise':None
}
},
'lens_subtraction':False,
}

'''
python="/mnt/users/hollowayp/python114_archive/bin/python3.11"
test_queue='redwood'
addqueue -c '3hr' -m 10 -q $test_queue --requeue $python ./paltas/generate.py ./paltas/Configs/Examples/config_SW_outreach.py /mnt/zfsusers/hollowayp/paltas/SW_outreach/ --n 1
'''