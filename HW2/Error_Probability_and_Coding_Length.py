# John Bumgardner and Nicholas Himes
# ECE 592-061
# HW 2
# Question 2

# Your role is to develop software (Matlab or Python) that selects the optimal model order and
# outputs the overall coding length for both possible model orders. 

import numpy as np
import math

#  t_n = W^T * x_n + noise_n


N=1000 # number of data points
x=np.random.rand(N,1) # where we evaluate function
noise_amp=0.3 # amplitude of Gaussian noise
random_matrix = np.random.randn(N,1)

t=np.cos(2*np.pi*x)+noise_amp*random_matrix # noisy observations

p3 = np.poly1d([1,2,7,9]) #Hypothesis 3: x^3 + 2x^2 + 7x + 9
p4 = np.poly1d([7,0,1,11,2]) #Hypothesis 4: 7x^4 + x^2 + 11x + 2

counter_3 = 0
counter_4 = 0

counter_3 += math.ceil(.5 * math.log2(N))
counter_4 += math.ceil(1.5 * math.log2(N))

hypothesis_3 = []
hypothesis_4 = []

hypothesis_3.append(0)
hypothesis_4.append(1)

print("hypothesis 3: " + str(counter_3))
print("hypothesis 4: " + str(counter_4))

