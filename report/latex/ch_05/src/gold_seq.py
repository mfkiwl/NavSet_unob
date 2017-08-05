# Gold sequence generator - two 10-bits SSRG
def gold_seq(x1,x2,N_codes):
	#  Output register
	x=np.zeros([N_codes*1023])
	# Maximum-length sequence generators: 
	#  Shift registers
	shft_reg_1 = np.array ([1,1,1,1,1,1,1,1,1,1])
	shft_reg_2 = np.array ([1,1,1,1,1,1,1,1,1,1])
	#  Feedback registers - bit '1' means -> FB is connected	
	fbck_reg_1 = np.array ([0,0,1,0,0,0,0,0,0,1])
	fbck_reg_2 = np.array ([0,1,1,0,0,1,0,1,1,1])

	for i1 in range (0,N_codes*1023):
		g1  = shft_reg_1 [9]
		g2  = ( shft_reg_1[x1] + shft_reg_2[x2] ) % 2
		in1 = np.dot(shft_reg_1,fbck_reg_1) % 2
		in2 = np.dot(shft_reg_2,fbck_reg_2) % 2
		x[i1] = ( g1 + g2 ) % 2
		shft_reg_1 = np.roll(shft_reg_1,1)
		shft_reg_1[0] = in1
		shft_reg_2 = np.roll(shft_reg_2,1)
		shft_reg_2[0] = in2
	
	return (x.astype(bool))
