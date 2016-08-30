# This function is used to calculate the size of a given sbox
def SboxSize(sbox):
	s = format(len(sbox), "b")
	num_of_1_in_the_binary_experission_of_the_len_of_sbox = s.count("1")
	assert num_of_1_in_the_binary_experission_of_the_len_of_sbox == 1
	return (len(s) - 1)


# Return the value of the bitproduct function Pi_u(x)
def BitProduct(u, x):
	if (u & x) == u:
		return 1
	else:
		return 0


# Retrieve the truth table of the boolean function Pi_u(y), where y = sbox(x)
def GetTruthTable(sbox, u):
    temp = [u for i in range(len(sbox))]
    table = map(BitProduct, temp, sbox)
    return table


# Process the truth table to get the ANF of the boolean function
def ProcessTable(table):
	# we use table size to calculate the SBOXSIZE
	SBOXSIZE = SboxSize(table)
	for i in range(0, SBOXSIZE):
		for j in range(0, 2**i):
			for k in range(0, 2**(SBOXSIZE - 1 - i)):
				table[k + 2**(SBOXSIZE - 1 - i) + j*(2**(SBOXSIZE - i))] =\
                table[k + 2**(SBOXSIZE - 1 - i) + j*(2**(SBOXSIZE - i))] ^\
                table[k + j*(2**(SBOXSIZE - i))]


# Return the ANF of the sbox, moreover, we also return the ANF of boolean function which
# is the product of some coordinates of the sbox output
def CreatANF(sbox):
	ANF = [[]for i in range(0, len(sbox))]
	for i in range(1, len(sbox)): 
		table = GetTruthTable(sbox, i)
		ProcessTable(table)
		sqr = []
		for j in range(0, len(sbox)):
		    if table[j] != 0:
		        sqr.append(j)
		ANF[i] = sqr
	return ANF


# Return all the division trails of a given sbox
def CreateDivisionTrails(sbox):
	ANF = CreatANF(sbox)
	SBOXSIZE = SboxSize(sbox)
	INDP = []
    # add zero vector into the division trails
	sqr = [0 for i in range(2 * SBOXSIZE)]
	INDP.append(sqr)
	# start from the non-zero vector
	for i in range(1, len(sbox)):
		sqn = []
		# start from the non-zero vector
		for j in range(1, len(sbox)):
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
			a = a[0:SBOXSIZE]
			b = b[0:SBOXSIZE]
			a.reverse()
			b.reverse()
			INDP.append((a+b))
	return INDP


# Write all division trails of an sbox into a file
def PrintfDivisionTrails(fileobj, sbox):
	INDP = CreateDivisionTrails(sbox)
	fileobj.write("Division Trails of sbox:\n")
	for l in INDP:
		fileobj.write(str(l) + "\n")
	fileobj.write("\n")


if __name__ == "__main__":

	# PRESENT Sbox
	sbox = [0xc, 0x5, 0x6, 0xb, 0x9, 0x0, 0xa, 0xd, 0x3, 0xe, 0xf, 0x8, 0x4, 0x7, 0x1, 0x2]
	
	filename = "DivisionTrails.txt"
	fileobj = open(filename, "w")

	PrintfDivisionTrails(fileobj, sbox)

	fileobj.close()