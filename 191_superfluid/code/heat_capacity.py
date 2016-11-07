import matplotlib.pyplot as plt
import numpy as np
import os

# Changes working directory to /data to access datasets
os.chdir("../data/")

cali_data = np.genfromtxt('cali_new.txt', delimiter=',', skip_header=1)
temperature = np.genfromtxt('temperature.txt')

a_run_02_plateaus = np.genfromtxt('a_run_02_plateaus.txt')

true_plateaus = a_run_02_plateaus[:142, 0] * (1.662 / 0.16754)

a_run_02 = np.genfromtxt('a_run_02.txt')

def converter(num, con):
    
    if con == 'VP':
        mmHg = cali_data[:, 0]
        V1   = cali_data[:, 1]
    
        maxi_list = []
        mini_list = []
    
        nlist = V1 - num
    
        for i in nlist:
            if i >= 0:
                maxi_list.append(i)
            else:
                mini_list.append(i)
    
        V_max = min(maxi_list) + num
        V_min = max(mini_list) + num
    
        V1_list = list(V1)
    
        P_max = mmHg[V1_list.index(V_max)]
        P_min = mmHg[V1_list.index(V_min)]
    
        slope = (P_max - P_min) / (V_max - V_min)
    
        return P_min + slope * (num - V_min)

    if con == 'PT':
        temp_mTorr = temperature[:, 0]
        temp_mmHg  = temp_mTorr / 1000
        temp_K     = temperature[:, 1]
    
        maxi_list = []
        mini_list = []
    
        nlist = temp_mmHg - num
    
        for i in nlist:
            if i >= 0:
                maxi_list.append(i)
            else:
                mini_list.append(i)
    
        P_max = min(maxi_list) + num
        P_min = max(mini_list) + num
    
        temp_mmHg_list = list(temp_mmHg)
    
        K_max = temp_K[temp_mmHg_list.index(P_max)]
        K_min = temp_K[temp_mmHg_list.index(P_min)]
    
        slope = (K_max - K_min) / (P_max - P_min)
    
        return K_min + slope * (num - P_min)

def list_converter(ls):
    temp = np.array([])
    for i in range(len(ls)):
        temp = np.append(temp, converter(converter(ls[i], 'VP'), 'PT'))

    return temp
    
def pulseE(string):
    
    R = 0.945 * (10 ** 3)
    
    if string == 'a_run_01':
        L = 310 * (10 ** -6)
        V = 10
    if string == 'a_run_02':
        L = 703 * (10 ** -6)
        V = 5
    if string == 'a_run_03':
        L = 3.22 * (10 ** -6)
        V = 5
        
    return (V ** 2) * L / R
    
def Heat(ls, x):

    C  = np.array([])
    dE = pulseE(x)
    dT = np.array([])
    
    list_length = len(ls)    
    
    i = 0
    
    while i+1 <= list_length-1:
        dt = (ls[i+1] + ls[i]) / 2
        c  = dE / (ls[i+1] - ls[i])
        
        C  = np.append(C, c)
        dT = np.append(dT, dt)
        
        i += 1
    
    plt.plot(dT, C, 'bo')
    plt.show()
    
    return np.array([dT, C])

Heat(list_converter(true_plateaus), 'a_run_02')