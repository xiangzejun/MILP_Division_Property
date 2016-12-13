"""
Variables used in the division property propagation of SIMECK2n
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
u_i_0,u_i_1,......u_i_n-1 denotes the input to the left rotation by R1(0) bit.
v_i_0,v_i_1,......v_i_n-1 denotes the input to the left rotation by R2(5) bits.
w_i_0,w_i_1,......w_i_n-1 denotes the input to the left rotation by R3(1) bits.
where R1, R2, R3 denote the rotation constants which are defined later.
"""

from gurobipy import *

import time

class Simeck:
	def __init__(self, Round, activebits, word_len):
		self.Round = Round
		self.activebits = activebits
		self.blocksize = 2 * word_len
		self.WORD_LENGTH = word_len
		self.filename_model = "Simeck_" + str(word_len) + "_" + str(self.Round) + "_" + str(self.activebits) + ".lp"
		self.filename_result = "result_" + str(word_len) + "_" + str(self.Round) + "_" + str(self.activebits) + ".txt"
		fileobj = open(self.filename_model, "w")
		fileobj.close()
		fileboj = open(self.filename_result, "w")
		fileobj.close()

	# Rotational constants
	R1 = 0
	R2 = 5
	R3 = 1

	def CreateVariable(self, n, x):
		"""
		Generate variables used in the model.
		"""
		variable = []
		for i in range(0, self.WORD_LENGTH):
			variable.append(x + "_" + str(n) + "_" + str(i))
		return variable

	def CreateObjectiveFunction(self):
		"""
		Create Objective function of the MILP model.
		"""
		fileobj = open(self.filename_model, "a")
		fileobj.write("Minimize\n")
		eqn = []
		for i in range(0,self.WORD_LENGTH):
			eqn.append("x" + "_" + str(self.Round) + "_" + str(i))
		for j in range(0,self.WORD_LENGTH):
			eqn.append("y" + "_" + str(self.Round) + "_" + str(j))
		temp = " + ".join(eqn)
		fileobj.write(temp)
		fileobj.write("\n")
		fileobj.close()

	def VariableRotation(self, x, n):
		"""
		Bit Rotation.
		"""
		eqn = []
		for i in range(0, self.WORD_LENGTH):
			eqn.append(x[(i + n) % self.WORD_LENGTH])
		return eqn

	def CreateConstrainsSplit(self,x_in, u, v, w, y_out):
		"""
		Generate constraints by split operation.
		"""
		fileobj = open(self.filename_model, "a")
		for i in range(0, self.WORD_LENGTH):
			eqn = []
			eqn.append(x_in[i])
			eqn.append(u[i])
			eqn.append(v[i])
			eqn.append(w[i])
			eqn.append(y_out[i])
			temp = " - ".join(eqn)
			temp = temp + " = " + str(0)
			fileobj.write(temp)
			fileobj.write("\n")
		fileobj.close()

	def CreateConstraintsAnd(self, u,v,t):
		"""
		Generate constraints by and operation.
		"""
		fileobj = open(self.filename_model, "a")
		for i in range(0, self.WORD_LENGTH):
			fileobj.write((t[i] + " - " + u[i] + " >= " + str(0)))
			fileobj.write("\n")
			fileobj.write((t[i] + " - " + v[i] + " >= " + str(0)))
			fileobj.write("\n")
			fileobj.write((t[i] + " - " + u[i] + " - " + v[i] + " <= " + str(0)))
			fileobj.write("\n")
		fileobj.close()

	def CreateConstraintsXor(self, y_in, t, w, x_out):
		"""
		Generate the constraints by Xor operation.
		"""
		fileobj = open(self.filename_model, "a")
		for i in range(0, self.WORD_LENGTH):
			eqn = []
			eqn.append(x_out[i])
			eqn.append(y_in[i])
			eqn.append(t[i])
			eqn.append(w[i])
			temp = " - ".join(eqn)
			temp = temp + " = " + str(0)
			fileobj.write(temp)
			fileobj.write("\n")
		fileobj.close()

	def Init(self):
		"""
		Generate constraints by the initial division property.
		"""
		assert(self.activebits < (2 * self.WORD_LENGTH))
		fileobj = open(self.filename_model, "a")
		x = self.CreateVariable(0,"x")
		y = self.CreateVariable(0,"y")
		if self.activebits <= self.WORD_LENGTH:
			for i in range(0,self.activebits):
				fileobj.write((y[(self.WORD_LENGTH - 1 - i) % self.WORD_LENGTH] + " = " + str(1)))
				fileobj.write("\n")
			for i in range(self.activebits,self.WORD_LENGTH):
				fileobj.write((y[(self.WORD_LENGTH - 1 - i) % self.WORD_LENGTH] + " = " + str(0)))
				fileobj.write("\n")
			for i in range(0,self.WORD_LENGTH):
				fileobj.write((x[(self.WORD_LENGTH - 1 - i) % self.WORD_LENGTH] + " = " + str(0)))
				fileobj.write("\n")

		else:
			for i in range(0, self.WORD_LENGTH):
				fileobj.write((y[(self.WORD_LENGTH - 1 - i) % self.WORD_LENGTH] + " = " + str(1)))
				fileobj.write("\n")
			for i in range(0, (self.activebits - self.WORD_LENGTH)):
				fileobj.write((x[(self.WORD_LENGTH - 1 - i) % self.WORD_LENGTH] + " = " + str(1)))
				fileobj.write("\n")
			for i in range((self.activebits - self.WORD_LENGTH), self.WORD_LENGTH):
				fileobj.write((x[(self.WORD_LENGTH - 1 - i) % self.WORD_LENGTH] + " = " + str(0)))
				fileobj.write("\n")
		fileobj.close()

	def CreateConstraints(self):
		"""
		Generate constraints used in the MILP model.
		"""
		assert(self.Round >= 1)
		fileobj = open(self.filename_model, "a")
		fileobj.write("Subject To\n")
		fileobj.close()
		# Init(file)
		x_in = self.CreateVariable(0,"x")
		y_in = self.CreateVariable(0,"y")
		for i in range(0, self.Round):
			u = self.CreateVariable(i,"u")
			v = self.CreateVariable(i,"v")
			w = self.CreateVariable(i,"w")
			t = self.CreateVariable(i,"t")
			x_out = self.CreateVariable((i+1), "x")
			y_out = self.CreateVariable((i+1), "y")
			self.CreateConstrainsSplit(x_in, u, v, w, y_out)
			u = self.VariableRotation(u, Simeck.R1)
			v = self.VariableRotation(v, Simeck.R2)
			w = self.VariableRotation(w, Simeck.R3)
			self.CreateConstraintsAnd(u, v, t)
			self.CreateConstraintsXor(y_in, t, w, x_out)
			x_in = x_out
			y_in = y_out

	def BinaryVariable(self):
		"""
		Specify variable type.
		"""
		fileobj = open(self.filename_model, "a")
		fileobj.write("Binary\n")
		for i in range(0, self.Round):
			for j in range(0, self.WORD_LENGTH):
				fileobj.write(("x_" + str(i) + "_" + str(j)))
				fileobj.write("\n")
			for j in range(0, self.WORD_LENGTH):
				fileobj.write(("y_" + str(i) + "_" + str(j)))
				fileobj.write("\n")
			for j in range(0, self.WORD_LENGTH):
				fileobj.write(("u_" + str(i) + "_" + str(j)))
				fileobj.write("\n")
			for j in range(0, self.WORD_LENGTH):
				fileobj.write(("v_" + str(i) + "_" + str(j)))
				fileobj.write("\n")
			for j in range(0, self.WORD_LENGTH):
				fileobj.write(("w_" + str(i) + "_" + str(j)))
				fileobj.write("\n")
			for j in range(0, self.WORD_LENGTH):
				fileobj.write(("t_" + str(i) + "_" + str(j)))
				fileobj.write("\n")
		for j in range(0, self.WORD_LENGTH):
			fileobj.write(("x_" + str(self.Round) + "_" + str(j)))
			fileobj.write("\n")
		for j in range(0, self.WORD_LENGTH):
			fileobj.write(("y_" + str(self.Round) + "_" + str(j)))
			fileobj.write("\n")
		fileobj.write("END")
		fileobj.close()

	def MakeModel(self):
		"""
		Write the MILP model into the file
		"""
		self.CreateObjectiveFunction()
		self.CreateConstraints()
		self.Init()
		self.BinaryVariable()

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
		Solve the MILP model to search the integral distinguisher of Simeck.
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

