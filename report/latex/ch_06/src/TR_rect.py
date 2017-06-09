def rect_tr( t,tp,ts,td,code ):
	n = np.size(code)
	x=np.zeros(np.shape(t)) > 1
	for i1 in range (0,n):
		p = pulse.rect_p( t,td + i1*(tp+ts),td + tp + i1*(tp+ts) )
		x = (x | p & code[i1]) * 1
	return (x)
