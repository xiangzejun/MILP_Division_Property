### Algorithm 1

This folder implementes the algorithm to select a set of linear inequalities from the H-Representation of a set of points, which corresponds to the Algorithm 1 presented in the paper. 
* [cipher_Inequalities.txt] ---This txt file contains the H-Representation of a given set of points, which is actually a set of linear inequalities returned by Sage software. Sage returns a linear inequality with the form $$$(a_1, a_2, ..., a_n)\cdot x^{T} + b >= 0$$$, this linear inequalty will be stored within a single line in cipher_Inequalities.txt with the form $$$(a_1, a_2, \cdots, a_n, b)$$$. The cipher_Inequalities.txt presented here contains all the linear inequalities among the H-Representation of the division trails of PRESENT Sbox with each line representing a single inequality.
* [cipher_Reduced_Inequalities.txt] ---This file contains the inequalities chosen by Algorithm 1. There are 10 inequalities for PRESENT Sbox as listed in this file.

####NOTE
PRESENT_Reduced_Inequality.txt contains 10 linear inequalities which are the linear description of division property propagations of PRESENT sbox. However, in our paper "Applying MILP Method to Searching Integral Distinguishers based on Division Property for 6 Lightweight Block Ciphers", we presented 11 linear inequalites to describe the division property propagation for PRESENT Sbox. And the difference comes from the different implementations of Algorithm 1.

We implemented Algorithm 1 in C++ in an earlier version, and we destroyed the original order of the linear inequalities returned by Sage software. In this version we implemented Algorithm 1 in Python and we keep the original order, thus, the number of linear inequalites returned is a little less. However, this does not influence the results of the paper.