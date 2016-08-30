"""
x_i_3_0,x_i_2_0,x_i_1_0,x_i_0_0,......x_i_3_7,x_i_2_7,x_i_1_7,x_i_0_7 denote the left halve 
  of the input of the (i+1)-th round
y_i_3_0,y_i_2_0,y_i_1_0,y_i_0_0,......y_i_3_7,y_i_2_7,y_i_1_7,y_i_0_7 denote the right halve
  of the input of the (i+1)-th round

u_i_3_0,u_i_2_0,u_i_1_0,u_i_0_0,......u_i_3_7,u_i_2_7,u_i_1_7,u_i_0_7 denote the input to 
  the sbox of the (i+1)-th round
v_i_3_0,v_i_2_0,v_i_1_0,v_i_0_0,......v_i_3_7,v_i_2_7,v_i_1_7,v_i_0_7 denote the output to
  the sbox of the (i+1)-th round

"""

filename = "LBlock.lp"
NUMBER = 9
LINE = 11

# Linear inequalities for the 8 Sboxes used in LBlock round function
S_T=[[[-1, -3, -4, -2, 1, 3, 2, -1, 5],\
[1, -1, 0, 0, -1, 1, -1, -1, 2],\
[-1, 0, -2, -2, 1, 0, -1, 2, 3],\
[1, 1, 1, 1, -1, -1, -1, -1, 0],\
[-1, -1, 0, 0, 2, 2, 1, 2, 0],\
[0, -1, -1, -1, 2, 2, 2, 1, 0],\
[-2, -1, 0, 1, 2, -2, -1, -2, 5],\
[1, 1, 1, 1, -2, -2, -2, 1, 1],\
[-1, -1, 2, 0, -1, -1, -2, 1, 3],\
[-1, 0, 2, -1, -1, -1, 1, -2, 3],\
[-1, 0, -1, 2, -1, -1, 1, -2, 3]],\
\
[[-1, -1, 0, 1, 1, -1, 0, -2, 3],\
[-1, -3, -4, -2, 1, 3, -1, 2, 5],\
[-1, 0, -2, -2, 1, 0, 2, -1, 3],\
[1, -1, 0, 1, -1, 1, -2, -2, 3],\
[-1, 0, -1, -2, 0, 0, 2, -1, 3],\
[1, 1, 1, 1, -1, -1, -1, -1, 0],\
[-2, -1, -1, 0, 2, 3, 2, 1, 1],\
[0, -1, -1, -1, 2, 2, 1, 2, 0],\
[-1, -1, 0, 0, -1, -1, -1, 2, 3],\
[-1, 0, -1, 2, -1, -1, -2, 1, 3],\
[-1, 0, 2, -1, -1, -1, -2, 1, 3],\
[1, 1, 1, 1, -2, -2, 1, -2, 1]],\
\
[[-1, -3, -4, -2, 2, 1, -1, 3, 5],\
[0, 0, 0, -1, -1, -1, 1, 0, 2],\
[0, -1, -1, 0, 1, -1, -1, 1, 2],\
[0, 1, 0, 1, -1, -1, 0, -1, 1],\
[-1, 0, -2, -2, -1, 1, 2, 0, 3],\
[1, -1, 0, 1, -2, -1, -2, 1, 3],\
[1, 1, 1, 1, -1, -1, -1, -1, 0],\
[0, -1, -1, -1, 2, 2, 1, 2, 0],\
[-1, -1, 0, 0, 1, 2, 2, 2, 0],\
[1, 1, 1, 1, -2, -2, 1, -2, 1],\
[0, 0, 0, 2, 0, -1, -1, -1, 1],\
[-1, 0, 2, -1, 1, -1, -2, -1, 3]],\
\
[[-1, -2, 0, 2, -1, -2, 1, -1, 4],\
[-1, 0, -2, -2, 0, -1, 1, 2, 3],\
[-1, -3, -4, -2, 3, 2, 1, -1, 5],\
[1, 0, 1, 1, 0, -2, -1, -2, 2],\
[-1, 0, -1, -2, 0, -1, 0, 2, 3],\
[1, 1, 1, 1, -1, -1, -1, -1, 0],\
[0, -1, -1, -1, 2, 2, 2, 1, 0],\
[-3, -1, -2, -1, 4, 1, 3, 2, 2],\
[-1, 0, 2, -1, -1, 1, -1, -2, 3],\
[-1, 0, -1, 2, -1, 1, -1, -2, 3],\
[1, 1, 1, 1, -2, -2, -2, 1, 1]],\
\
[[-1, -3, -4, -2, 2, 1, 3, -1, 5],\
[0, -1, -1, 0, 1, -1, 1, -1, 2],\
[0, 0, 0, -1, -1, -1, 0, 1, 2],\
[-1, 0, -2, -2, -1, 1, 0, 2, 3],\
[0, 1, 0, 1, -1, -1, -1, 0, 1],\
[1, -1, 0, 1, -2, -1, 1, -2, 3],\
[1, 1, 1, 1, -1, -1, -1, -1, 0],\
[-1, -1, 0, 1, -2, 1, -1, 0, 3],\
[-1, -1, 0, 0, 1, 2, 2, 2, 0],\
[0, -1, -1, -1, 2, 2, 2, 1, 0],\
[-1, 0, 2, -1, 1, -1, -1, -2, 3],\
[-1, 0, -1, 2, 1, -1, -1, -2, 3],\
[1, 1, 1, 1, -2, -2, -2, 1, 1]],\
\
[[-1, -3, -4, -2, 1, 2, 3, -1, 5],\
[0, 0, 0, -1, -1, -1, 0, 1, 2],\
[-1, 0, -2, -2, 1, -1, 0, 2, 3],\
[1, -1, 0, 1, -1, -2, 1, -2, 3],\
[1, 1, 1, 1, -1, -1, -1, -1, 0],\
[-1, -1, 0, 0, 2, 1, 2, 2, 0],\
[0, -1, -1, -1, 2, 2, 2, 1, 0],\
[1, 1, 1, 1, -2, -2, -2, 1, 1],\
[0, 0, 0, 2, -1, 0, -1, -1, 1],\
[-1, 0, 2, -1, -1, 1, -1, -2, 3]],\
\
[[-1, -1, 0, 1, 1, -1, 0, -2, 3],\
[-1, -3, -4, -2, 1, 3, -1, 2, 5],\
[-1, 0, -2, -2, 1, 0, 2, -1, 3],\
[1, -1, 0, 1, -1, 1, -2, -2, 3],\
[-1, 0, -1, -2, 0, 0, 2, -1, 3],\
[1, 1, 1, 1, -1, -1, -1, -1, 0],\
[-2, -1, -1, 0, 2, 3, 2, 1, 1],\
[0, -1, -1, -1, 2, 2, 1, 2, 0],\
[-1, -1, 0, 0, -1, -1, -1, 2, 3],\
[-1, 0, -1, 2, -1, -1, -2, 1, 3],\
[-1, 0, 2, -1, -1, -1, -2, 1, 3],\
[1, 1, 1, 1, -2, -2, 1, -2, 1]],\
\
[[-1, -1, 0, 1, 1, -1, 0, -2, 3],\
[-1, -3, -4, -2, 1, 3, -1, 2, 5],\
[-1, 0, -2, -2, 1, 0, 2, -1, 3],\
[1, -1, 0, 1, -1, 1, -2, -2, 3],\
[-1, 0, -1, -2, 0, 0, 2, -1, 3],\
[1, 1, 1, 1, -1, -1, -1, -1, 0],\
[-2, -1, -1, 0, 2, 3, 2, 1, 1],\
[0, -1, -1, -1, 2, 2, 1, 2, 0],\
[-1, -1, 0, 0, -1, -1, -1, 2, 3],\
[-1, 0, -1, 2, -1, -1, -2, 1, 3],\
[-1, 0, 2, -1, -1, -1, -2, 1, 3],\
[1, 1, 1, 1, -2, -2, 1, -2, 1]]]

