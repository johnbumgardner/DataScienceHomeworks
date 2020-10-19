# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 17:11:23 2020

@author: Nicholas Himes
"""
#%% Imports 

import matplotlib.image as mpimg 
import matplotlib.pyplot as plt

from sklearn import cluster
from collections import Counter
import math

#%% Distortion
def distortion(x_orig, x_new, M, N):
    factor = 1 / M * N
    sum = 0
    for i in range(0, M):
        for j in range(0, N):
            sum += (x_orig[i][j] - x_new[i][j])^2

    return factor * sum    


#%% Task 1: Load an Image

img = mpimg.imread('mountain.jpg') 
plt.figure(1)
plt.title("Original Image")
plt.imshow(img) 

plt.figure(2)
plt.title("Subset of Original Image")
subsetImg = img[400:800,400:800] 
plt.imshow(subsetImg)

M = N = len(img) #Its a square image

#%% Task 2: Clustering and Vector Quantization

P = 2 #Initial patch size, so 2x2 = 4 pixels per patch
patches = []
x = 0 #Count up through the patches, highest index will be M-1 = N-1
y = 0
while ((x < M) and (y < M)):
    partition = img[x:x+P, y:y+P]
    patches.append(partition)
    
    x += P
    if (x >= M):
        x = 0
        y += P
        
#Now cluster the patches
R = 1 #Rate is 1
C = 2**(R*(P**2))

#These next 6 lines take about 3 minutes to run since the picture is large
x, y, z = img.shape
img2D = img.reshape(x*y, z)
kmeansCluster = cluster.KMeans(n_clusters = C)
kmeansCluster.fit(img2D)
clusterCenters = kmeansCluster.cluster_centers_
clusterLabels = kmeansCluster.labels_

plt.figure(3)
plt.title("Image after Clustering")
clusteredImg = clusterCenters[clusterLabels].reshape(x,y,z).astype('uint8')
plt.imshow(clusteredImg)

plt.figure(4)
plt.subplot(1, 2, 1)
plt.title("Part of Original Image")
plt.imshow(img[500:700, 500:700])

plt.subplot(1, 2, 2)
plt.title("Part of Quantized Image")
plt.imshow(clusteredImg[500:700, 500:700])


#%% Task 3 - Rate vs. Distortion
#range of coding rates
P = 2 #Initial patch size, so 2x2 = 4 pixels per patch
patches = []
x = 0 #Count up through the patches, highest index will be M-1 = N-1
y = 0
while ((x < M) and (y < M)):
    partition = img[x:x+P, y:y+P]
    patches.append(partition)
    
    x += P
    if (x >= M):
        x = 0
        y += P

R_list = [0.2, 0.4, 0.6, 0.8, 1.0]
D_list = []
C_list = []
for i in R_list:
    new_C = round(2**(i*(P**2)))
    C_list.append(new_C)
    x, y, z = img.shape
    img2D = img.reshape(x*y, z)
    kmeansCluster = cluster.KMeans(n_clusters = new_C)
    kmeansCluster.fit(img2D)
    clusterCenters = kmeansCluster.cluster_centers_
    clusterLabels = kmeansCluster.labels_

    clusteredImg = clusterCenters[clusterLabels].reshape(x,y,z).astype('uint8')
    D_list.append(distortion(img, clusteredImg, M, N))

# Plot rate vs distortion
plt.figure(5)
plt.title("Rate vs Distortion Task 3")
plt.xlabel("Rate")
plt.ylabel("Distortion")
plt.plot(R_list, D_list)


#%% Task 4 - Patch Size
P_set = [2 ,4 ,8] #Initial patch size, so 2x2 = 4 pixels per patch

for P in P_set:
    patches = []
    x = 0 #Count up through the patches, highest index will be M-1 = N-1
    y = 0
    while ((x < M) and (y < M)):
        partition = img[x:x+P, y:y+P]
        patches.append(partition)
    
        x += P
        if (x >= M):
            x = 0
            y += P
    
    R_list = [0.2, 0.4, 0.6, 0.8, 1.0]
    D_list = []
    C_list = []
    for i in R_list:
        new_C = round(2**(i*(P**2)))
        C_list.append(new_C)
        x, y, z = img.shape
        img2D = img.reshape(x*y, z)
        kmeansCluster = cluster.KMeans(n_clusters = new_C)
        kmeansCluster.fit(img2D)
        clusterCenters = kmeansCluster.cluster_centers_
        clusterLabels = kmeansCluster.labels_
    
        clusteredImg = clusterCenters[clusterLabels].reshape(x,y,z).astype('uint8')
        D_list.append(distortion(img, clusteredImg, M, N))
        
    plt.figure()
    plt.title("Rate vs Distortion Task 4, P = {}".format(P))
    plt.xlabel("Rate")
    plt.ylabel("Distortion")
    plt.plot(R_list, D_list)


#%% Task 5 - Better Compression
clusterUseCount = Counter(clusterLabels)

# For the task 2 example...
probs = []
for i in range(C):
    tempProb = clusterUseCount[i] / (M*N / (P**2))
    tempProb /= (P**2) #Divide by P^2 since the clusterUseCount counted every pixel instead of patches
    probs.append(tempProb)
    
tempH = 0 
for p in probs:
    tempH += p * math.log2(p)
H = -tempH #Entropy equation!

R = H / (P**2)
print("R using the Task 2 Example is {}".format(R))