#-------
# classification.m
# This script goes through examples in Hastie et al.'s book.
# Binary classification is performed in two ways: linear regression
# and nearest neighbors
# Jordan Miller, 09.07.2018
#-------

import numpy as np
from matplotlib import pyplot as plt

#-------
# parameters
#-------
num_clusters=5 # number of components (clusters) in mixture model
N=200 # total number of samples of training data
step=0.1
grid=np.arange(-3,3+step,step) # test data grid for each dimension
num_neighbors=5 # number of neighbors used in nearest neighbors

#-------
# mixture models
#-------
Gmean=np.random.randn(2,num_clusters) # locations of centers of clusters for green class
Rmean=np.random.randn(2,num_clusters) # -"- red class

#-------
# training data
#-------
samples=np.zeros((2,N)) # locations of samples in 2 dimensions
class_samples=np.zeros((N,1)) # class of each one (green or red)
cluster_variance=0.1 # variance of each cluster around its mean
for n in range(1,int(N/2)):
    Gcluster=int(np.ceil(np.random.rand(1)*num_clusters)) # select green cluster
    Rcluster=int(np.ceil(np.random.rand(1)*num_clusters)) # -"- red
    samples[:,n]=Gmean[:,Gcluster-1]+np.sqrt(cluster_variance)*np.random.randn(2) # generate green sample
    samples[:,int(n+N/2)]=Rmean[:,Rcluster-1]+np.sqrt(cluster_variance)*np.random.randn(2) # -"- red
    class_samples[n]=1 # green
    class_samples[int(n+N/2)]=0 # red

#-------
# test data - basically a 2-D grid
#-------
test_samples=np.zeros((2,np.size(grid)**2)) # locations of test samples
for n1 in range(1,np.size(grid)):
    for n2 in range(1,np.size(grid)):
        test_samples[0,int(n1+np.size(grid)*(n2-1))]=grid[n1] # first coordinate
        test_samples[1,int(n1+np.size(grid)*(n2-1))]=grid[n2] # second 

#------- 
# run classifiers on test grid
#-------
# linear model
#-------
beta,_,_,_ = np.linalg.lstsq(class_samples,np.transpose(samples)) # compute coefficients of least squares
beta=np.reshape(beta, (2,))
test_linear=(np.dot(beta,test_samples)>0.5)

#-------
# nearest neighbors 
#-------
test_NN=np.zeros((np.size(grid)**2,1)) # classification results on test data
for n1 in range(0,np.size(grid)-1):
    for n2 in range (0,np.size(grid)-1):
        distances=(grid[n1]-samples[0,:])**2+(grid[n2]-samples[1,:])**2 # distances to training samples
        distances_sort = np.sort(distances)
        distances_index = np.argsort(distances)
        neighbors=distances_index[0:num_neighbors]
        class_predicted=((np.sum(class_samples[neighbors-1])/num_neighbors)>0.5) # NN classifier
        test_NN[n1+np.size(grid)*(n2-1)-1]=class_predicted # store classification


#-------
# show data
#-------
## identify location indices (in test grid) that are red and green
r_locations=np.argwhere(np.logical_not(test_linear))
g_locations=np.argwhere(test_linear)

# linear classification plot
plt.figure()
plt.title("Linear Classification")
plt.subplot(111)
plt.plot(samples[0,1:int(N/2)],samples[1,1:int(N/2)],'b*', # green training samples
    samples[0,int(N/2+1):N],samples[1,int(N/2+1):N],'ro', # red training 
    test_samples[0,g_locations],test_samples[1,g_locations],'b.', # green test
    test_samples[0,r_locations],test_samples[1,r_locations],'r.') # red
  
plt.xlim=(-3,3) # boundaries for figure aligned with grid
plt.ylim=(-3,3)


# identify location indices (in test grid) that are red and green
r_locations=np.argwhere(np.logical_not(test_NN))
g_locations=np.argwhere(test_NN)

# NN plot
plt.figure()
plt.title("Q1 Nearest Neighbors Classification, K={}".format(num_neighbors))
plt.subplot(111)
plt.plot(samples[0,1:int(N/2-1)],samples[1,1:int(N/2-1)],'b*', # green training samples
    samples[0,int(N/2):N-1],samples[1,int(N/2):N-1],'ro', # red training 
    test_samples[0,g_locations-1],test_samples[1,g_locations-1],'b.', # green test
    test_samples[0,r_locations-1],test_samples[1,r_locations-1],'r.') # red
   
plt.xlim=(-3,3) # boundaries for figure aligned with grid
plt.ylim=(-3,3)


#%% Question 2
# Code to implement NN such that the nearest neighbor receives weight (K)/[K(K+1)/2], 
# the second nearest weight (K-1)/[K(K+1)/2], down to the K’th nearest neighbor whose weight is (1)/[K(K+1)/2]:
    
#-------
# nearest neighbors 
#-------
test_NN=np.zeros((np.size(grid)**2,1)) # classification results on test data
for n1 in range(0,np.size(grid)-1):
    for n2 in range (0,np.size(grid)-1):
        distances=(grid[n1]-samples[0,:])**2+(grid[n2]-samples[1,:])**2 # distances to training samples
        distances_sort = np.sort(distances)
        distances_index = np.argsort(distances)
        neighbors=distances_index[0:num_neighbors]
        #class_predicted=((np.sum(class_samples[neighbors-1])/num_neighbors)>0.5) # NN classifier
        tempK = num_neighbors
        allPredictions = [] #Add each neighbors weight to this list
        allWeights = [] #Add each K weight to this
        while tempK > 0:
            tempWeight = tempK / (num_neighbors*(num_neighbors+1)/2)
            allWeights.append(tempWeight)
            tempK -= 1

        for i in range(len(allWeights)):
            allPredictions.append(allWeights[i] * class_samples[neighbors-1][i])
        class_predicted = ((np.sum(allPredictions)) > 0.5)
        
        test_NN[n1+np.size(grid)*(n2-1)-1]=class_predicted # store classification


# identify location indices (in test grid) that are red and green
r_locations=np.argwhere(np.logical_not(test_NN))
g_locations=np.argwhere(test_NN)

# NN plot
plt.figure()
plt.title("Q2 Nearest Neighbors Classification, K={}".format(num_neighbors))
plt.subplot(111)
plt.plot(samples[0,1:int(N/2-1)],samples[1,1:int(N/2-1)],'b*', # green training samples
    samples[0,int(N/2):N-1],samples[1,int(N/2):N-1],'ro', # red training 
    test_samples[0,g_locations-1],test_samples[1,g_locations-1],'b.', # green test
    test_samples[0,r_locations-1],test_samples[1,r_locations-1],'r.') # red
   
plt.xlim=(-3,3) # boundaries for figure aligned with grid
plt.ylim=(-3,3)