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
'z_lens':truncnorm(-1.9316781735341293,np.inf,loc=0.4877719913959017,scale=0.2525120375013046).rvs,
'gamma':norm(loc=2,scale=0.1918303639537035).rvs,
'theta_E':truncnorm(-3.854034453681824,np.inf,loc=1.415142080833239,scale=0.3671845952184807).rvs,
'e1':norm(loc=0.0006717732515758,scale=0.1918303639537035).rvs,
'e2':norm(loc=0.0006717732515758,scale=0.1918303639537035).rvs,
'center_x':norm(loc=0.0006717732515758,scale=0.1918303639537035).rvs,
'center_y':norm(loc=0.0006717732515758,scale=0.1918303639537035).rvs,
'gamma1':norm(loc=0.0006717732515758,scale=0.1918303639537035).rvs,
'gamma2':norm(loc=0.0006717732515758,scale=0.1918303639537035).rvs,
'ra_0':0.0, 'dec_0':0.0
}
},
'lens_light':{
'class': SingleSersicSource,
'parameters':{
'z_source':truncnorm(-1.9316781735341293,np.inf,loc=0.4877719913959017,scale=0.2525120375013046).rvs,
'mag_app':truncnorm(-10.341669207413242,np.inf,loc=18.29812747650855,scale=1.7693591923624732).rvs,
'output_ab_zeropoint':output_ab_zeropoint,
'R_sersic':truncnorm(-1.8573312405609943,np.inf,loc=0.9325585871164952,scale=0.5020960002992368).rvs,
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
'z_source':truncnorm(-2.463209501776144,np.inf,loc=2.130605796445149,scale=0.8649714102307722).rvs,
'mag_app':truncnorm(-23.112963222304234,np.inf,loc=25.59522698969772,scale=1.107397037044479).rvs,
'output_ab_zeropoint':output_ab_zeropoint,
'R_sersic':truncnorm(-1.3930624850924862,np.inf,loc=0.2754466206271935,scale=0.1977273981424505).rvs,
'n_sersic':1.0,
'e1':norm(loc=0.0006717732515758,scale=0.1918303639537035).rvs,
'e2':norm(loc=-0.0022746809017941,scale=0.1905041047369143).rvs,
'center_x':norm(loc=-0.0081003056719121,scale=0.3851088882157438).rvs,
'center_y':norm(loc=0.0022404619042228,scale=0.5160831813028319).rvs,
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
