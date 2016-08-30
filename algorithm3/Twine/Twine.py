"""
x_i_3_0,x_i_2_0,x_i_1_0,x_i_0_0,......,x_i_3_15,x_i_2_15,x_i_1_15,x_i_0_15 
denote the 64-bit input of the (i+1)-th round.

x_i_3_0,x_i_2_0,x_i_1_0,x_i_0_0 denotes the first sbox of the (i+1)-th round input
with x_0_3_0 the most significant bit.

x_i_3_15,x_i_2_15,x_i_1_15,x_i_0_15 denotes the 15-th sbox of the frist round.

t_i_3_0,t_i_2_0,t_i_1_0,t_i_0_0,......,t_i_3_15,t_i_2_15,t_i_1_15,t_i_0_15
denote the input AND output of the eight Sboxes, among which the Sbox with even index 
denotes input of the Sboxlayer, and the Sbox with odd index denotes output of the 
Sboxlayer.
"""

filename = "Twine.lp"
NUMBER = 9
LINE = 11

# Linear inequalities for TWINE Sbox
S_T=[[-2, -1, -3, -1, 6, 5, 6, 4, 0],\
[-1, -1, -2, 0, 4, 3, 4, 2, 0],\
[0, -1, -1, -2, 4, 4, 2, 3, 0],\
[3, 0, 0, 0, -1, -1, -1, -1, 1],\
[0, 1, 0, 0, -1, 0, 0, -1, 1],\
[1, 4, 1, 1, -2, -2, -2, -2, 1],\
[0, 0, 2, 0, -1, -1, 0, -1, 1],\
[0, 0, 0, 3, -1, -1, -1, -1, 1],\
[-2, -2, 0, -2, -1, -1, 2, 1, 5],\
[-6, -4, -5, -6, 3, 1, 1, 2, 14],\
[-2, -2, -1, -3, 0, 2, -1, 1, 6]]

# Nibble permutation
Player = [5,0,1,4,7,12,3,8,13,6,9,2,15,10,11,14]

def CreateObjectiveFunction(Round):
	file = open(filename, "a")
	file.write("Minimize\n")
	eqn = []
	for i in range(0,16):
		for j in range(0,4):
			eqn.append("x" + "_" + str(Round) + "_" +str(3-j) + "_" + str(i))
	temp = " + ".join(eqn)
	file.write(temp)
	file.write("\n")
	file.close()


def CreateVariables(n):
	array = [["" for i in range(0,4)] for j in range(0,16)]
	for i in range(0,16):
		for j in range(0,4):
			array[i][j] = "x_" + str(n) + "_" + str(j) + "_" + str(i)
	return array

def CreateTempVariables(n):
	array = [["" for i in range(0,4)] for j in range(0,16)]
	for i in range(0,16):
		for j in range(0,4):
			array[i][j] = "t_" + str(n) + "_" + str(j) + "_" + str(i)
	return array


def ConstraintsBySbox(variable1, variable2, variabletemp):
	file = open(filename,"a")
	for i in range(0,8):
		for j in range(0,4):
			temp = []
			temp.append(variable1[2 * i][j])
			temp.append(variabletemp[2 * i][j])
			temp.append(variable2[2 * i][j])
			file.write((" - ".join(temp)) + " = 0")
			file.write("\n")

	for k in range(0,8):
		for i in range(0,LINE):
			temp = []
			for u in range(0,4):
				temp.append(str(S_T[i][u]) + " " + variabletemp[2 * k][3 - u])
			for v in range(0,4):
				temp.append(str(S_T[i][v + 4]) + " " + variabletemp[2 * k + 1][3 - v])
			temp1 = " + ".join(temp)
			temp1 = temp1.replace("+ -", "- ")
			s = str(-S_T[i][NUMBER - 1])
			s = s.replace("--", "")
			temp1 += " >= " + s
			file.write(temp1)
			file.write("\n")

	for i in range(0,8):
		for j in range(0,4):
			temp = []
			temp.append(variable2[2 * i + 1][j])
			temp.append(variabletemp[2 * i + 1][j])
			temp.append(variable1[2 * i + 1][j])
			file.write((" - ".join(temp)) + " = 0")
			file.write("\n")
	file.close(); 

def LinearLaryer(variable):
	array = [["" for i in range(0,4)] for j in range(0,16)]
	for i in range(0,16):
		array[Player[i]] = variable[i]
	return array

def Constrain(Round):
	assert(Round >= 1)
	file = open(filename, "a")
	file.write("Subject To\n")
	file.close()
	variablein = CreateVariables(0)
	variableout = CreateVariables(1)
	variabletemp = CreateTempVariables(0)
	if Round == 1:
		ConstraintsBySbox(variablein, variableout,variabletemp)
		# omit the last nibble permutation
	else:
		ConstraintsBySbox(variablein, variableout,variabletemp)
		for i in range(1,Round):
			variablein = LinearLaryer(variableout)
			variableout= CreateVariables(i + 1)
			variabletemp = CreateTempVariables(i)
			ConstraintsBySbox(variablein, variableout,variabletemp)
			# omit the last nibble permutation

def VariableBinary(Round):
	file = open(filename, "a")
	file.write("Binary\n")
	for i in range(0,(Round + 1)):
		for j in range(0,16):
			for k in range(0,4):
				file.write("x_" + str(i) + "_" + str(k) + "_" + str(j))
				file.write("\n")
	for i in range(0,Round):
		for j in range(0,16):
			for k in range(0,4):
				file.write("t_" + str(i) + "_" + str(k) + "_" + str(j))
				file.write("\n")
	file.write("END")
	file.close()

def Init(activebits):
	variableout = CreateVariables(0)
	file = open(filename, "a")
	eqn = []
	for i in range(0,activebits):
		temp = variableout[15 - (i / 4)][i % 4] + " = 1"
		file.write(temp)
		file.write("\n")
	for i in range(activebits,64):
		temp = variableout[15 - (i / 4)][i % 4] + " = 0"
		file.write(temp)
		file.write("\n")
	file.close()



if __name__ == "__main__":

	ROUND = int(raw_input("Input the target round number: "))
	while not (ROUND > 0):
		print "Input a round number greater than 0."
		ROUND = int(raw_input("Input the target round number again: "))

	ACTIVEBITS = int(raw_input("Input the number of acitvebits: "))
	while not (ACTIVEBITS < 64 and ACTIVEBITS > 0):
		print "Input a number of activebits with range (0, 64):"
		ACTIVEBITS = int(raw_input("Input the number of acitvebits again: "))

	#empty an txt file
	file = open(filename,"w")
	file.close()

	# write the MILP model into the file
	CreateObjectiveFunction(ROUND)
	Constrain(ROUND)
	Init(ACTIVEBITS)
	VariableBinary(ROUND)