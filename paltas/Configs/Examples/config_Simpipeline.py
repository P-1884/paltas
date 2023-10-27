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
'z_lens':truncnorm(-1.7810948110060492,np.inf,loc=0.8658730642973657,scale=0.4861465313058086).rvs,
'gamma':2.0,
'theta_E':truncnorm(-3.2490400366185948,np.inf,loc=1.068456500606486,scale=0.3288529807464211).rvs,
'e1':norm(loc=-0.0017158114334681,scale=0.1110115284906313).rvs,
'e2':norm(loc=0.0553919606505096,scale=0.0852354435056784).rvs,
'center_x':norm(loc=-0.0056856083760816,scale=0.0974577205441075).rvs,
'center_y':norm(loc=-0.0040386167712699,scale=0.1008033031432856).rvs,
'gamma1':norm(loc=-0.0013687203825218,scale=0.0643702184480688).rvs,
'gamma2':norm(loc=1.9708971285053825e-05,scale=0.0637545433481586).rvs,
'ra_0':0.0, 'dec_0':0.0
}
},
'lens_light':{
'class': SingleSersicSource,
'parameters':{
'z_source':truncnorm(-1.7810948110060492,np.inf,loc=0.8658730642973657,scale=0.4861465313058086).rvs,
'mag_app':truncnorm(-10.75154615795547,np.inf,loc=23.007440345958976,scale=2.1399192272392296).rvs,
'output_ab_zeropoint':output_ab_zeropoint,
'R_sersic':truncnorm(-1.2451886565531105,np.inf,loc=0.3333037570691031,scale=0.2676733001983358).rvs,
'n_sersic':4.0,
'e1':norm(loc=-0.0010544646605801,scale=0.0898126834965152).rvs,
'e2':norm(loc=0.0587608725588675,scale=0.0597261237897697).rvs,
'center_x':norm(loc=-0.0056856083760816,scale=0.0974577205441075).rvs,
'center_y':norm(loc=-0.0040386167712699,scale=0.1008033031432856).rvs,
}
},
'source':{
'class': SingleSersicSource,
'parameters':{
'z_source':truncnorm(-3.0178938657171126,np.inf,loc=3.099763593732144,scale=1.0271281004759845).rvs,
'mag_app':truncnorm(-20.11330577429675,np.inf,loc=25.75938583108002,scale=1.2807136788025428).rvs,
'output_ab_zeropoint':output_ab_zeropoint,
'R_sersic':truncnorm(-1.144120027154079,np.inf,loc=0.7437858545622738,scale=0.6500942531461412).rvs,
'n_sersic':1.0,
'e1':norm(loc=-0.007313232579771,scale=0.2122382976298328).rvs,
'e2':norm(loc=0.0135350137849048,scale=0.2231764504746161).rvs,
'center_x':norm(loc=-0.0459823855236006,scale=0.5697759801591946).rvs,
'center_y':norm(loc=0.0033824392692899,scale=0.5600297563661846).rvs,
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
'lens_subtraction':True
}
