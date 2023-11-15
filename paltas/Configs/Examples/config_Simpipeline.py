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
'z_lens':truncnorm(-2.0643547703340706,np.inf,loc=0.5121770144622586,scale=0.248105132810759).rvs,
'gamma':truncnorm(-9.090909090909092,np.inf,loc=2.0,scale=0.22).rvs,
'theta_E':truncnorm(-4.37318666306154,np.inf,loc=1.3901772227340146,scale=0.3178865504361509).rvs,
'e1':norm(loc=0.0010705052680761,scale=0.1107442207974042).rvs,
'e2':norm(loc=0.0622486689457087,scale=0.0911057622038108).rvs,
'center_x':norm(loc=-0.0017628644237583,scale=0.1000390343128891).rvs,
'center_y':norm(loc=0.0001576312711377,scale=0.099882653175783).rvs,
'gamma1':norm(loc=0.0010716066764874,scale=0.0667254280929729).rvs,
'gamma2':norm(loc=0.0004073762272798,scale=0.0652109155879061).rvs,
'ra_0':0.0, 'dec_0':0.0
}
},
'lens_light':{
'class': SingleSersicSource,
'parameters':{
'z_source':truncnorm(-2.0643547703340706,np.inf,loc=0.5121770144622586,scale=0.248105132810759).rvs,
'mag_app':norm(loc=20.83430806868726,scale=1.5627126218108605).rvs,
'output_ab_zeropoint':output_ab_zeropoint,
'R_sersic':truncnorm(-0.84313649331203,np.inf,loc=0.4327529611255181,scale=0.513265603562677).rvs,
'n_sersic':4.0,
'e1':norm(loc=0.0003599184071794,scale=0.0887832154135639).rvs,
'e2':norm(loc=0.0658266339058222,scale=0.0633436306227756).rvs,
'center_x':norm(loc=-0.0017628644237583,scale=0.1000390343128891).rvs,
'center_y':norm(loc=0.0001576312711377,scale=0.099882653175783).rvs,
}
},
'source':{
'class': SingleSersicSource,
'parameters':{
'z_source':truncnorm(-2.4709825595389594,np.inf,loc=2.6870762041647054,scale=1.087452517133939).rvs,
'mag_app':norm(loc=24.65191127183449,scale=0.9680304743637757).rvs,
'output_ab_zeropoint':output_ab_zeropoint,
'R_sersic':truncnorm(-1.839589813220832,np.inf,loc=0.5181033076190359,scale=0.2816406700534608).rvs,
'n_sersic':1.0,
'e1':norm(loc=0.001014729402287,scale=0.2037517732962369).rvs,
'e2':norm(loc=0.0026329124102336,scale=0.2096969591393339).rvs,
'center_x':norm(loc=-0.0090360716617926,scale=0.5077365277152224).rvs,
'center_y':norm(loc=0.0077253087718501,scale=0.5080190829669426).rvs,
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
x_dist=norm(loc=-0.0017628644237583,scale=0.1000390343128891).rvs, 
y_dist=norm(loc=0.0001576312711377,scale=0.099882653175783).rvs),
'main_deflector:z_lens,source:z_source':dist.RedshiftsTruncNorm( 
z_lens_min=0,z_lens_mean=0.5121770144622586,z_lens_std=0.248105132810759,
z_source_min=0,z_source_mean=2.6870762041647054,z_source_std=1.087452517133939)
}
}
}