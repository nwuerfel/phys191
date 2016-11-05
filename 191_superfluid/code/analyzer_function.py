import matplotlib.pyplot as plt
import numpy as np
import os

# Changes working directory to /data to access datasets
os.chdir("../data/")

######################
### BEGIN DATASETS ###
######################
'''
SECOND SOUND
'''
ss_run_01 = np.genfromtxt('ss_run_01.txt')
ss_run_02 = np.genfromtxt('ss_run_02.txt')
ss_run_03 = np.genfromtxt('ss_run_03.txt')
ss_run_04 = np.genfromtxt('ss_run_04.txt')
ss_run_05 = np.genfromtxt('ss_run_05.txt')
ss_run_06 = np.genfromtxt('ss_run_06.txt')
ss_run_07 = np.genfromtxt('ss_run_07.txt')
ss_run_08 = np.genfromtxt('ss_run_08.txt')

'''
HEAT CAPACITY
'''
cali_data = np.genfromtxt('cali_new.txt', delimiter=',', skip_header=1)
temperature = np.genfromtxt('temperature.txt')

drun_01 = np.genfromtxt('run_01.txt')
run_02 = np.genfromtxt('run_02.txt')
run_03 = np.genfromtxt('run_03.txt')
run_04 = np.genfromtxt('run_04.txt')
run_05 = np.genfromtxt('run_05.txt')

a_run_01 = np.genfromtxt('a_run_01.txt')
a_run_02 = np.genfromtxt('a_run_02.txt')
a_run_03 = np.genfromtxt('a_run_03.txt')

"""
# DO NOT USE THESE
a_run_04 = np.genfromtxt('a_run_04.txt')
a_run_05 = np.genfromtxt('a_run_05.txt')
a_run_06 = np.genfromtxt('a_run_06.txt')
a_run_07 = np.genfromtxt('a_run_07.txt')
"""

he_run_01 = np.genfromtxt('he_run_01.txt') 

b_l_a_run_01 = np.genfromtxt('he_below_l_a_run_01.txt')
b_l_a_run_02 = np.genfromtxt('he_below_l_a_run_02.txt')
b_l_run_01   = np.genfromtxt('he_above_l_run_01.txt')

a_l_a_run_01 = np.genfromtxt('he_above_l_a_run_01.txt')
######################
#### END DATASETS ####
######################

#######################
### BEGIN FUNCTIONS ###
#######################
'''
SECOND SOUND
'''
def PTconverter(ls):
    temp = np.array([])
    for i in range(len(ls)):
        np.append(temp, converter(ls[i], 'PT'))

    return temp

'''
HEAT CAPCAITY
'''
def ppFinder(data):
    
    time = data[:, 2]
    volt = data[:, 0] * (1.662 / 0.16754) # This is in mV
    plt.plot(time, volt, 'g')
    plt.title('Title')
    plt.xlabel('Time (s)')
    plt.ylabel('INSERT LABEL (mV)')
    plt.show()

    
    time_list = list(time)
    volt_list = list(volt)
    
    list_length = len(time_list)

    plateau = []
    comparison = 100
    saved_point = 0
    i = 0
    
    while i+1 <= list_length-1:
        y1 = volt_list[i]
        y2 = volt_list[i+1]
            
        working = abs((y1 - y2))
            
        if working <= comparison:
            comparison = working
            saved_point = y2
        
        if working > comparison:
            plateau.append(saved_point)
            comparison = 100
        
        i += 1
            
    plateau = np.array(plateau)
    
    return plateau

def converter(num, con):
    
    if con == 'VP':
        mmHg = cali_data[:, 0]
        V1   = cali_data[:, 1]
    
        maxi_list = []
        mini_list = []
    
        nlist = V1 - num
    
        for i in nlist:
            if i > 0:
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
            if i > 0:
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
        np.append(temp, converter(converter(ls[i], 'VP'), 'PT'))

    return temp

'''
def pulseE(string):
    if string == 'a_run_01':
'''        
#######################
#### END FUNCTIONS ####
#######################

###################
### BEGIN PLOTS ###
###################
'''
SECOND SOUND
'''

'''
HEAT CAPCITY
'''
# Temperature (K) v. Pressure (mTorr)
temp_mTorr = temperature[:, 0]
temp_mmHg  = temp_mTorr / 1000
temp_K     = temperature[:, 1]

plt.plot(temp_mmHg, temp_K, 'g')
plt.show()

# Calibration data plot
mmHg = cali_data[:, 0]
V1   = cali_data[:, 1]
V2   = cali_data[:, 2]

plt.plot(V2, mmHg, 'ro')
plt.show()

#print("The ratio of V2:V1 without taking offset into account is: {} ").format(V2 / V1)

###################
#### END PLOTS ####
###################