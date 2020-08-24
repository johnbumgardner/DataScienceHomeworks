
import random

# consider N bit binary sequence X
N = 500
# generate an unknown theta value to distribute bits
theta = random.uniform(0, 1)

# empty list
binary_sequence = []

# create a binary sequence from given theta
for i in range(0,N):
	val = random.uniform(0,1)
	if(val > theta):
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
		rep_levels_for_instance_k.append((j-.5)/j)
	representation_level_dict[i] = rep_levels_for_instance_k



