"""
x_i_63,x_i_62,....x_i_0 denote the input to the (i+1)-th round.
"""

from gurobipy import *

import time

class Present:
	def __init__(self, Round, activebits):
		self.Round = Round
		self.activebits = activebits
		self.blocksize = 64
		self.filename_model = "Present_" + str(self.Round) + "_" + str(self.activebits) + ".lp"
		self.filename_result = "result_" + str(self.Round) + "_" + str(self.activebits) + ".txt"
		fileobj = open(self.filename_model, "w")
		fileobj.close()
		fileboj = open(self.filename_result, "w")
		fileobj.close()

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
	NUMBER = 9

	def CreateObjectiveFunction(self):
		"""
		Create objective function of the MILP model
		"""
		fileobj = open(self.filename_model, "a")
		fileobj.write("Minimize\n")
		eqn = []
		for i in range(0,64):
			eqn.append("x" + "_" + str(self.Round) + "_" + str(i))
		temp = " + ".join(eqn)
		fileobj.write(temp)
		fileobj.write("\n")
		fileobj.close()

	@staticmethod
	def CreateVariables(n):
		"""
		Generate the variables used in the model.
		"""
		array = []
		for i in range(0,64):
			array.append(("x" + "_" + str(n) + "_" + str(i)))
		return array

	def ConstraintsBySbox(self, variable1, variable2):
		"""
		Generate the constraints by sbox layer.
		"""
		fileobj = open(self.filename_model,"a")
		for k in range(0,16):
			for coff in Present.S_T:
				temp = []
				for u in range(0,4):
					temp.append(str(coff[u]) + " " + variable1[(k * 4) + 3 - u])
				for v in range(0,4):
					temp.append(str(coff[v + 4]) + " " + variable2[(k * 4) + 3 - v])
				temp1 = " + ".join(temp)
				temp1 = temp1.replace("+ -", "- ")
				s = str(-coff[Present.NUMBER - 1])
				s = s.replace("--", "")
				temp1 += " >= " + s
				fileobj.write(temp1)
				fileobj.write("\n")
		fileobj.close(); 

	@staticmethod
	def LinearLaryer(variable):
		"""
		Linear layer of Present.
		"""
		array = ["" for i in range(0,64)]
		for i in range(0,63):
			array[(16 * i) % 63] = variable[i]
		array[63] = variable[63]
		return array

	def Constraint(self):
		"""
		Generate the constraints used in the MILP model.
		"""
		assert(self.Round >= 1)
		fileobj = open(self.filename_model, "a")
		fileobj.write("Subject To\n")
		fileobj.close()
		variablein = Present.CreateVariables(0)
		variableout = Present.CreateVariables(1)
		if self.Round == 1:
			self.ConstraintsBySbox(variablein, variableout)
			# omit the last linear layer
		else:
			self.ConstraintsBySbox(variablein, variableout)
			for i in range(1, self.Round):
				variablein = Present.LinearLaryer(variableout)
				variableout= Present.CreateVariables(i + 1)
				self.ConstraintsBySbox(variablein, variableout)
				#omit the last linear layer

	def VariableBinary(self):
		"""
		Specify the variable type.
		"""
		fileobj = open(self.filename_model, "a")
		fileobj.write("Binary\n")
		for i in range(0, (self.Round + 1)):
			for j in range(0,64):
				fileobj.write("x_" + str(i) + "_" + str(j))
				fileobj.write("\n")
		fileobj.write("END")
		fileobj.close()

	def Init(self):
		"""
		Generate the constraints introduced by the initial division property.
		"""
		variableout = Present.CreateVariables(0)
		fileobj = open(self.filename_model, "a")
		eqn = []
		for i in range(0, self.activebits):
			temp = variableout[63 - i] + " = 1"
			fileobj.write(temp)
			fileobj.write("\n")
		for i in range(self.activebits, 64):
			temp = variableout[63 - i] + " = 0"
			fileobj.write(temp)
			fileobj.write("\n")
		fileobj.close()

	def MakeModel(self):
		"""
		Generate the MILP model of Present given the round number and activebits.
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
		Solve the MILP model to search the integral distinguisher of Present.
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