# Sbox permutation
Player = [1,3,0,2,5,7,4,6]

def CreateObjectiveFunction(Round):
	file = open(filename, "a")
	file.write("Minimize\n")
	eqn = []
	for i in range(0,8):
		for j in range(0,4):
			eqn.append("x" + "_" + str(Round) + "_" + str(3 - j) + "_" + str(i))
	for i in range(0,8):
		for j in range(0,4):
			eqn.append("y" + "_" + str(Round) + "_" + str(3 - j) + "_" + str(i))
	temp = " + ".join(eqn)
	file.write(temp)
	file.write("\n")
	file.close()


def CreateVariables(n,s):
	array = [["" for i in range(0,4)] for j in range(0,8)]
	for i in range(0,8):
		for j in range(0,4):
			array[i][j] = s + "_" + str(n) + "_" + str(j) + "_" + str(i)
	return array


def ConstraintsBySbox(variable1, variable2):
	file = open(filename,"a")
	for k in range(0,8):
		for coff in S_T[7 - k]:
			temp = []
			for u in range(0,4):
				temp.append(str(coff[u]) + " " + variable1[k][3 - u])
			for v in range(0,4):
				temp.append(str(coff[4 + v]) + " " + variable2[k][3 - v])
			temp1 = " + ".join(temp)
			temp1 = temp1.replace("+ -", "- ")
			s = str(-coff[NUMBER - 1])
			s = s.replace("--", "")
			temp1 += " >= " + s
			file.write(temp1)
			file.write("\n")
	file.close(); 

