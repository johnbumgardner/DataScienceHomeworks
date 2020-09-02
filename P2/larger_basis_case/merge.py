
# coding: utf-8

# # The merge.m file has been converted to python
# 
# We are only importing the numpy module in the program.

# In[ ]:


import numpy as np


# this is the modified version of the program to suit python numpy module

# In[ ]:


def merge(x1, x2):
    N1=len(x1)
    N2=len(x2)
    N=N1+N2
    y=np.zeros(N) 
    ind1 = 0
    ind2 = 0 
    for n in range(N):
        if x1[ind1]<x2[ind2]: 
            y[n]=x1[ind1]
            ind1=ind1+1
            if ind1==N1: 
                y[n+1:N]=x2[ind2:N2]
                return y
        else:
            y[n]=x2[ind2]
            ind2=ind2+1
            if ind2==N2: #at end of x2
                y[n+1:N]=x1[ind1:N1]
                return y


# The following is a test output

# In[ ]:


a = np.array([2, 3, 7, 9, 10, 11, 54, 78])
b = np.array([1, 4, 5, 6, 8, 12, 13, 55, 65, 100, 103])
print(merge(a, b))

