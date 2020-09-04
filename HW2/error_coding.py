# John Bumgardner and Nicholas Himes
# ECE 592-061
# HW 2
# Question 2

# Your role is to develop software (Matlab or Python) that selects the optimal model order and
# outputs the overall coding length for both possible model orders. 

def f(noise_n, variance): #This is our noise function that uses the formula from the document
    return (1/ math.sqrt(2*math.pi*variance)) * math.exp(-(noise_n)**2 / (2*variance**2))

import numpy as np
import math
import random
import statistics 

# Part A
p3 = np.poly1d([1,2,7,9]) #Hypothesis 3: x^3 + 2x^2 + 7x + 9
p4 = np.poly1d([7,0,1,11,2]) #Hypothesis 4: 7x^4 + x^2 + 11x + 2
cl3 = 1 #Flag bit to distinguish between H3 or H4
cl4 = 1

# Part B
N = 500 #Number of data points
cl3 += 0.5*p3.order*math.log2(N) #From Rissanen's MDL Theory
cl4 += 0.5*p4.order*math.log2(N)

# Part C
# t_n = W^T * x_n + noise_n

x3 = np.array([])
x4 = np.array([])
for i in range(N):
    x3 = np.append(x3,p3(i))
    x4 = np.append(x4,p4(i))

w3T = np.array([]) #Column vector of weights
w4T = np.array([])
for item in x3:
    w3T = np.append(w3T, item/sum(x3))
for item in x4:
    w4T = np.append(w4T, item/sum(x4))
w3T = w3T.reshape(1, -1) #Now a row vector of weights
w4T = w4T.reshape(1, -1)

var_sum = 0 #Find variance based on the number of N
for noise_n in range(N):
    var_sum += noise_n**2
variance = (1/N) * var_sum
print("Variance: {}".format(variance))

x_n3 = np.array([]) #Create a row vector of length N for X_n based on the random X + noise
for i in range(N):
    x_n3 = np.append(x_n3,x3[i] + f(i,variance))
x_n4 = np.array([]) #Create a row vector of length N for X_n based on the random X + noise
for i in range(N):
    x_n4 = np.append(x_n4,x4[i] + f(i,variance))

# t_n = W^T * x_n + noise_n
# Make a t_n for each Hypothesis since the weights and polys are different
t_n3 = np.array([])
for i in range(N):
    t_n3 = np.append(t_n3, w3T[0][i] * x_n3[i] + f(i,variance))
    
t_n4 = np.array([])
for i in range(N):
    t_n4 = np.append(t_n4, w4T[0][i] * x_n4[i] + f(i,variance))

sum3 = 0 #Need to go through the bins and make a sum of coding length
delta = 0.1 #delta = bin width
for bn in range(0,100):
	bn_dec = bn/100
	sum3 += math.log2(delta * f(delta * bn_dec, variance))
	sum4 = sum3
    
cl3 -= sum3 #The sum was negated in the document, so subtract from the existing coding length
cl4 -= sum4

# Now compare coding lengths and choose the better hypothesis
if (cl3 < cl4):
    print("The coding length of Hypothesis 3 is shorter!")
else:
    print("The coding length of Hypothesis 4 is shorter!")
print("CL3: {}, CL4: {}".format(cl3, cl4))





