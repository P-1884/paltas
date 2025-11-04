#From Paltas: https://github.com/swagnercarena/paltas/blob/be74107f2e285f890d61fdd91f18dd07760fe085/paltas/Sampling/distributions.py#L171
def EllipticitiesTranslation(phi,q):
	import numpy as np
	"""Class that takes in distributions for q_lens and phi_lens, returns
	samples of e1 and e2 correspondingly
	Args:
		q_dist (scipy.stats.rv_continuous.rvs or float): distribution for
			axis ratio (can be callable or constant)
		phi_dist (scipy.stats.rv_continuous.rvs or float): distribution for
			orientation angle in radians (can be callable or constant)
	Returns a sample of e1,e2
		Returns:
			(float,float): samples of x-direction ellipticity
				eccentricity, xy-direction ellipticity eccentricity
	"""
	e1 = (1 - q)/(1+q) * np.cos(2*phi)
	e2 = (1 - q)/(1+q) * np.sin(2*phi)
	return e1,e2