def rcos_p( t,t0,Tb,alpha ):
	beta = alpha / Tb 
	damp = np.cos(np.pi*beta*(t - t0)) / (1 - 4*(beta*(t - t0))**2)
	p = np.sinc(np.pi*(t - t0)/Tb) * damp
	return (p)
