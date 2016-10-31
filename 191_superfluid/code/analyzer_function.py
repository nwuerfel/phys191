import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

os.chdir("../data/")

cali_data = pd.read_csv('cali_new.txt')

mmHg = cali_data[[0]]
V1   = cali_data[[1]]
V2   = cali_data[[2]]

plt.plot(mmHg, V1, 'ro')
plt.plot(mmHg, V2, 'bo')
plt.show()

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
    x = data[:, 2]
    y = data[:, 0]
    
    plt.plot(x, y, form)
    plt.title('Title')
    plt.xlabel('Time (s)')
    plt.ylabel('INSERT LABEL (mV)')
    plt.show()
    
analyzer(a_run_02, 'g')
