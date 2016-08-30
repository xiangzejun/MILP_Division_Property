from gurobipy import *
import time

def WriteObjective(file, obj):
	file.write("The objective value = %d\n" %obj.getValue())
	eqn1 = []
	eqn2 = []
	for i in range(0, 2*WORD_LENGTH):
		u = obj.getVar(i)
		if u.getAttr('x') > 0:
			eqn1.append(u.getAttr('VarName'))
			eqn2.append(u.getAttr('x'))
	for i in range(0,len(eqn1)):
		s = eqn1[i] + "=" + str(eqn2[i])
		file.write(s)
		file.write("\n")

if __name__ == "__main__":

	time_start = time.time()

	WORD_LENGTH = int(raw_input("Input the word length of the target cipher: "))
	ROUND = int(raw_input("Input the target round number: "))
	ACTIVEBITS = int(raw_input("Input the number of acitvebits: "))

	filename = "result_"+ str(WORD_LENGTH) + "_" + str(ROUND) + "_" + str(ACTIVEBITS) + ".txt"

	m = read('simeck.lp')

	counter = 0

	file = open(filename, 'w')

	set_zero = []

	global_flag = False

	while counter < (2 * WORD_LENGTH):
		m.optimize()
		obj = m.getObjective()
		file.write("***************************************COUNTER = %d\n" %counter)
		WriteObjective(file, obj)
		if obj.getValue() > 1:
			global_flag = True
			break

		else:
			for i in range(0, 2*WORD_LENGTH):
				u = obj.getVar(i)
				temp = u.getAttr('x')
				if temp == 1:
					set_zero.append(u.getAttr('VarName'))
					u.ub = 0
					m.update()
					counter += 1
					break

	if global_flag:
		file.write("Integral Distinguisher found!\n\n")
		print "Integral Distinguisher found!"
	else:	
		file.write("Integral Distinguisher do NOT exist\n\n")
		print "Integral Distinguisher do NOT exist"

	file.write("Those are the coordinates set to zero!\n")
	for u in set_zero:
		file.write(u)
		file.write("\n")
	file.write("\n\n")

	time_end = time.time()
	file.write("Time used = " + str((time_end - time_start)))
	file.close()
