import matplotlib.pyplot as plt
import numpy as np
import os

# Changes working directory to /data to access datasets
os.chdir("../data/")

# Datasets
cali_data = np.genfromtxt('cali_new.txt', delimiter=',', skip_header=1)
temperature = np.genfromtxt('temperature.txt')

run_01 = np.genfromtxt('run_01.txt')
run_02 = np.genfromtxt('run_02.txt')
run_03 = np.genfromtxt('run_03.txt')
run_04 = np.genfromtxt('run_04.txt')

a_run_01 = np.genfromtxt('a_run_01.txt')
a_run_02 = np.genfromtxt('a_run_02.txt')
a_run_03 = np.genfromtxt('a_run_03.txt')
a_run_04 = np.genfromtxt('a_run_04.txt')

# Temperature (K) v. Pressure (mTorr) plot
temp_0 = temperature[:, 0]
temp_1 = temperature[:, 1]

plt.plot(temp_1, temp_0, 'g')
plt.show()

# Calibration data plot
mmHg = cali_data[:, 0]
V1   = cali_data[:, 1]
V2   = cali_data[:, 2]

plt.plot(mmHg, V1, 'ro')
plt.plot(mmHg, V2, 'bo')
plt.show()

#print("The ratio of V2:V1 without taking offset into account is: {} ").format(V2 / V1)

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

def edgefinder(data):
    
    time = data[:25, 2]
    volt = data[:25, 0]

    plt.plot(time, volt, 'go')
    plt.title('Title')
    plt.xlabel('Time (s)')
    plt.ylabel('INSERT LABEL (mV)')
    plt.show()
    
    time_list = list(time)
    volt_list = list(volt)
    volt_list.reverse()
    
    list_length = len(time_list)

    edge = []
    comparison = 0
    saved_point = 0
    i = 0
    
    while i+1 <= list_length-1:
        y1 = volt_list[i]
        y2 = volt_list[i+1]
            
        working = abs((y1 - y2))
            
        if working >= comparison:
            comparison = working
            saved_point = y2
        
        if working < comparison:
            edge.append(saved_point)
            comparison = 0
        
        i += 1
    
    return edge

print edgefinder(a_run_02)