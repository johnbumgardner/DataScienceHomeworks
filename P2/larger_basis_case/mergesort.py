
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
    global mergesortCalls
    mergesortCalls += 1
    
    if len(x)<2: # x is short --> already sorted --> return it
        y=x
        return y
    
    elif (len(x) == 2): #A larger basis case of length 2
        y=x
        if (y[0] > y[1]): #If the order needs to be swapped...
            y[0], y[1] = y[1], y[0] #Tuple swap the array indexes 

        #If the first index was already less than or = to the second, just return y
        return y
        
    elif (len(x) == 3): #A larger basis case of length 3
        y=x
        if (y[0] > y[2]):
            y[0], y[2] = y[2], y[0] #Swap them
        if (y[0] > y[1]):
            y[0], y[1] = y[1], y[0] 
        if (y[1] > y[2]):
            y[1], y[2] = y[2], y[1]
        return y
            
    else: # x needs to be sorted
        N = len(x)
        y1 = mergesort(x[0:int(N/2)]) #sort first half
        y2 = mergesort(x[int(N/2):N]) # second half
        y=merge.merge(y1,y2)
        return y


# In[ ]:


size_arr = [10, 100, 1000, 10000, 100000, 1000000]
N = 5 # iterations to average

#populate arrays
for i in size_arr:

    sum_of_times = 0
    mergesortCalls = 0
    for h in range(N):
        list = []
        for j in range(i):
            list.append(random.randint(0, 100))
        array = np.array(list)
        start = time.time()
        mergesort(array)
        end = time.time()
        sum_of_times += end - start
    mergesortCalls = round(mergesortCalls / N) #Take average calls amount
    print("size: " + str(len(array)) + " elapsed time to sort: " + str(sum_of_times / N) + ", Mergesort Calls: {}".format(mergesortCalls))
