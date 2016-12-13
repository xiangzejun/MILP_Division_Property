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

from gurobipy import *

import time

class Lblock:
	def __init__(self, Round, activebits):
		self.Round = Round
		self.activebits = activebits
		self.blocksize = 64
		self.filename_model = "Lblock_" + str(self.Round) + "_" + str(self.activebits) + ".lp"
		self.filename_result = "result_" + str(self.Round) + "_" + str(self.activebits) + ".txt"
		fileobj = open(self.filename_model, "w")
		fileobj.close()
		fileboj = open(self.filename_result, "w")
		fileobj.close()


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

	NUMBER = 9

	def CreateObjectiveFunction(self):
		"""
		Create objective function of the MILP model.
		"""
		fileobj = open(self.filename_model, "a")
		fileobj.write("Minimize\n")
		eqn = []
		for i in range(0,8):
			for j in range(0,4):
				eqn.append("x" + "_" + str(self.Round) + "_" + str(3 - j) + "_" + str(i))
		for i in range(0,8):
			for j in range(0,4):
				eqn.append("y" + "_" + str(self.Round) + "_" + str(3 - j) + "_" + str(i))
		temp = " + ".join(eqn)
		fileobj.write(temp)
		fileobj.write("\n")
		fileobj.close()

	@staticmethod
	def CreateVariables(n,s):
		"""
		Generate the variables used in the model.
		"""
		array = [["" for i in range(0,4)] for j in range(0,8)]
		for i in range(0,8):
			for j in range(0,4):
				array[i][j] = s + "_" + str(n) + "_" + str(j) + "_" + str(i)
		return array

	def ConstraintsBySbox(self, variable1, variable2):
		"""
		Generate the constraints by Sbox layer.
		"""
		fileobj = open(self.filename_model,"a")
		for k in range(0,8):
			for coff in Lblock.S_T[7 - k]:
				temp = []
				for u in range(0,4):
					temp.append(str(coff[u]) + " " + variable1[k][3 - u])
				for v in range(0,4):
					temp.append(str(coff[4 + v]) + " " + variable2[k][3 - v])
				temp1 = " + ".join(temp)
				temp1 = temp1.replace("+ -", "- ")
				s = str(-coff[Lblock.NUMBER - 1])
				s = s.replace("--", "")
				temp1 += " >= " + s
				fileobj.write(temp1)
				fileobj.write("\n")
		fileobj.close(); 

	def ConstraintsByCopy(self, variablex, variableu, variabley):
		"""
		Generate the constraints by copy operation.
		"""
		fileobj = open(self.filename_model,"a")
		for i in range(0,8):
			for j in range(0,4):
				temp = []
				temp.append(variablex[i][j])
				temp.append(variableu[i][j])
				temp.append(variabley[i][j])
				s = " - ".join(temp)
				s += " = 0"
				fileobj.write(s)
				fileobj.write("\n")
		fileobj.close()

	def ConstraintsByXor(self, variabley,variablev,variablex):
		"""
		Generate the constraints by Xor operation.
		"""
		fileobj = open(self.filename_model,"a")
		for i in range(0,8):
			for j in range(0,4):
				temp = []
				temp.append(variablex[i][j])
				temp.append(variablev[i][j])
				temp.append(variabley[i][j])
				s = " - ".join(temp)
				s += " = 0"
				fileobj.write(s)
				fileobj.write("\n")
		fileobj.close()

	@classmethod
	def NibblePermutation(cls, variable):
		"""
		Permute the nibble.
		"""
		temp = [["" for i in range(0,4)] for j in range(0,8)]
		for i in range(0,8):
			temp[i] = variable[cls.Player[i]]
		return temp

	@staticmethod	
	def NibbleRotation(variable):
		"""
		Rotate the nibble.
		"""
		temp = [["" for i in range(0,4)] for j in range(0,8)]
		for i in range(0,8):
			temp[i] = variable[(i + 2) % 8]
		return temp

	def Constraint(self):
		"""
		Generate the constraints used in the MILP model.
		"""
		assert(self.Round >= 1)
		fileobj = open(self.filename_model, "a")
		fileobj.write("Subject To\n")
		fileobj.close()
		variableinx = Lblock.CreateVariables(0, "x")
		variableiny = Lblock.CreateVariables(0, "y")
		variableu = Lblock.CreateVariables(0, "u")
		variablev = Lblock.CreateVariables(0, "v")
		variableoutx = Lblock.CreateVariables(1, "x")
		variableouty = Lblock.CreateVariables(1, "y")
		if self.Round == 1:
			self.ConstraintsByCopy(variableinx,variableu,variableouty)
			self.ConstraintsBySbox(variableu,variablev)
			variablev = Lblock.NibblePermutation(variablev)
			variableiny = Lblock.NibbleRotation(variableiny)
			self.ConstraintsByXor(variableiny,variablev,variableoutx)
		else:
			self.ConstraintsByCopy(variableinx,variableu,variableouty)
			self.ConstraintsBySbox(variableu,variablev)
			variablev = Lblock.NibblePermutation(variablev)
			variableiny = Lblock.NibbleRotation(variableiny)
			self.ConstraintsByXor(variableiny,variablev,variableoutx)
			for i in range(1,self.Round):
				variableinx = variableoutx
				variableiny = variableouty
				variableouty = Lblock.CreateVariables((i + 1),"y")
				variableoutx = Lblock.CreateVariables((i + 1),"x")
				variableu = Lblock.CreateVariables(i, "u")
				variablev = Lblock.CreateVariables(i, "v")
				self.ConstraintsByCopy(variableinx,variableu,variableouty)
				self.ConstraintsBySbox(variableu,variablev)
				variablev = Lblock.NibblePermutation(variablev)
				variableiny = Lblock.NibbleRotation(variableiny)
				self.ConstraintsByXor(variableiny,variablev,variableoutx)


	def VariableBinary(self):
		"""
		Specify the variable type.
		"""
		fileobj = open(self.filename_model, "a")
		fileobj.write("Binary\n")
		for i in range(0,(self.Round + 1)):
			for j in range(0,8):
				for k in range(0,4):
					fileobj.write("x_" + str(i) + "_" + str(k) + "_" + str(j))
					fileobj.write("\n")
		for i in range(0,(self.Round + 1)):
			for j in range(0,8):
				for k in range(0,4):
					fileobj.write("y_" + str(i) + "_" + str(k) + "_" + str(j))
					fileobj.write("\n")
		for i in range(0,self.Round):
			for j in range(0,8):
				for k in range(0,4):
					fileobj.write("u_" + str(i) + "_" + str(k) + "_" + str(j))
					fileobj.write("\n")
		for i in range(0,self.Round):
			for j in range(0,8):
				for k in range(0,4):
					fileobj.write("v_" + str(i) + "_" + str(k) + "_" + str(j))
					fileobj.write("\n")
		fileobj.write("END")
		fileobj.close()

	def Init(self):
		"""
		Generate the initial constraints introduced by the initial division property.
		"""
		variabley = Lblock.CreateVariables(0,"y")
		variablex = Lblock.CreateVariables(0,"x")
		fileobj = open(self.filename_model, "a")
		eqn = []
		if self.activebits <= 32:
			for i in range(0,self.activebits):
				temp = variabley[7 - (i / 4)][i % 4] + " = 1"
				fileobj.write(temp)
				fileobj.write("\n")
			for i in range(self.activebits, 32):
				temp = variabley[7 - (i / 4)][i % 4] + " = 0"
				fileobj.write(temp)
				fileobj.write("\n")
			for i in range(0,32):
				temp = variablex[7 - (i / 4)][i % 4] + " = 0"
				fileobj.write(temp)
				fileobj.write("\n")

		else:
			for i in range(0,32):
				temp = variabley[7 - (i / 4)][i % 4] + " = 1"
				fileobj.write(temp)
				fileobj.write("\n")
			for i in range(0,(self.activebits - 32)):
				temp = variablex[7 - (i / 4)][i % 4] + " = 1"
				fileobj.write(temp)
				fileobj.write("\n")
			for i in range((self.activebits - 32), 32):
				temp = variablex[7 - (i / 4)][i % 4] + " = 0"
				fileobj.write(temp)
				fileobj.write("\n")
		fileobj.close()

	def MakeModel(self):
		"""
		Generate the MILP model of LBock given the round number and activebits.
		"""
		self.CreateObjectiveFunction()
		self.Constraint()
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
		Solve the MILP model to search the integral distinguisher of Lblock.
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
