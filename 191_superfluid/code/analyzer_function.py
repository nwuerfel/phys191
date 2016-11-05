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

run_01 = np.genfromtxt('run_01.txt')
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


'''
HEAT CAPCAITY
'''
def ppFinder(data):
    
    time = data[:, 2]
    volt = data[:, 0]
    

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
    
    return plateau

def VPconverter(num):

def PTconverter(num):
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
    
    return P_min + slope * (num - P_min)
    
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
'''
# Calibration data plot
mmHg = cali_data[:, 0]
V1   = cali_data[:, 1]
V2   = cali_data[:, 2]

plt.plot(mmHg, V1, 'ro')
plt.plot(mmHg, V2, 'bo')
plt.show()

#print("The ratio of V2:V1 without taking offset into account is: {} ").format(V2 / V1)
'''
###################
#### END PLOTS ####
###################

'''
'''
'''
JUNK
'''
'''
'''

def analyzer(data, form='b'):    
    
    gamma = 0.1 # inital offset
    delta = 0.485
    
    time = data[:, 2]
    volt = data[:, 0]
  
    global_min = time.min()
    global_max = time.max()    
    
    local_min = global_min + gamma
    local_max = local_min + delta

    max_volts  = []
    
#    plt.axvline(local_min)
    while local_max <= global_max:
        local_list = []
        for i in time:
            if i >= local_min and i <= local_max:
                ind      = list(time).index(i)
                volt_val = data[ind, 0]
                local_list.append(volt_val)
        
        max_value = max(local_list)
        max_volts.append(max_value)
        
#        plt.axvline(local_max)
        local_min += delta
        local_max += delta

    plt.plot(time, volt, form)
    plt.title('Title')
    plt.xlabel('Time (s)')
    plt.ylabel('INSERT LABEL (mV)')
    plt.show()