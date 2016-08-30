"""
x_i_0_0, x_i_0_1,......,x_i_0_15
x_i_1_0, x_i_1_1,......,x_i_1_15
x_i_2_0, x_i_2_1,......,x_i_2_15
x_i_3_0, x_i_3_1,......,x_i_3_15
denote the input to the (i+1)-th round.

x_i_0_0
x_i_1_0
x_i_2_0
x_i_3_0
denotes the first sbox of the input with x_0_3_0 the most significant bit.
"""

filename = "Rectangle.lp"
NUMBER = 9
LINE = 17

#Linear inequalities for the RECTANGLE Sbox
S_T=[[-1, -1, -2, -3, -2, 0, 1, 2, 6],\
[0, 0, 0, 0, -1, -1, 0, 1, 1],\
[1, 1, 1, 1, -1, -1, -1, -1, 0],\
[3, 1, 0, 0, -1, -2, -1, -2, 2],\
[0, 1, 0, 1, 0, -1, -2, -1, 2],\
[0, -1, -1, -1, 1, 2, 0, 2, 1],\
[-2, 0, -1, -1, 1, 0, 2, 1, 2],\
[-3, -1, -1, -2, 1, 2, 2, -1, 4],\
[0, -1, -1, 0, 1, 1, 1, 0, 1],\
[-3, -1, -1, -2, 3, 2, 2, 1, 2],\
[0, 2, 3, 0, -3, -1, -2, -1, 3],\
[-1, -1, 0, -1, 2, 2, 1, 1, 0],\
[0, -2, -1, -1, 3, 4, 2, 2, 0],\
[1, 1, 1, 1, -2, 0, 0, -2, 1],\
[0, 0, 0, 2, -1, -1, -1, 0, 1],\
[3, -4, -1, -1, -2, -1, -3, 2, 7],\
[1, 0, 1, 1, 1, -3, -2, -2, 3]]

def CreateObjectiveFunction(Round):
	file = open(filename, "a")
	file.write("Minimize\n")
	eqn = []
	for i in range(0,4):
		for j in range(0,16):
			eqn.append("x" + "_" + str(Round) + "_" +str(i) + "_" + str(j))
	temp = " + ".join(eqn)
	file.write(temp)
	file.write("\n")
	file.close()


def CreateVariables(n):
	array = [[" " for i in range(0,16)] for j in range(0,4)]
	for i in range(0,4):
		for j in range(0,16):
			array[i][j] = "x" + "_" + str(n) + "_" + str(i) + "_" + str(j)
	return array

def ConstraintsBySbox(variable1, variable2):
	file = open(filename,"a")
	for k in range(0,16):
		for i in range(0,LINE):
			temp = []
			for u in range(0,4):
				temp.append(str(S_T[i][u]) + " " + variable1[3-u][k])
			for v in range(0,4):
				temp.append(str(S_T[i][v + 4]) + " " + variable2[3-v][k])
			temp1 = " + ".join(temp)
			temp1 = temp1.replace("+ -", "- ")
			s = str(-S_T[i][NUMBER - 1])
			s = s.replace("--", "")
			temp1 += " >= " + s
			file.write(temp1)
			file.write("\n")
	file.close(); 

def LinearLaryer(variable):
	array = [[" " for i in range(0,16)] for j in range(0,4)]
	for i in range(0,16):
		array[0][i] = variable[0][i]
	for i in range(0,16):
		array[1][i] = variable[1][(i + 1) % 16]
	for i in range(0,16):
		array[2][i] = variable[2][(i + 12) % 16]
	for i in range(0,16):
		array[3][i] = variable[3][(i + 13) % 16]
	return array

def Constrain(Round):
	assert(Round >= 1)
	file = open(filename, "a")
	file.write("Subject To\n")
	file.close()
	variablein = CreateVariables(0)
	variableout = CreateVariables(1)
	if Round == 1:
		ConstraintsBySbox(variablein, variableout)
		# omit the last linear layer
	else:
		ConstraintsBySbox(variablein, variableout)
		for i in range(1,Round):
			variablein = LinearLaryer(variableout)
			variableout= CreateVariables(i + 1)
			ConstraintsBySbox(variablein, variableout)
			# omit the last linear layer

def VariableBinary(Round):
	file = open(filename, "a")
	file.write("Binary\n")
	for i in range(0,(Round + 1)):
		for j in range(0,4):
			for k in range(0,16):
				file.write("x_" + str(i) + "_" + str(j) + "_" + str(k))
				file.write("\n")
	file.write("END")
	file.close()

def Init(activebits):
	variableout = CreateVariables(0)
	file = open(filename, "a")
	eqn = []
	for i in range(0,activebits):
		temp = variableout[(i + 2) % 4][15 - (i / 4)] + " = 1"
		file.write(temp)
		file.write("\n")
	for i in range(activebits,64):
		temp = variableout[(i + 2) % 4][15 - (i / 4)] + " = 0"
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



