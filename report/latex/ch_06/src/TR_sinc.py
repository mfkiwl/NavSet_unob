def sinc_tr( t,ts,td,code,pw ):

	#pw = 2e-3 # pulse width in ms	
	n = np.size(code)
	x=np.zeros(np.shape(t))
	for i1 in range (0,n):
		p = pulse.sinc_p( t,td + i1*(ts),pw )	
		x = (x + p * code[i1]) 
	return (x)

