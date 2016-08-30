from gurobipy import *
import time

BLOCKSIZE = 64

def WriteObjective(file, obj):
	file.write("The objective value = %d\n" %obj.getValue())
	eqn1 = []
	eqn2 = []
	for i in range(0, BLOCKSIZE):
		u = obj.getVar(i)
		if u.getAttr("x") != 0:
			eqn1.append(u.getAttr('VarName'))
			eqn2.append(u.getAttr('x'))
	length = len(eqn1)
	for i in range(0,length):
		s = eqn1[i] + "=" + str(eqn2[i])
		file.write(s)
		file.write("\n")


if __name__ == "__main__":

	time_start = time.time()

	ROUND = int(raw_input("Input the target round number: "))
	ACTIVEBITS = int(raw_input("Input the number of acitvebits: "))

	filename = "result_" + str(ROUND) + "_" + str(ACTIVEBITS) + ".txt"
	
	m = read('Twine.lp')
	
	counter = 0
	
	file = open(filename, 'w')

	set_zero = []

	gloab_falg = False

	while counter < BLOCKSIZE:
		m.optimize()
		obj = m.getObjective()
		file.write("***************************************COUNTER = %d\n" %counter)
		WriteObjective(file, obj)
		if obj.getValue() > 1:
			gloab_falg = True
			break
		else:
			for i in range(0, BLOCKSIZE):
				u = obj.getVar(i)
				temp = u.getAttr('x')
				if temp == 1:
					set_zero.append(u.getAttr('VarName'))
					u.ub = 0
					m.update()
					counter += 1
					break


	if gloab_falg:
		file.write("Integral Distinguisher Found!\n\n")
		print "Integral Distinguisher Found!\n"
	else:
		file.write("Integral Distinguisher do NOT exist\n\n")
		print "Integral Distinguisher do NOT exist\n"

	file.write("Those are the coordinates set to zero!\n")
	for u in set_zero:
		file.write(u)
		file.write("\n")
	file.write("\n\n")

	time_end = time.time()
	file.write(("Time used = " + str(time_end - time_start)))
	file.close()
