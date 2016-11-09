import matplotlib.pyplot as plt
import numpy as np
import os
import junk

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
    '''
    plt.plot(dT, C, 'bo')
    plt.show()
    plt.plot(dT, C, 'b')
    plt.show()
    '''
    
    return np.array([dT, C])

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
    if string == 'a_run_05':
        L = 398 * (10 ** -6)
        V = 10
    if string == 'a_run_06':
        L = 210 * (10 ** -6) 
        V = 13.5
    if string == 'he':
        L = 47  * (10 ** -3)
        V = 13.7
    
    return (V ** 2) * L / R

########################
######### Plot #########
########################

P   = cali_data[:, 0]
T   = list_converter(P, 1)
V1  = cali_data[:, 1]
V2  = cali_data[:, 2]
V_r = V2 / V1
avg_r = np.average(V_r)

print avg_r, 1.957 / 1.013

def cali_plot():
    
    size  = 16 
    size1 = 16
    
    left, bottom, width, height = [0.72, 0.4, 0.2, 0.2]
    
    fig, ax  = plt.subplots()
    ax1 = fig.add_axes([left, bottom, width, height])
    ax1.set_xlabel('$V_1$', fontsize=size1)
    ax1.set_ylabel('$V_2$', fontsize=size1)
    
    ax1.plot(V1, V2, color='purple')   
    ax1.set_title('INSERT BETTER NAME')
    
    ax.plot(V1, T, 'bo', label='$I_1 : 1.013 \mu A$')
    ax.plot(V2, T, 'ro', label='$I_2 : 1.957 \mu A$')
    ax.set_title('Calibration Plot', fontsize=size+6)
    ax.set_xlabel('Voltage (mV)', fontsize=size)
    ax.set_xlim([0, 21])
    ax.set_ylabel('Temperature (K)', fontsize=size)
    ax.legend(loc=0, prop={'size':15}, numpoints=1)
    
    plt.tight_layout()
    plt.savefig('calibration_curve.pdf')

plats_04       = np.genfromtxt('he_run_1_pointer.txt')
addendum_plats = np.genfromtxt('a_run_06_plat.txt')

he_true_plats       = plats_04[3:, 1] * (1.662 / 0.16754)
addendum_true_plats = addendum_plats[3:,1] * (1.662/0.16754)

z = np.polyfit(V1, T, 12)
p = np.poly1d(z)

def lambda_point():
    he_data       = Heat(p(he_true_plats), 'he')
    addendum_data = Heat(p(addendum_true_plats), 'a_run_06')
    
    addendum_max_t = np.max(addendum_data[0])
    addendum_min_t = np.min(addendum_data[0])
    
    he_temp_data = he_data[0,:]
    he_hcap_data = he_data[1,:]
    
    he_min_t = np.min(np.where(he_data[0] >= addendum_min_t)[0])
    he_max_t = np.max(np.where(he_data[0] <= addendum_max_t)[0])

    he_temp_data_restricted = he_temp_data[he_min_t:he_max_t]
    he_hcap_data_restricted = he_hcap_data[he_min_t:he_max_t]
    
    final = np.array([])
    for index, data in enumerate(he_temp_data_restricted):
    #print 'finding heat cap of addendum at temperature: %f' %data
        addendum_val = junk.subtract_addendum(addendum_data, data)
    #print 'addendum cap at %f: %f' % (data, addendum_val)
        final = np.append(final, he_hcap_data_restricted[index] - addendum_val)

    plt.plot(he_temp_data_restricted, he_hcap_data_restricted, 'bo')
    plt.show()
    plt.plot(he_temp_data_restricted, final, 'ro') 
    plt.show()

lambda_point()
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