
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

