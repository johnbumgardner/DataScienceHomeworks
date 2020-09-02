
# coding: utf-8

# # The Mergesort.m file in python
# 
# Here we are only importing the numpy module

# In[ ]:


import numpy as np
import merge
import time
import random

# In[ ]:


def mergesort(x):

    if len(x)<2: # x is short --> already sorted --> return it
        y=x
        return y
    
    
    else: # x needs to be sorted
        N = len(x)
        y1 = mergesort(x[0:int(N/2)]) #sort first half
        y2 = mergesort(x[int(N/2):N]) # second half
        y=merge.merge(y1,y2)
        return y


# In[ ]:


size_arr = [10, 100, 1000, 10000, 100000, 1000000]
N = 10 # iterations to average

#populate arrays
for i in size_arr:
    sum_of_times = 0
    for h in range(N):
        list = []
        for j in range(i):
            list.append(random.randint(0, 100))
        array = np.array(list)
        start = time.time()
        mergesort(array)
        end = time.time()
        sum_of_times += end - start
    print("size: " + str(len(array)) + " elapsed time to sort: " + str(sum_of_times / N))

