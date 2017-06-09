# 10-bits sequence outputting 3-bits SSRG in a Fibonacci form. 
def tri_seq(init_reg,fb_reg):
	#  Output register
	x=np.zeros([10]) 
	#  Shift register
	shft_reg = init_reg
	#  Feedback registers - bit '1' means -> FB is connected	
	#  defined as an input argument fb_reg
	for i1 in range (0,9):
		in1 = int(np.dot(shft_reg,fb_reg)%2)
		x[i1] = shft_reg[2]
		shft_reg = np.roll(shft_reg,1)
		shft_reg[0] = in1
	
	return (x.astype(bool))
