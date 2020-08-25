# John Bumgardner and Nicholas Himes
# ECE 592-061
# HW 2

import random
import numpy as np
import math
from matplotlib.pyplot import matshow
import matplotlib.pyplot as plt

def closest(lst, K):    
    return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))] 
      
def get_redundancy(theta):
	# consider N bit binary sequence X
	N = 500

	# empty list
	binary_sequence = []

	# create a binary sequence from given theta
	for i in range(0,N):
		val = random.uniform(0,1)
		if(val < theta):
			binary_sequence.append(1)
		else:
			binary_sequence.append(0)

	# theta is technically unknown
	# count number of ones and zeroes
	numberDigits = [0,0]
	for i in binary_sequence:
		if(i == 0):
			numberDigits[0] += 1
		else:
			numberDigits[1] += 1

	# define number of bins to be from 1 to N
	K = []
	for i in range(1,N+1):
		K.append(i)

	# generate representation levels 1-N defined
	representation_level_dict = dict()
	for i in K:
		rep_levels_for_instance_k = []
		for j in range(1,i+1):
			rep_levels_for_instance_k.append((j-.5)/i)
		representation_level_dict[i] = rep_levels_for_instance_k
   
	# find nearest representation level
	r_k = []
	to_find = numberDigits[1] / N
	for i in representation_level_dict:
		r_k.append(closest(representation_level_dict[i],to_find))

	




	# show what range of values for K makes sense
	# plot redundancy R(X,theta) 

	# horizontal axis is theta from 0->1
	# hstep = 0.01 #CHANGE LATER 
	# horizontalAxis = np.arange(0,1+hstep,hstep)

	# vertical axis varies number of bins K from 1 to N
	# vstep = 1
	# verticalAxis = np.arange(1,N+vstep,vstep)

	#r_k = 1 # NEED TO IMPLEMENT
	current_level = 0
	redundancy = []
	for r in r_k:
		value = math.log2(K[current_level])
		value += N*(1-theta)*math.log2((1-theta)/(1-r))
		value += N*theta*math.log2(theta/r)
		redundancy.append(value)
		current_level = current_level + 1                 

	return redundancy



def main():

	#go thru some theta values
	thetas = []
	for i in range(1,100):
		thetas.append(i/100)

	redundancy_matrix = []
	for i in thetas:
		redundancy_matrix.append(get_redundancy(i))

	arr = np.array(redundancy_matrix)

	plt.matshow(arr)
	plt.show()



main()

