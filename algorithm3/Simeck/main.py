# Algorithm 3 presented in paper "Applyint MILP Method to Searching Integral 
# Distinguishers based on Division Property for 6 Lightweight Block Ciphers"
# Regarding to the paper, please refer to https://eprint.iacr.org/2016/857
# For more information, feedback or questions, pleast contact at xiangzejun@iie.ac.cn

# Implemented by Xiang Zejun, State Key Laboratory of Information Security, 
# Institute Of Information Engineering, CAS

from simeck import Simeck

if __name__ == "__main__":

	WORD_LENGTH = int(raw_input("Input the word length of the target cipher (16 for SIMECK32): "))
	while WORD_LENGTH not in [16, 24, 32]:
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


	simeck = Simeck(ROUND, ACTIVEBITS, WORD_LENGTH)

	simeck.MakeModel()

	simeck.SolveModel()

