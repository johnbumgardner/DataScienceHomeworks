import numpy as np
import matplotlib.pyplot as plt
#-------
# line_search.m
# The following code defines a simple convex function, and 
# then finds the minimum using a crude line search.
# Dror Baron, 11.14.2016
#-------

#-------
# initialize
#-------

def indices(a, func):
    return [i for (i, val) in enumerate(a) if func(val)]

x=np.arange(0.01,10.0002,0.0001)# grid for visualizing signal
f=3*x-np.log(x) # signal values

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(1, 1, 1, aspect=0.25)
ax.plot(x,f)


#-------
# optimize
#-------
xmax=np.max(x)+ 0.9
xmin=np.min(x)

for iter in range(1,11):
   
    grid_here=np.arange(xmin,xmax,(xmax-xmin)/10)
    fhere=3*grid_here-np.log(grid_here) # compute function
    location_min = indices(fhere, lambda n: n == np.min(fhere))# index where f is minimal 
    min_loc = location_min[0]+1
    next_min = np.max((min_loc-2,1)) # compute indices for next iteration
    next_max=np.min((min_loc+2,len(grid_here)))
    xmin=grid_here[next_min-1] # actual edges for next iteration
    xmax=grid_here[next_max-1]
    print ('xmin='+str((xmin+xmax)/2) + ', fmin=' +str(fhere[location_min][0]) + ', interval width=' +str(xmax-xmin) + '\n')
plt.show()
