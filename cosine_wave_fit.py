from numpy.linalg import inv
import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.metrics import r2_score

#-------
# curve_fitting.m
# This file shows how to perform polynomial curve fitting.
# Based on example in Section 1.1 in Bishop.
# Dror Baron, 8.24.2016
#-------


#-------
# generate signals
#-------
N=1000 # number of data points
x=np.random.rand(N,1) # where we evaluate function
noise_amp=0.5 # amplitude of Gaussian noise
random_matrix = np.random.randn(N,1)

t=np.cos(2*np.pi*x)+noise_amp*random_matrix # noisy observations

xbackup = x  # Make backups for later R2 testing
tbackup = t
#-------
# curve fitting
#-------
M=5 # maximal polynomial order
X=np.matrix(np.zeros((N,M)))

for m in range(M):
    X[:,m]= np.power(x,m)
Xpseudo=inv(X.transpose()*X)*X.transpose();
what=Xpseudo*t
#---------
# graphics
#---------

xplot = np.arange(0,1.00,1.0/N)
tplot=np.cos(2*np.pi*xplot)
X2=np.zeros((len(xplot),M))
for m in range(M):
    X2[:,m]=np.power(xplot,m)
            
tpred=X2*what
x = np.asarray(x)

t = np.asarray(t)

xplot = np.asarray(xplot)
tplot = np.asarray(tplot)
tpred = np.asarray(tpred)
print("MSE: " + str(metrics.mean_squared_error(tpred, tplot)))
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(1, 1, 1, aspect=0.25)
ax.plot(x, t, linewidth=0,
        marker='o', markerfacecolor='w', markeredgecolor='k', label="observations")
ax.plot(xplot, tpred, c=(1.0, 0.1, 0.1), lw=2, label="truth")
ax.plot(xplot, tplot, c=(0.1, 0.1, 1.00), lw=2, label="polynomial", zorder=10)
ax.legend()
plt.show()

# Creating an 80/20 training/test split
train_x = np.ndarray.flatten(xbackup[:800])
train_y = np.ndarray.flatten(tbackup[:800])
test_x = np.ndarray.flatten(xbackup[800:])
test_y = np.ndarray.flatten(tbackup[800:])
# plt.scatter(train_x, train_y)
# plt.show()
# plt.scatter(test_x, test_y)
# plt.show()

polyModel = np.poly1d(np.polyfit(train_x, train_y, 4)) #Create a model to predict observations

train_r2 = r2_score(train_y, polyModel(train_x)) #0 means no relationship, 1 means completely related
test_r2 = r2_score(test_y, polyModel(test_x))
print("Train R2: {}".format(train_r2))
print("Test R2: {}".format(test_r2))
