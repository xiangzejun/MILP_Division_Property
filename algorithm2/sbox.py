
class Sbox:
	def __init__(self, sbox):
		self.sbox = sbox
		self.SBOXSIZE = self.SboxSize()

	def SboxSize(self):
		"""	
		This function is used to calculate the size of a given sbox
		"""
		s = format(len(self.sbox), "b")
		num_of_1_in_the_binary_experission_of_the_len_of_sbox = s.count("1")
		assert num_of_1_in_the_binary_experission_of_the_len_of_sbox == 1
		return (len(s) - 1)

	def BitProduct(self, u, x):
		"""
		Return the value of the bitproduct function Pi_u(x)
		"""
		if (u & x) == u:
			return 1
		else:
			return 0

	def GetTruthTable(self, u):
		"""
		Retrieve the truth table of the boolean function Pi_u(y), where y = sbox(x)
		"""
		temp = [u for i in range(len(self.sbox))]
		table = map(self.BitProduct, temp, self.sbox)
		return table

	def ProcessTable(self, table):
		"""
		Process the truth table to get the ANF of the boolean function
		we use table size to calculate the SBOXSIZE
		"""
		for i in range(0, self.SBOXSIZE):
			for j in range(0, 2**i):
				for k in range(0, 2**(self.SBOXSIZE - 1 - i)):
					table[k + 2**(self.SBOXSIZE - 1 - i) + j*(2**(self.SBOXSIZE - i))] =\
	                table[k + 2**(self.SBOXSIZE - 1 - i) + j*(2**(self.SBOXSIZE - i))] ^\
	                table[k + j*(2**(self.SBOXSIZE - i))]

	def CreatANF(self):
		"""
		Return the ANF of the sbox, moreover, this function also return the ANF of boolean function which
		is the product of some coordinates of the sbox output
		"""
		ANF = [[]for i in range(0, len(self.sbox))]
		for i in range(1, len(self.sbox)): 
			table = self.GetTruthTable(i)
			self.ProcessTable(table)
			sqr = []
			for j in range(0, len(self.sbox)):
			    if table[j] != 0:
			        sqr.append(j)
			ANF[i] = sqr
		return ANF

	def CreateDivisionTrails(self):
		"""
		Return all the division trails of a given sbox
		"""
		ANF = self.CreatANF()
		INDP = []
	    # add zero vector into the division trails
		sqr = [0 for i in range(2 * self.SBOXSIZE)]
		INDP.append(sqr)
		# start from the non-zero vector
		for i in range(1, len(self.sbox)):
			sqn = []
			# start from the non-zero vector
			for j in range(1, len(self.sbox)):
				flag = False
				for entry in ANF[j]:
					if (i | entry) == entry:
						flag = True
						break
				if flag:
					sqn1 = []
					flag_add = True
					for t1 in sqn:
						if (t1 | j) == j:
							flag_add = False
							break
						elif (t1 | j) == t1:
							sqn1.append(t1)
					if flag_add:
						for t2 in sqn1:
							sqn.remove(t2)
						sqn.append(j)
			for num in sqn:
				a = format(i, "0256b")
				b = format(num, "0256b")
				a = list(reversed(map(int, list(a))))
				b = list(reversed(map(int, list(b))))
				a = a[0:self.SBOXSIZE]
				b = b[0:self.SBOXSIZE]
				a.reverse()
				b.reverse()
				INDP.append((a+b))
		return INDP

	def PrintfDivisionTrails(self, filename):
		"""
		Write all division trails of an sbox into a file
		"""
		INDP = self.CreateDivisionTrails()
		fileobj = open(filename, "w")
		fileobj.write("Division Trails of sbox:\n")
		for l in INDP:
			fileobj.write(str(l) + "\n")
		fileobj.write("\n")
		fileobj.close()


