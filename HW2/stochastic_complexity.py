# John Bumgardner and Nicholas Himes
# ECE 592-061
# HW 2

import random
import math
import matplotlib.pyplot as plt 

def closest(lst, K):    
    return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))] 

def get_string(N, theta):
    binary_sequence = []

    # create a binary sequence from given theta
    for i in range(0,N):
        val = random.uniform(0,1)
        if(val < theta):
            binary_sequence.append(1)
        else:
            binary_sequence.append(0)

    return binary_sequence

def get_empirical_theta(binary_sequence):
    # theta is technically unknown
    # count number of ones and zeroes
    numberDigits = [0,0]
    for i in binary_sequence:
        if(i == 0):
            numberDigits[0] += 1
        else:
            numberDigits[1] += 1
    return 1.0*numberDigits[1] / (numberDigits[1] + numberDigits[0])

def get_rep_level(estimated_theta, num_bins):
    step_size = 1 / num_bins
    val_low = 0
    val_high = step_size
    for i in range(num_bins):
        if estimated_theta > val_low and estimated_theta < val_high:
            return (i + .5) / num_bins
        val_low += step_size
        val_high += step_size

def get_ones(binary_sequence):
    num_ones = 0
    for i in binary_sequence:
        if i == 1:
            num_ones += 1
    return num_ones

def get_zeros(binary_sequence):
    num_zeros = 0
    for i in binary_sequence:
        if i == 0:
            num_zeros += 1
    return num_zeros

def get_total_length(K, rep_level, binary_sequence):
    val = math.log2(K)
    val -= get_zeros(binary_sequence) * math.log2(1-rep_level)
    val -= get_ones(binary_sequence) * math.log2(rep_level)
    return val

def get_true_entropy(theta):
    return -theta * math.log2(theta) - (1-theta)*math.log2(1-theta)

def get_redundancy(expiriment, theory, N):
    return expiriment - N*theory

def main():
    size = 1000
    optimal = math.sqrt(size)
    k_list = []
    redundancy_list = []
    for i in range(1,10):
        theta = i / 10.0
        string = get_string(size, theta) #Makes sequence from theta of size N
        estimated_theta = get_empirical_theta(string)
        K = 1
        while(K < size):
            k_list.append(K)
            r_k = get_rep_level(estimated_theta, K)
            true_ent = get_true_entropy(theta)
            measured_ent = get_total_length(K, r_k, string)
            redundancy = get_redundancy(measured_ent, true_ent, size)
            redundancy_list.append(redundancy)
            #print("theta = " + str(theta) + " | K = " + str(K) + " | redundancy = " + str(redundancy))
            K += 1

        ymin = min(redundancy_list)
        xpos = redundancy_list.index(ymin)
        xmin = k_list[xpos]
        plt.annotate('local min', xy=(xmin, ymin), xytext=(xmin, ymin+5),
            arrowprops=dict(facecolor='black', shrink=0.01),
            )
        plt.plot(k_list, redundancy_list)
        plt.xlabel('K values')
        plt.ylabel('Redundancy')
        plt.title('Theta = ' + str(theta) + ' Theoretical optimal = ' + str(optimal))
        plt.show()
        
        #When K is close to sqrt(N), the redundancy R will be close to 0.5log2(N)
        theoretical_redundancy = 0.5*math.log2(size)
        closestK = min(k_list, key=lambda x:abs(x-optimal))
        actual_redundancy = redundancy_list[k_list.index(closestK)] #If we want K=32, use index 31 in redundancy list since K starts at 1
        print("Theta: {}, Theoretical R: {}, Actual R: {}".format(theta, theoretical_redundancy, actual_redundancy))
    
        k_list.clear()
        redundancy_list.clear()
main()