def ConstraintsByCopy(variablex, variableu, variabley):
	file = open(filename,"a")
	for i in range(0,8):
		for j in range(0,4):
			temp = []
			temp.append(variablex[i][j])
			temp.append(variableu[i][j])
			temp.append(variabley[i][j])
			s = " - ".join(temp)
			s += " = 0"
			file.write(s)
			file.write("\n")
	file.close()

def ConstraintsByXor(variabley,variablev,variablex):
	file = open(filename,"a")
	for i in range(0,8):
		for j in range(0,4):
			temp = []
			temp.append(variablex[i][j])
			temp.append(variablev[i][j])
			temp.append(variabley[i][j])
			s = " - ".join(temp)
			s += " = 0"
			file.write(s)
			file.write("\n")
	file.close()

def NibblePermutation(variable):
	temp = [["" for i in range(0,4)] for j in range(0,8)]
	for i in range(0,8):
		temp[i] = variable[Player[i]]
	return temp
	
def NibbleRotation(variable):
	temp = [["" for i in range(0,4)] for j in range(0,8)]
	for i in range(0,8):
		temp[i] = variable[(i + 2) % 8]
	return temp

def Constraint(Round):
	assert(Round >= 1)
	file = open(filename, "a")
	file.write("Subject To\n")
	file.close()
	variableinx = CreateVariables(0, "x")
	variableiny = CreateVariables(0, "y")
	variableu = CreateVariables(0, "u")
	variablev = CreateVariables(0, "v")
	variableoutx = CreateVariables(1, "x")
	variableouty = CreateVariables(1, "y")
	if Round == 1:
		ConstraintsByCopy(variableinx,variableu,variableouty)
		ConstraintsBySbox(variableu,variablev)
		variablev = NibblePermutation(variablev)
		variableiny = NibbleRotation(variableiny)
		ConstraintsByXor(variableiny,variablev,variableoutx)
	else:
		ConstraintsByCopy(variableinx,variableu,variableouty)
		ConstraintsBySbox(variableu,variablev)
		variablev = NibblePermutation(variablev)
		variableiny = NibbleRotation(variableiny)
		ConstraintsByXor(variableiny,variablev,variableoutx)
		for i in range(1,Round):
			variableinx = variableoutx
			variableiny = variableouty
			variableouty = CreateVariables((i + 1),"y")
			variableoutx = CreateVariables((i + 1),"x")
			variableu = CreateVariables(i, "u")
			variablev = CreateVariables(i, "v")
			ConstraintsByCopy(variableinx,variableu,variableouty)
			ConstraintsBySbox(variableu,variablev)
			variablev = NibblePermutation(variablev)
			variableiny = NibbleRotation(variableiny)
			ConstraintsByXor(variableiny,variablev,variableoutx)

def VariableBinary(Round):
	file = open(filename, "a")
	file.write("Binary\n")
	for i in range(0,(Round + 1)):
		for j in range(0,8):
			for k in range(0,4):
				file.write("x_" + str(i) + "_" + str(k) + "_" + str(j))
				file.write("\n")
	for i in range(0,(Round + 1)):
		for j in range(0,8):
			for k in range(0,4):
				file.write("y_" + str(i) + "_" + str(k) + "_" + str(j))
				file.write("\n")
	for i in range(0,Round):
		for j in range(0,8):
			for k in range(0,4):
				file.write("u_" + str(i) + "_" + str(k) + "_" + str(j))
				file.write("\n")
	for i in range(0,Round):
		for j in range(0,8):
			for k in range(0,4):
				file.write("v_" + str(i) + "_" + str(k) + "_" + str(j))
				file.write("\n")
	file.write("END")
	file.close()

def Init(activebits):
	variabley = CreateVariables(0,"y")
	variablex = CreateVariables(0,"x")
	file = open(filename, "a")
	eqn = []
	if activebits <= 32:
		for i in range(0,activebits):
			temp = variabley[7 - (i / 4)][i % 4] + " = 1"
			file.write(temp)
			file.write("\n")
		for i in range(activebits, 32):
			temp = variabley[7 - (i / 4)][i % 4] + " = 0"
			file.write(temp)
			file.write("\n")
		for i in range(0,32):
			temp = variablex[7 - (i / 4)][i % 4] + " = 0"
			file.write(temp)
			file.write("\n")

	else:
		for i in range(0,32):
			temp = variabley[7 - (i / 4)][i % 4] + " = 1"
			file.write(temp)
			file.write("\n")
		for i in range(0,(activebits - 32)):
			temp = variablex[7 - (i / 4)][i % 4] + " = 1"
			file.write(temp)
			file.write("\n")
		for i in range((activebits - 32), 32):
			temp = variablex[7 - (i / 4)][i % 4] + " = 0"
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


	# empty the file
	file = open(filename,"w")
	file.close()

	# write the MILP model into the file 
	CreateObjectiveFunction(ROUND)
	Constraint(ROUND)
	Init(ACTIVEBITS)
	VariableBinary(ROUND)



