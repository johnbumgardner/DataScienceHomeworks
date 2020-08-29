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

def get_string(N, theta):
	binary_sequence = []

	# create a binary sequence from given theta
	for i in range(0,N):
		val = random.uniform(0,1)
		if(val < theta):
			binary_sequence.append(1)
		else:
			binary_sequence.append(0)

	return binary_sequence

def get_empirical_theta(binary_sequence):
	# theta is technically unknown
	# count number of ones and zeroes
	numberDigits = [0,0]
	for i in binary_sequence:
		if(i == 0):
			numberDigits[0] += 1
		else:
			numberDigits[1] += 1
	return 1.0*numberDigits[1] / (numberDigits[1] + numberDigits[0])

def get_rep_level(estimated_theta, num_bins):
	step_size = 1 / num_bins
	val_low = 0
	val_high = step_size
	for i in range(num_bins):
		if estimated_theta > val_low and estimated_theta < val_high:
			return (i + .5) / num_bins
		val_low += step_size
		val_high += step_size

def get_ones(binary_sequence):
	num_ones = 0
	for i in binary_sequence:
		if i == 1:
			num_ones += 1
	return num_ones

def get_zeros(binary_sequence):
	num_zeros = 0
	for i in binary_sequence:
		if i == 0:
			num_zeros += 1
	return num_zeros

def get_total_length(K, rep_level, binary_sequence):
	val = math.log2(K)
	val -= get_zeros(binary_sequence) * math.log2(1-rep_level)
	val -= get_ones(binary_sequence) * math.log2(rep_level)
	return val

def get_true_entropy(theta):
	return -theta * math.log2(theta) - (1-theta)*math.log2(1-theta)

def get_redundancy(expiriment, theory):
	return expiriment - theory

def main():
	size = 100
	for i in range(1,10):
		theta = i / 10.0
		string = get_string(size, theta)
		estimated_theta = get_empirical_theta(string)
		K = 1
		while(K < size):
			r_k = get_rep_level(estimated_theta, K)
			true_ent = get_true_entropy(theta)
			measured_ent = get_total_length(K, r_k, string)
			redundancy = get_redundancy(measured_ent, true_ent)
			print("theta = " + str(theta) + " | K = " + str(K) + " | redundancy = " + str(redundancy))
			K += 10



main()

