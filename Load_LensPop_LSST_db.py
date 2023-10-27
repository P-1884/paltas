import pandas as pd
from Ellipticities_Translation import EllipticitiesTranslation
import numpy as np
#[0] zl, lens redshift 
#[1] zs, source redshift 
#[2] b, Einstein radius (arcseconds) 
#[3] sig_v, lens velocity dispersion (km/s) 
#[4] ql, lens flattening (1=circular, q=1-e) 
#[5] rl, lens half light radius (arcseconds) NB/ sersic index is 4
#[6] lens g band magnitude
#[7] lens r band magnitude
#[8] lens i band magnitude
#[9] xs, source x coordinate relative, 0 is lens centre (arcseconds) 
#[10] ys, source y coordinate relative, 0 is lens centre (arcseconds) 
#[11] qs, source flattening (1=circular, q=1-e) 
#[12] ps, source position angle (degrees)
#[13] rs, source half light radius (arcseconds) NB/ sersic index is 1
#[14] source g band magnitude
#[15] source r band magnitude
#[16] source i band magnitude
#[17] mu_s, source magnification
#[18] g band coadd seeing
#[19] g band coadd signal-to-noise of source assuming poisson limited lens subtraction
#[20] r band coadd seeing
#[21] r band coadd signal-to-noise of source assuming poisson limited lens subtraction
#[22] i band coadd seeing
#[23] i band coadd signal-to-noise of source assuming poisson limited lens subtraction
#[24] signal-to-noise in the g - i difference image
#paltas_directory = '/global/homes/p/phil1884/paltas'
paltas_directory = '/mnt/zfsusers/hollowayp/paltas/'
db_LensPop_LSST = pd.read_csv(paltas_directory+'/LensPop_lenses_LSSTa.txt',skiprows=33,delimiter=' ',\
                      names = ['zL','zS','tE','sig_v','q_lens_flat', 'Re_lens', 'g_lens','r_lens','i_lens',\
                               'xs','ys','q_source_flat','PA_source','Re_source', 'g_source','r_source','i_source','mu_s',\
                               'g_see','g_see_sub','r_see','r_see_sub','i_see','i_see_sub','SNR'],index_col=False)
db_LSST_e1e2_source = EllipticitiesTranslation(db_LensPop_LSST['PA_source']*(2*np.pi/360),db_LensPop_LSST['q_source_flat'])
db_LensPop_LSST['e1_source'] = db_LSST_e1e2_source[0]
db_LensPop_LSST['e2_source'] = db_LSST_e1e2_source[1]