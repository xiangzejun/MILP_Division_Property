"""
x_i_63,x_i_62,....x_i_0 denote the input to the (i+1)-th round.
"""

filename = "Present.lp"
NUMBER = 9
LINE = 11

# Linear inequalities for the PRESENT Sbox
S_T=[[1, 1, 1, 1, -1, -1, -1, -1, 0],\
[0, -1, -1, -2, 1, 0, 1, -1, 3],\
[0, -1, -1, -2, 4, 3, 4, 2, 0],\
[-2, -1, -1, 0, 2, 2, 2, 1, 1],\
[-2, -1, -1, 0, 3, 3, 3, 2, 0],\
[0, 0, 0, 0, -1, 1, -1, 1, 1],\
[-2, -2, -2, -4, 1, 4, 1, -3, 7],\
[1, 1, 1, 1, -2, -2, 1, -2, 1],\
[0, -4, -4, -2, 1, -3, 1, 2, 9],\
[0, 0, 0, -2, -1, -1, -1, 2, 3],\
[0, 0, 0, 1, 1, -1, -2, -1, 2]]

def CreateObjectiveFunction(Round):
	file = open(filename, "a")
	file.write("Minimize\n")
	eqn = []
	for i in range(0,64):
		eqn.append("x" + "_" + str(Round) + "_" + str(i))
	temp = " + ".join(eqn)
	file.write(temp)
	file.write("\n")
	file.close()

def CreateVariables(n):
	array = []
	for i in range(0,64):
		array.append(("x" + "_" + str(n) + "_" + str(i)))
	return array

def ConstraintsBySbox(variable1, variable2):
	file = open(filename,"a")
	for k in range(0,16):
		for i in range(0,LINE):
			temp = []
			for u in range(0,4):
				temp.append(str(S_T[i][u]) + " " + variable1[(k * 4) + 3 - u])
			for v in range(0,4):
				temp.append(str(S_T[i][v + 4]) + " " + variable2[(k * 4) + 3 - v])
			temp1 = " + ".join(temp)
			temp1 = temp1.replace("+ -", "- ")
			s = str(-S_T[i][NUMBER - 1])
			s = s.replace("--", "")
			temp1 += " >= " + s
			file.write(temp1)
			file.write("\n")
	file.close(); 

def LinearLaryer(variable):
	array = ["" for i in range(0,64)]
	for i in range(0,63):
		array[(16 * i) % 63] = variable[i]
	array[63] = variable[63]
	return array

def Constraint(Round):
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
			#omit the last linear layer

def VariableBinary(Round):
	file = open(filename, "a")
	file.write("Binary\n")
	for i in range(0,(Round + 1)):
		for j in range(0,64):
			file.write("x_" + str(i) + "_" + str(j))
			file.write("\n")
	file.write("END")
	file.close()

def Init(activebits):
	variableout = CreateVariables(0)
	file = open(filename, "a")
	eqn = []
	for i in range(0,activebits):
		temp = variableout[63 - i] + " = 1"
		file.write(temp)
		file.write("\n")
	for i in range(activebits,64):
		temp = variableout[63 - i] + " = 0"
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
	Constraint(ROUND)
	Init(ACTIVEBITS)
	VariableBinary(ROUND)

