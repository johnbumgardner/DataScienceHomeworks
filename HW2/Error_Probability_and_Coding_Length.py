# John Bumgardner and Nicholas Himes
# ECE 592-061
# HW 2
# Question 2

# Your role is to develop software (Matlab or Python) that selects the optimal model order and
# outputs the overall coding length for both possible model orders. 

def f(noise_n, variance):
    return (1/ math.sqrt(2*math.pi*variance)) * math.exp(-(noise_n)**2 / (2*variance**2))

import numpy as np
import math

# Part A
p3 = np.poly1d([1,2,7,9]) #Hypothesis 3: x^3 + 2x^2 + 7x + 9
p4 = np.poly1d([7,0,1,11,2]) #Hypothesis 4: 7x^4 + x^2 + 11x + 2
cl3 = 1 #Flag bit to distinguish between H3 or H4
cl4 = 1

# Part B
N = 1000 #Number of data points
cl3 += 1.5*math.log2(N) #From Rissanen's MDL Theory
cl4 += 2*math.log2(N)

# Part C
#  t_n = W^T * x_n + noise_n
wT = np.random.rand(N,1).transpose() #Column vector of weights
x = np.random.rand(N,1) #Input variables - given

variance = 100 #Fix

x_n = np.array([])
for i in range(N):
    x_n = np.append(x_n,x[i] + f(i,variance))

#delta = bin width
#Pb = delta * f(delta * b), where f is the noise function?

#t_n = wT * x_n + noise_n dont even need to implement?

sum3 = 0
delta = 1
for bn in range(N):
    sum3 += math.log2(delta * f(delta * bn, variance))
    sum4 = sum3 #?????? Are both polys the same code length in part c?
    
#cl3 -= sum3
#cl4 -= sum4

# Now compare coding lengths and choose the better hypothesis
if (cl3 < cl4):
    print("The coding length of Hypothesis 3 is shorter!")
else:
    print("The coding length of Hypothesis 4 is shorter!")
print("CL3: {}, CL4: {}".format(cl3, cl4))






