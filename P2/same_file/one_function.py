import numpy as np
import time
import random

def mergesort(x):
    if len(x)<2: # x is short --> already sorted --> return it
        y=x
        return y
    else: # x needs to be sorted
        N = len(x)
        y1 = mergesort(x[0:int(N/2)]) #sort first half
        y2 = mergesort(x[int(N/2):N]) # second half
        # y=merge(y1,y2) # replace with inline merge

        #### In-line merge #####
        N1=len(y1)
        N2=len(y2)
        N=N1+N2
        y=np.zeros(N) 
        ind1 = 0
        ind2 = 0 
        for n in range(N):
            if y1[ind1]<y2[ind2]: 
            	y[n]=y1[ind1]
            	ind1=ind1+1
            	if ind1==N1:
            		y[n+1:N]=y2[ind2:N2]
            		break
            else: 
            	y[n]=y2[ind2]
            	ind2=ind2+1
            	if ind2==N2: #at end of x2
            		y[n+1:N]=y1[ind1:N1]
            		break
        return y




size_arr = [10, 100, 1000, 10000, 100000, 1000000]

#populate arrays
for i in size_arr:
    list = []
    for j in range(i):
        list.append(random.randint(0, 100))
    array = np.array(list)
    start = time.time()
    mergesort(array)
    end = time.time()
    print("size: " + str(len(array)) + " elapsed time to sort: " + str(end - start))
