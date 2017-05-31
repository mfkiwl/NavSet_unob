def rcos_tr( t,ts,td,code,pw,alpha ):

	#pw = 2e-3 # pulse width in ms
	#alpha = .5 # roll-off factor
	n = np.size(code)
	x=np.zeros(np.shape(t))
	for i1 in range (0,n):
		p = pulse.rcos_p( t,td + i1*(ts),pw,alpha )
		x = (x + p * code[i1]) 
	return (x)
