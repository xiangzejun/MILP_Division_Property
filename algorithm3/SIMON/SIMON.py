"""
Variables used in the division property propagation of SIMON2n
 x_i_0,x_i_1,......x_i_n-1,            y_i_0,y_i_1,......y_i_n-1

 u_i_0,u_i_1,......u_i_n-1,
                         >>>1
                               & ->>  t_i_0,t_i_1,......t_i_n-1
                         >>>8
 v_i_0,v_i_1,......v_i_n-1,

 w_i_0,w_i_1,......w_i_n-1,


 x_i+1_0,x_i+1_1,......x_i+1_n-1,      y_i+1_0,y_i+1_1,......y_i+1_n-1
=y_i_0,y_i_1,......y_i_n-1 +
 t_i_0,t_i_1,......t_i_n-1 +
 w_i_0,w_i_1,......w_i_n-1

x_i_0,x_i_1,......x_i_n-1 denotes the left halve of the (i+1)-th round.
y_i_0,y_i_1,......y_i_n-1 deontes the right halve of the (i+1)-th round.
u_i_0,u_i_1,......u_i_n-1 denotes the input to the left rotation by R1(1) bit.
v_i_0,v_i_1,......v_i_n-1 denotes the input to the left rotation by R2(8) bits.
w_i_0,w_i_1,......w_i_n-1 denotes the input to the left rotation by R3(2) bits.
where R1, R2, R3 denote the rotation constants which are defined later.
"""

global WORD_LENGTH

filename = "simon.lp"

# Rotational constants
R1 = 1
R2 = 8
R3 = 2

def CreateVariable(n,x):
	variable = []
	for i in range(0,WORD_LENGTH):
		variable.append(x + "_" + str(n) + "_" + str(i))
	return variable

def CreateObjectiveFunction(Round):
	file = open(filename, "a")
	file.write("Minimize\n")
	eqn = []
	for i in range(0,WORD_LENGTH):
		eqn.append("x" + "_" + str(Round) + "_" + str(i))
	for j in range(0,WORD_LENGTH):
		eqn.append("y" + "_" + str(Round) + "_" + str(j))
	temp = " + ".join(eqn)
	file.write(temp)
	file.write("\n")
	file.close()

def VariableRotation(x,n):
	eqn = []
	for i in range(0,WORD_LENGTH):
		eqn.append(x[(i + n) % WORD_LENGTH])
	return eqn

def CreateConstrainsSplit(x_in, u, v, w, y_out):
	file = open(filename, "a")
	for i in range(0,WORD_LENGTH):
		eqn = []
		eqn.append(x_in[i])
		eqn.append(u[i])
		eqn.append(v[i])
		eqn.append(w[i])
		eqn.append(y_out[i])
		temp = " - ".join(eqn)
		temp = temp + " = " + str(0)
		file.write(temp)
		file.write("\n")
	file.close()

def CreateConstraintsAnd(u,v,t):
	file = open(filename, "a")
	for i in range(0, WORD_LENGTH):
		file.write((t[i] + " - " + u[i] + " >= " + str(0)))
		file.write("\n")
		file.write((t[i] + " - " + v[i] + " >= " + str(0)))
		file.write("\n")
		file.write((t[i] + " - " + u[i] + " - " + v[i] + " <= " + str(0)))
		file.write("\n")
	file.close()

def CreateConstraintsXor(y_in, t, w, x_out):
	file = open(filename, "a")
	for i in range(0,WORD_LENGTH):
		eqn = []
		eqn.append(x_out[i])
		eqn.append(y_in[i])
		eqn.append(t[i])
		eqn.append(w[i])
		temp = " - ".join(eqn)
		temp = temp + " = " + str(0)
		file.write(temp)
		file.write("\n")
	file.close()

