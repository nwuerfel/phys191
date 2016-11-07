import matplotlib.pyplot as plt
import numpy as np
import os

# Changes working directory to /data to access datasets
os.chdir("../data/")

cali_data = np.genfromtxt('cali_new.txt', delimiter=',', skip_header=1)
temperature = np.genfromtxt('temperature.txt')

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

def list_converter(ls, ind=2):
    temp = np.array([])
    
    if ind == 1:
        for i in range(len(ls)):
            temp = np.append(temp, converter(ls[i], 'PT'))

    if ind == 2:
        for i in range(len(ls)):
            temp = np.append(temp, converter(converter(ls[i], 'VP'), 'PT'))

    return temp

########################
### Calibration Plot ###
########################

P  = cali_data[:, 0]
T  = list_converter(P, 1)
V1 = cali_data[:, 1]
V2 = cali_data[:, 2]

fig, ax1 = plt.subplots()

# These are in unitless percentages of the figure size. (0,0 is bottom left)
left, bottom, width, height = [0.25, 0.6, 0.2, 0.2]
ax2 = fig.add_axes([left, bottom, width, height])

ax1.plot(V1, V2, color='red')
ax2.plot(V1, V2, color='green')

plt.show()

'''
def cali_plot():
    size = 16
    
    plt.plot(V1, T, 'ro', label='1.013 uA')
    plt.plot(V2, T, 'bo', label='1.957 uA')
    plt.title('Calibration Plot', fontsize=size+6)
    plt.xlabel('Voltage (mV)', fontsize=size)
    plt.xlim([0, 21])
    plt.xticks(fontsize=15)    
    plt.ylabel('Temperature (K)', fontsize=size)
    plt.yticks(fontsize=15)
    plt.legend(loc=0, prop={'size':15}, numpoints=1)
    plt.tight_layout()
    plt.savefig('calibration_curve.pdf')
    
cali_plot()
'''