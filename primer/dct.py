import math

# simple function for coefficents in discrete cosine transform
def C_uv(uv):
	if(uv == 0):
		return 1 / math.sqrt(2.0)
	else:
		return 1.0

# returns the 2d frequency domain of a square block of pixel values
def DCT(block):
	# initial 2d array to store the result of discrete cosine transform
	f_domain = [[0.0 for v in range(len(block))] for u in range(len(block))]

	for u in range(len(block)):
		for v in range(len(block)):
			projection = 0.0
			for x in range(len(block)):
				for y in range(len(block)):
					projection += block[x][y] * math.cos(u * math.pi * (2*x + 1) / (2 * len(block))) \
											  * math.cos(v * math.pi * (2*y + 1) / (2 * len(block)))

			f_domain[u][v] = 0.25 * C_uv(u) * C_uv(v) * projection
#			if(u > 25 or v > 25):
#				f_domain[u][v] = 0
	return f_domain

# returns the 2d spatial domain of a square block of pixel values
def inverse_DCT(block):
	s_domain = [[0.0 for y in range(len(block))] for x in range(len(block))]

	for x in range(len(block)):
		for y in range(len(block)):
			projection = 0.0
			for u in range(len(block)):
				for v in range(len(block)):
					projection += block[u][v] * C_uv(u) * C_uv(v) \
											  * math.cos(u * math.pi * (2.0*x + 1.0) / (2.0 * len(block))) \
											  * math.cos(v * math.pi * (2.0*y + 1.0) / (2.0 * len(block)))

			s_domain[x][y] = int(round(0.25 * projection))

	return s_domain
