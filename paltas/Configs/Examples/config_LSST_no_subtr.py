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
add_RSP_background=True
RSP_cutout_folder='/mnt/zfsusers/hollowayp/paltas/RSP_Coadd_Files_100000/'
RSP_ZP = 27 #Zeropoint for the coadds
output_ab_zeropoint = 27.85 #From https://smtn-002.lsst.io/. Refers to ZP which gives 1e/s. Is fainter in ADU (when gain=0.7)

#Asserting this as otherwise need to update read_noise and sky-brightness (and maybe gain too):
assert add_RSP_background==True

config_dict = {
'main_deflector':{
'class': PEMDShear,
'parameters':{
'M200': 1e13,
'z_lens': UPDATE,
'gamma': UPDATE,
'theta_E': UPDATE,
'e1': UPDATE,
'e2': UPDATE,
'center_x': UPDATE,
'center_y': UPDATE,
'gamma1': UPDATE,
'gamma2': UPDATE,
'ra_0':0.0, 'dec_0':0.0
}
},
'lens_light':{
'class': SingleSersicSource,
'parameters':{
'z_source':UPDATE,
'mag_app':UPDATE,
'output_ab_zeropoint':output_ab_zeropoint,
'R_sersic':UPDATE,
'n_sersic':UPDATE,
'e1':UPDATE,
'e2':UPDATE,
'center_x':UPDATE,
'center_y':UPDATE
}
},
'source':{
'class': SingleSersicSource,
'parameters':{
'z_source':UPDATE,
'mag_app':UPDATE,
'output_ab_zeropoint':output_ab_zeropoint,
'R_sersic':UPDATE,
'n_sersic':UPDATE,
'e1':UPDATE,
'e2':UPDATE,
'center_x':UPDATE,
'center_y':UPDATE
}
},
'cosmology':{
'parameters':{
'cosmology_name': 'planck18'
}
},
'psf':{
'parameters':{
#Could also get value for seeing from https://www.lsst.org/scientists/keynumbers, of 0.67"
'psf_type':'GAUSSIAN',
'fwhm': 0.71

}
},
#From Lenspop: https://github.com/tcollett/LensPop/blob/master/Surveys.py
#self.pixelsize=0.18
#self.side=111
#self.bands=['g','r','i']
#self.zeropoints=[30,30,30]
#self.zeroexposuretime=25
#self.skybrightnesses=[21.7,20.7,20.1]
#self.exposuretimes=[3000,6000,6000]
#self.gains=[4.5,4.5,4.5]
#self.seeing=[.4,.4,.4]
#self.nexposures=100
#self.degrees_of_survey=18000
#self.readnoise=(10/4.5)
#From Lenstronomy: https://github.com/lenstronomy/lenstronomy/blob/main/lenstronomy/SimulationAPI/ObservationConfig/LSST.py:
#i_band_obs = {
#    "exposure_time": 15.0,
#    "sky_brightness": 20.48,
#    "magnitude_zero_point": 27.79,
#    "num_exposures": 460,
#    "seeing": 0.71,
#    "psf_type": "GAUSSIAN"}
#self.camera = {
#    "read_noise": 10,  # will be <10
#    "pixel_scale": 0.2,
#    "ccd_gain": 2.3}
#Currently using the lenstronomy values:
'detector':{
'parameters':{
'pixel_scale':0.2,'ccd_gain':0.7,'read_noise':0, #Noise is added from RSP. Gain from here https://community.lsst.org/t/dp0-zeropoints-adding-poisson-noise/8230/7, correct for DP0
'magnitude_zero_point':output_ab_zeropoint,
'exposure_time':30,'sky_brightness':100, #Sky needs to be faint, as added in from RSP. Exposure time must = 30 for RSP.
'num_exposures':None,'background_noise':None
}
},
'lens_subtraction':False,
}
