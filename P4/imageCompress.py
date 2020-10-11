# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 17:11:23 2020

@author: Nicholas Himes
"""
#%% Imports 

import matplotlib.image as mpimg 
import matplotlib.pyplot as plt
import numpy as np

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
clusters = np.split(np.array(patches), C)
