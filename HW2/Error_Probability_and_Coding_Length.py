# John Bumgardner and Nicholas Himes
# ECE 592-061
# HW 2
# Question 2

# Your role is to develop software (Matlab or Python) that selects the optimal model order and
# outputs the overall coding length for both possible model orders. 

import numpy as np

#  t_n = W^T * x_n + noise_n

p3 = np.poly1d([1,2,7,9]) #Hypothesis 3: x^3 + 2x^2 + 7x + 9
p4 = np.poly1d([7,0,1,11,2]) #Hypothesis 4: 7x^4 + x^2 + 11x + 2
CL3 = 1 #Flag bit to distinguish between H3 or H4
CL4 = 1