def Init(activebits):
	assert(activebits < (2 * WORD_LENGTH))
	file = open(filename, "a")
	x = CreateVariable(0,"x")
	y = CreateVariable(0,"y")
	if activebits <= WORD_LENGTH:
		for i in range(0,activebits):
			file.write((y[(WORD_LENGTH - 1 - i) % WORD_LENGTH] + " = " + str(1)))
			file.write("\n")
		for i in range(activebits,WORD_LENGTH):
			file.write((y[(WORD_LENGTH - 1 - i) % WORD_LENGTH] + " = " + str(0)))
			file.write("\n")
		for i in range(0,WORD_LENGTH):
			file.write((x[(WORD_LENGTH - 1 - i) % WORD_LENGTH] + " = " + str(0)))
			file.write("\n")

	else:
		for i in range(0, WORD_LENGTH):
			file.write((y[(WORD_LENGTH - 1 - i) % WORD_LENGTH] + " = " + str(1)))
			file.write("\n")
		for i in range(0, (activebits - WORD_LENGTH)):
			file.write((x[(WORD_LENGTH - 1 - i) % WORD_LENGTH] + " = " + str(1)))
			file.write("\n")
		for i in range((activebits - WORD_LENGTH), WORD_LENGTH):
			file.write((x[(WORD_LENGTH - 1 - i) % WORD_LENGTH] + " = " + str(0)))
			file.write("\n")
	file.close()


def CreateConstraints(Round):
	assert(Round >= 1)
	file = open(filename, "a")
	file.write("Subject To\n")
	file.close()
	# Init(file)
	x_in = CreateVariable(0,"x")
	y_in = CreateVariable(0,"y")
	for i in range(0,Round):
		u = CreateVariable(i,"u")
		v = CreateVariable(i,"v")
		w = CreateVariable(i,"w")
		t = CreateVariable(i,"t")
		x_out = CreateVariable((i+1), "x")
		y_out = CreateVariable((i+1), "y")
		CreateConstrainsSplit(x_in, u, v, w, y_out)
		u = VariableRotation(u, R1)
		v = VariableRotation(v, R2)
		w = VariableRotation(w, R3)
		CreateConstraintsAnd(u, v, t)
		CreateConstraintsXor(y_in, t, w, x_out)
		x_in = x_out
		y_in = y_out


def BinaryVariable(Round):
	file = open(filename, "a")
	file.write("Binary\n")
	for i in range(0, Round):
		for j in range(0, WORD_LENGTH):
			file.write(("x_" + str(i) + "_" + str(j)))
			file.write("\n")
		for j in range(0, WORD_LENGTH):
			file.write(("y_" + str(i) + "_" + str(j)))
			file.write("\n")
		for j in range(0, WORD_LENGTH):
			file.write(("u_" + str(i) + "_" + str(j)))
			file.write("\n")
		for j in range(0, WORD_LENGTH):
			file.write(("v_" + str(i) + "_" + str(j)))
			file.write("\n")
		for j in range(0, WORD_LENGTH):
			file.write(("w_" + str(i) + "_" + str(j)))
			file.write("\n")
		for j in range(0, WORD_LENGTH):
			file.write(("t_" + str(i) + "_" + str(j)))
			file.write("\n")
	for j in range(0, WORD_LENGTH):
		file.write(("x_" + str(Round) + "_" + str(j)))
		file.write("\n")
	for j in range(0, WORD_LENGTH):
		file.write(("y_" + str(Round) + "_" + str(j)))
		file.write("\n")
	file.write("END")
	file.close()


if __name__ == "__main__":

	WORD_LENGTH = int(raw_input("Input the word length of the target cipher (16 for SIMON32): "))
	while WORD_LENGTH not in [16, 24, 32, 48, 64]:
		print "Invalid word length!"
		WORD_LENGTH = int(raw_input("Input the word length again: "))

	ROUND = int(raw_input("Input the target round number: "))
	while not (ROUND > 0):
		print "Input a round number greater than 0."
		ROUND = int(raw_input("Input the target round number again: "))

	ACTIVEBITS = int(raw_input("Input the number of acitvebits: "))
	while not (ACTIVEBITS < 64 and ACTIVEBITS > 0):
		print "Input a number of activebits with range (0, 64):"
		ACTIVEBITS = int(raw_input("Input the number of acitvebits again: "))

	#empty the file
	file = open(filename, "w")
	file.close()

	# Write the MILP model into the file
	CreateObjectiveFunction(ROUND)
	CreateConstraints(ROUND)
	Init(ACTIVEBITS)
	BinaryVariable(ROUND)
