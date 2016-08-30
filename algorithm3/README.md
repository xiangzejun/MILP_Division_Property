
## Algorithm 3 
For each folder named by a cipher name contains three file:
* [cipher.py] --- This python code produces the MILP model used in algorithm 3. cipher.py can produce different models according to the round number and number of active bits specified by the users.
* [cipher.lp] ---- This is the MILP model produced by cipher.py. The cipher.lp file in each folder is the MILP model used to search the corresponding integral distingusihers in Table 1. The MILP model of SIMON32 and SIMECK32 are presented in the corresponding folder, MILP models for other cipher variants can be easily produced by cipher.py.
* [Solver.py] --- This is the source code of Algorithm 3.
