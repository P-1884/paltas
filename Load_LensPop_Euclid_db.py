import pandas as pd
from Ellipticities_Translation import EllipticitiesTranslation
import numpy as np
#[0] zl, lens redshift 
#[1] zs, source redshift 
#[2] b, Einstein radius (arcseconds) 
#[3] sig_v, lens velocity dispersion (km/s) 
#[4] ql, lens flattening (1=circular, q=1-e) 
#[5] rl, lens half light radius (arcseconds) NB/ sersic index is 4
#[6] lens VIS band magnitude
#[7] xs, source x coordinate relative, 0 is lens centre (arcseconds) 
#[8] ys, source y coordinate relative, 0 is lens centre (arcseconds) 
#[9] qs, source flattening (1=circular, q=1-e) 
#[10] ps, source position angle (degrees)
#[11] rs, source half light radius (arcseconds) NB/ sersic index is 1
#[12] source VIS band magnitude
#[13] mu_s, source magnification
#[14] VIS band coadd seeing
#[15] VIS band coadd signal-to-noise of source assuming poisson limited lens subtraction
#paltas_directory = '/global/homes/p/phil1884/paltas'
paltas_directory = '/mnt/zfsusers/hollowayp/paltas/'
db_LensPop_Euclid = pd.read_csv(paltas_directory+'/LensPop_lenses_Euclid.txt',skiprows=33,delimiter=' ',\
                      names = ['zL','zS','tE','sig_v','q_lens_flat', 'Re_lens', 'VIS_lens',\
                               'xs','ys','q_source_flat','PA_source','Re_source','VIS_source','mu_s',\
                               'VIS_see','VIS_SNR_sub'],index_col=False)
db_Euclid_e1e2_source = EllipticitiesTranslation(db_LensPop_Euclid['PA_source']*(2*np.pi/360),db_LensPop_Euclid['q_source_flat'])
db_LensPop_Euclid['e1_source'] = db_Euclid_e1e2_source[0]
db_LensPop_Euclid['e2_source'] = db_Euclid_e1e2_source[1]