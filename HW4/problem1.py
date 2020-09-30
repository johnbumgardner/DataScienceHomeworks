# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 16:39:33 2020

@author: Nicholas Himes
"""

import itertools
import matplotlib.pyplot as plt
import time

def logs(n):
    p = [1,3,5,6,11] #Prices
    Psi = [] #Psi list
    
    #Fill the Psi list
    for k in range(1,n+1): #1 -> n
        if (k==1):
            Psi.append(p[k-1]) #Append p1 = p[0]
        else:
            #Find all combos
            combos = [x for x in itertools.combinations_with_replacement(range(1,k+1), 2) if (sum(x)==k)]
            #print([i for i in combos])
            if (k > len(p)):
                tempMax = 0 #If k=6, there are only 5 prices so start max at 0
            else:
                tempMax = p[k-1] #If k was 5, this returns p5 = [4]
            
            for combo in combos:
                tempMax = max(tempMax, Psi[combo[0]-1] + Psi[combo[1]-1])
            
            Psi.append(tempMax)
        
    #print("Psi List: {}".format(Psi))
    print("Highest Price for n={} is {}".format(n, Psi[n-1]))
    print()
    

test_n = [5, 96, 100]
for n in test_n:
    logs(n)
    

runTime = []
for n in range(1,500,5):
    start = time.time()
    logs(n)
    runTime.append(time.time() - start)
    
plt.figure()
plt.xlabel("n")
plt.ylabel("Time (s)")
plt.title("Runtime")
plt.plot(range(1,500,5), runTime)
    