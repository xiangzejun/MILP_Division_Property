### Algorithm 1

This folder contains three files which are used to select a set of linear inequalities from the H-Representation of a set of points. 
* [Reduce.cpp] ---This is the C++ source code to implement Algorithm 1.
* [Inequalities.txt] ---This txt file contains the H-Representation of a given set of points, which is actually a set of linear inequalities returned by Sage software. Sage returns a linear inequality with the form (a_1, a_2, ..., a_n)x + b >= 0, this linear inequalty will be stored within a single line in Inequalities.txt with the form (a_1  a_2  ... a_n  b). The Inequalities.txt presented here contains all the linear inequalities among the H-Representation of the division trails of PRESENT Sbox with each line representing a single inequality.
* [Reduced_Inequalities.txt] ---This file contains the inequalities chosen by Algorithm 1. There are 11 inequalities for PRESENT Sbox as listed in this file.