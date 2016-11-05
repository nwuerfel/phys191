import numpy as np
import os
from analyzer_function import PTconverter

data_Dir = '../data/ss_runs/'
pressures = np.array([12.7, 7.1, 10.8, 17, 21.5, 26, 30, 35])

def second_sound():

    vel_Data = np.empty([len(os.listdir(data_Dir)),2])
    j = 0;

    # use converter when its done
    temperatures = PTconverter(pressures)

    for file in os.listdir(data_Dir):
        if file=='.DS_Store':
            continue

        print 'Doing the data dance: %s' % file 

        data = np.genfromtxt(data_Dir + file)

        time = data[:,1]
        dist = data[:,2]

        vel = np.empty(len(dist), dtype=float)

        for i in range(0,len(dist)):
            vel[i]=dist[i]/time[i]
    
        vel_Data[j,0] = np.mean(vel)
        # janky fucking shit
        vel_Data[j,1] = temperatures[j]
        j = j + 1
    
    return vel_Data    
