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

from gurobipy import *

import time

class Twine:
	def __init__(self, Round, activebits):
		self.Round = Round
		self.activebits = activebits
		self.blocksize = 64
		self.filename_model = "Twine_" + str(self.Round) + "_" + str(self.activebits) + ".lp"
		self.filename_result = "result_" + str(self.Round) + "_" + str(self.activebits) + ".txt"
		fileobj = open(self.filename_model, "w")
		fileobj.close()
		fileboj = open(self.filename_result, "w")
		fileobj.close()

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

	NUMBER = 9

	def CreateObjectiveFunction(self):
		"""
		Create objective function of the MILP model.
		"""
		fileobj = open(self.filename_model, "a")
		fileobj.write("Minimize\n")
		eqn = []
		for i in range(0,16):
			for j in range(0,4):
				eqn.append("x" + "_" + str(self.Round) + "_" +str(3-j) + "_" + str(i))
		temp = " + ".join(eqn)
		fileobj.write(temp)
		fileobj.write("\n")
		fileobj.close()

	@staticmethod
	def CreateVariables(n):
		"""
		Generate the variables used in the model.
		"""
		array = [["" for i in range(0,4)] for j in range(0,16)]
		for i in range(0,16):
			for j in range(0,4):
				array[i][j] = "x_" + str(n) + "_" + str(j) + "_" + str(i)
		return array

	@staticmethod
	def CreateTempVariables(n):
		"""
		Generate the temp variables used in the model.
		"""
		array = [["" for i in range(0,4)] for j in range(0,16)]
		for i in range(0,16):
			for j in range(0,4):
				array[i][j] = "t_" + str(n) + "_" + str(j) + "_" + str(i)
		return array

	def ConstraintsBySbox(self, variable1, variable2, variabletemp):
		fileobj = open(self.filename_model, "a")
		for i in range(0,8):
			for j in range(0,4):
				temp = []
				temp.append(variable1[2 * i][j])
				temp.append(variabletemp[2 * i][j])
				temp.append(variable2[2 * i][j])
				fileobj.write((" - ".join(temp)) + " = 0")
				fileobj.write("\n")
		for k in range(0,8):
			for coeff in Twine.S_T:
				temp = []
				for u in range(0,4):
					temp.append(str(coeff[u]) + " " + variabletemp[2 * k][3 - u])
				for v in range(0,4):
					temp.append(str(coeff[v + 4]) + " " + variabletemp[2 * k + 1][3 - v])
				temp1 = " + ".join(temp)
				temp1 = temp1.replace("+ -", "- ")
				s = str(-coeff[Twine.NUMBER - 1])
				s = s.replace("--", "")
				temp1 += " >= " + s
				fileobj.write(temp1)
				fileobj.write("\n")

		for i in range(0,8):
			for j in range(0,4):
				temp = []
				temp.append(variable2[2 * i + 1][j])
				temp.append(variabletemp[2 * i + 1][j])
				temp.append(variable1[2 * i + 1][j])
				fileobj.write((" - ".join(temp)) + " = 0")
				fileobj.write("\n")
		fileobj.close(); 

	@classmethod
	def LinearLaryer(cls, variable):
		"""
		Linear layer of TWINE.
		"""
		array = [["" for i in range(0,4)] for j in range(0,16)]
		for i in range(0,16):
			array[cls.Player[i]] = variable[i]
		return array

	def Constrain(self):
		"""
		Generate the constraints used in the MILP model.
		"""
		assert(self.Round >= 1)
		fileobj = open(self.filename_model, "a")
		fileobj.write("Subject To\n")
		fileobj.close()
		variablein = Twine.CreateVariables(0)
		variableout = Twine.CreateVariables(1)
		variabletemp = Twine.CreateTempVariables(0)
		if self.Round == 1:
			self.ConstraintsBySbox(variablein, variableout,variabletemp)
			# omit the last nibble permutation
		else:
			self.ConstraintsBySbox(variablein, variableout,variabletemp)
			for i in range(1,self.Round):
				variablein = Twine.LinearLaryer(variableout)
				variableout= Twine.CreateVariables(i + 1)
				variabletemp = Twine.CreateTempVariables(i)
				self.ConstraintsBySbox(variablein, variableout,variabletemp)
				# omit the last nibble permutation

	def VariableBinary(self):
		"""
		Specify the variable type.
		"""
		fileobj = open(self.filename_model, "a")
		fileobj.write("Binary\n")
		for i in range(0,(self.Round + 1)):
			for j in range(0,16):
				for k in range(0,4):
					fileobj.write("x_" + str(i) + "_" + str(k) + "_" + str(j))
					fileobj.write("\n")
		for i in range(0,self.Round):
			for j in range(0,16):
				for k in range(0,4):
					fileobj.write("t_" + str(i) + "_" + str(k) + "_" + str(j))
					fileobj.write("\n")
		fileobj.write("END")
		fileobj.close()

	def Init(self):
		"""
		Generate constraints introudced by the initial division property.
		"""
		variableout = Twine.CreateVariables(0)
		fileobj = open(self.filename_model, "a")
		eqn = []
		for i in range(0,self.activebits):
			temp = variableout[15 - (i / 4)][i % 4] + " = 1"
			fileobj.write(temp)
			fileobj.write("\n")
		for i in range(self.activebits,64):
			temp = variableout[15 - (i / 4)][i % 4] + " = 0"
			fileobj.write(temp)
			fileobj.write("\n")
		fileobj.close()

	def MakeModel(self):
		"""
		Generate the MILP model of Twine given the round number and activebits.
		"""
		self.CreateObjectiveFunction()
		self.Constrain()
		self.Init()
		self.VariableBinary()

	def WriteObjective(self, obj):
		"""
		Write the objective value into filename_result.
		"""
		fileobj = open(self.filename_result, "a")
		fileobj.write("The objective value = %d\n" %obj.getValue())
		eqn1 = []
		eqn2 = []
		for i in range(0, self.blocksize):
			u = obj.getVar(i)
			if u.getAttr("x") != 0:
				eqn1.append(u.getAttr('VarName'))
				eqn2.append(u.getAttr('x'))
		length = len(eqn1)
		for i in range(0,length):
			s = eqn1[i] + "=" + str(eqn2[i])
			fileobj.write(s)
			fileobj.write("\n")
		fileobj.close()

	def SolveModel(self):
		"""
		Solve the MILP model to search the integral distinguisher of Twine.
		"""
		time_start = time.time()
		m = read(self.filename_model)
		counter = 0
		set_zero = []
		global_flag = False
		while counter < self.blocksize:
			m.optimize()
			# Gurobi syntax: m.Status == 2 represents the model is feasible.
			if m.Status == 2:
				obj = m.getObjective()
				if obj.getValue() > 1:
					global_flag = True
					break
				else:
					fileobj = open(self.filename_result, "a")
					fileobj.write("************************************COUNTER = %d\n" % counter)
					fileobj.close()
					self.WriteObjective(obj)
					for i in range(0, self.blocksize):
						u = obj.getVar(i)
						temp = u.getAttr('x')
						if temp == 1:
							set_zero.append(u.getAttr('VarName'))
							u.ub = 0
							m.update()
							counter += 1
							break
			# Gurobi syntax: m.Status == 3 represents the model is infeasible.
			elif m.Status == 3:
				global_flag = True
				break
			else:
				print "Unknown error!"

		fileobj = open(self.filename_result, "a")		
		if global_flag:
			fileobj.write("\nIntegral Distinguisher Found!\n\n")
			print "Integral Distinguisher Found!\n"
		else:
			fileobj.write("\nIntegral Distinguisher do NOT exist\n\n")
			print "Integral Distinguisher do NOT exist\n"

		fileobj.write("Those are the coordinates set to zero: \n")
		for u in set_zero:
			fileobj.write(u)
			fileobj.write("\n")
		fileobj.write("\n")
		time_end = time.time()
		fileobj.write(("Time used = " + str(time_end - time_start)))
		fileobj.close()
