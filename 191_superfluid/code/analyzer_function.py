import matplotlib.pyplot as plt
import numpy as np
import os
import junk 

# Changes working directory to /data to access datasets
os.chdir("../data/")

######################
### BEGIN DATASETS ###
######################
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

he_run_01 = np.genfromtxt('manual_run.txt') 

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
        temp = np.append(temp, converter(ls[i], 'PT'))

    return temp

'''
HEAT CAPCAITY
'''
def ppFinder(data):
    
    time = data[:, 2]
    volt = data[:, 0] * (1.662 / 0.16754) # This is in mV
    
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
    '''
    for i in plateau:
        plt.axhline(i)
    plt.axvline(data[h1, 2], c='r')
    plt.axvline(data[l1, 2], c='r')
    '''    
    plt.plot(time, volt, 'g')
    plt.show()
    
    #return plateau

'''
a1 = 1300
a2 = a1 + 25

ppFinder(a_run_02, 0, -1)
ppFinder(a_run_02, a1, a2)
'''
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
    if string == 'he_below':
        L = 47  * (10 ** -3)
        V = 13.7
    if string == 'he_above':
        L = 47  * (10 ** -3)
        V = 13.7
    
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
    
    plt.plot(dT, C, 'o')
    plt.show()
    
    return np.array([dT, C])

plats    = np.genfromtxt('a_run_05_plateaus.txt')
addendum_plats = np.genfromtxt('a_run_06_plat.txt')
plats_02 = np.genfromtxt('he_below_l_a_run_02_plateaus.txt')
plats_03 = np.genfromtxt('he_above_l_a_run_01_plateaus.txt')
plats_04 = np.genfromtxt('he_run_1_pointer.txt')

he_true_plats = plats_04[3:, 1] * (1.662 / 0.16754)
addendum_true_plats = addendum_plats[3:,1] * (1.662/0.16754)

he_plat_temps = list_converter(he_true_plats)
addendum_plat_temps = list_converter(addendum_true_plats)

addendum_data = Heat(addendum_plat_temps, 'a_run_06')
he_data = Heat(he_plat_temps, 'he_below')

# iter over he data, getting the corresponding addendum vals and subtracting
# slow but who gives a fuck

# need to only choose temp data in helium measurement we have in our addendum

addendum_max_t = np.max(addendum_data[0])
addendum_min_t = np.min(addendum_data[0])

he_temp_data = he_data[0,:]
he_hcap_data = he_data[1,:]

# garbage bullshit code fucking sux
he_min_t = np.min(np.where(he_data[0] >= addendum_min_t)[0])
he_max_t = np.max(np.where(he_data[0] <= addendum_max_t)[0])

he_temp_data_restricted = he_temp_data[he_min_t:he_max_t]
he_hcap_data_restricted = he_hcap_data[he_min_t:he_max_t]

print 'lost %d points' % (len(he_temp_data)-len(he_temp_data_restricted))

final = np.array([])
for index, data in enumerate(he_temp_data_restricted):
    #print 'finding heat cap of addendum at temperature: %f' %data
    addendum_val = junk.subtract_addendum(addendum_data,data)
    #print 'addendum cap at %f: %f' % (data, addendum_val)
    final = np.append(final, he_hcap_data_restricted[index] - addendum_val)

#print 'before subtraction:'
#print he_hcap_data_restricted
#print 'after subtraction:'
#print final

plt.figure()
plt.plot(he_temp_data_restricted, he_hcap_data_restricted, c='blue', marker='o')
plt.plot(he_temp_data_restricted, final, c='red', marker='o') 
plt.show()

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

'''
# Temperature (K) v. Pressure (mTorr)
temp_mTorr = temperature[:, 0]
temp_mmHg  = temp_mTorr / 1000
temp_K     = temperature[:, 1]

#plt.plot(temp_mmHg, temp_K, 'g')
#plt.show()

# Calibration data plot
mmHg = cali_data[:, 0]
V1   = cali_data[:, 1]
V2   = cali_data[:, 2]

<<<<<<< HEAD
temper = list_converter(mmHg, 1)
=======
#plt.plot(V2, mmHg, 'ro')
#plt.show()
>>>>>>> b6a9dd69a901a0ecd67e63ac59877839d7e416c4

plt.plot(V1, temper, 'bo')
plt.show()
plt.plot(V2, temper, 'ro')
plt.show()
'''
#print("The ratio of V2:V1 without taking offset into account is: {} ").format(V2 / V1)

###################
#### END PLOTS ####
###################
