import matplotlib.pyplot as plt
import numpy as np
import os

os.chdir("../data/")

"""
import pandas as pd

cali_data = pd.read_csv('cali_new.txt')

mmHg = cali_data[[0]]
V1   = cali_data[[1]]
V2   = cali_data[[2]]

plt.plot(mmHg, V1, 'ro')
plt.plot(mmHg, V2, 'bo')
plt.show()
"""

cali_data = np.genfromtxt('cali_new.txt', delimiter=',', skip_header=1)

mmHg = cali_data[:, 0]
V1   = cali_data[:, 1]
V2   = cali_data[:, 2]

plt.plot(mmHg, V1, 'ro')
plt.plot(mmHg, V2, 'bo')
plt.show()

V3 = V2 / V1

temperature = np.genfromtxt('temperature.txt')

temp_0 = temperature[:, 0]
temp_1 = temperature[:, 1]

plt.plot(temp_1, temp_0, 'g')
plt.show()

run_01 = np.genfromtxt('run_01.txt')
run_02 = np.genfromtxt('run_02.txt')
run_03 = np.genfromtxt('run_03.txt')
run_04 = np.genfromtxt('run_04.txt')

a_run_01 = np.genfromtxt('a_run_01.txt')
a_run_02 = np.genfromtxt('a_run_02.txt')
a_run_03 = np.genfromtxt('a_run_03.txt')
a_run_04 = np.genfromtxt('a_run_04.txt')

def analyzer(data, form='b'):    
    time = data[:, 2]
    volt = data[:, 0]
    
    global_min = time.min()
    global_max = time.max()    
    
    local_min = global_min
    local_max = global_min + 0.485

    max_volts  = []
    
    while local_max <= global_max:
        local_list = []
        for i in time:
            if i >= local_min and i <= local_max:
                ind      = list(time).index(i)
                volt_val = data[ind, 0]
                local_list.append(volt_val)
        
        max_value = max(local_list)
        max_volts.append(max_value)
        
        local_min += 0.485
        local_max += 0.485
    
    plt.plot(volt, time, form)
    plt.title('Title')
    plt.xlabel('Time (s)')
    plt.ylabel('INSERT LABEL (mV)')
    plt.show()
    
    return max_volts
    
analyzer(a_run_02, 'g')