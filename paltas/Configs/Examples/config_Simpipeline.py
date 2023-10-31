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
'z_lens':truncnorm(-1.8865444701063916,np.inf,loc=0.4568355983409655,scale=0.2421546937163916).rvs,
'gamma':2.0,
'theta_E':truncnorm(-4.132593693177156,np.inf,loc=1.4950328094333465,scale=0.3617662224819297).rvs,
'e1':norm(loc=-0.0060943081174119,scale=0.1055571908081157).rvs,
'e2':norm(loc=0.0678020040711208,scale=0.0929723985401996).rvs,
'center_x':norm(loc=0.0010894620090816,scale=0.1021346003466486).rvs,
'center_y':norm(loc=-0.000626546439325,scale=0.1040078361251386).rvs,
'gamma1':norm(loc=-0.0011598183143016,scale=0.0681872799018937).rvs,
'gamma2':norm(loc=0.000924638195015,scale=0.0701958105972862).rvs,
'ra_0':0.0, 'dec_0':0.0
}
},
'lens_light':{
'class': SingleSersicSource,
'parameters':{
'z_source':truncnorm(-1.8865444701063916,np.inf,loc=0.4568355983409655,scale=0.2421546937163916).rvs,
'mag_app':norm(loc=21.02921146752473,scale=1.8768236770209363).rvs,
'output_ab_zeropoint':output_ab_zeropoint,
'R_sersic':truncnorm(-1.083505832645003,np.inf,loc=0.3767020089455462,scale=0.3476695718618875).rvs,
'n_sersic':4.0,
'e1':norm(loc=-0.0051495538974389,scale=0.0913336661407818).rvs,
'e2':norm(loc=0.0726530877062765,scale=0.0715110215864414).rvs,
'center_x':norm(loc=0.0010894620090816,scale=0.1021346003466486).rvs,
'center_y':norm(loc=-0.000626546439325,scale=0.1040078361251386).rvs,
}
},
'source':{
'class': SingleSersicSource,
'parameters':{
'z_source':truncnorm(-1.8685279477294392,np.inf,loc=2.1923829200962266,scale=1.1733209143381147).rvs,
'mag_app':norm(loc=24.056431508967357,scale=0.7172701657563104).rvs,
'output_ab_zeropoint':output_ab_zeropoint,
'R_sersic':truncnorm(-1.7271909288863991,np.inf,loc=0.6673531849624067,scale=0.3863806680554306).rvs,
'n_sersic':1.0,
'e1':norm(loc=-0.0156133092730783,scale=0.193228461082578).rvs,
'e2':norm(loc=-0.0042034913440727,scale=0.2068432195811454).rvs,
'center_x':norm(loc=-0.0031859064993109,scale=0.5071438987474562).rvs,
'center_y':norm(loc=0.0232247362610413,scale=0.4740541058981876).rvs,
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
'cross_object':{
'parameters':{
('main_deflector:center_x,main_deflector:center_y,lens_light:center_x,lens_light:center_y'):
dist.DuplicateXY(
x_dist=norm(loc=0.0010894620090816,scale=0.1021346003466486).rvs, 
y_dist=norm(loc=-0.000626546439325,scale=0.1040078361251386).rvs),
'main_deflector:z_lens,source:z_source':dist.RedshiftsTruncNorm( 
z_lens_min=0,z_lens_mean=0.4568355983409655,z_lens_std=0.2421546937163916,
z_source_min=0,z_source_mean=2.1923829200962266,z_source_std=1.1733209143381147)
}
}
}