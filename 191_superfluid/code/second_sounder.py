import matplotlib.pyplot as plt
import numpy as np
import os
from analyzer_function import PTconverter

data_Dir = '../data/ss_runs/'
pressures = np.array([12.7, 7.1, 10.8, 17, 21.5, 26, 30, 35])
distance_uncertainty = 0.1
time_uncertainty = 1

def second_sound():

    vel_Data = np.empty([len(os.listdir(data_Dir)),3])
    j = 0;

    # use converter when its done
    temperatures = PTconverter(pressures)

    for file in os.listdir(data_Dir):
        if file=='.DS_Store':
            continue

        print 'Doing the data dance: %s' % file 

        data = np.genfromtxt(data_Dir + file)

        dist = data[:,1]
        time = data[:,2]

        vel = np.empty(len(dist), dtype=float)
        vel_uncertainty = np.empty(len(dist), dtype=float)

        for i in range(0,len(dist)):
            vel[i]=dist[i]/time[i]
            vel_uncertainty[i] = (dist[i]/time[i])*np.sqrt((distance_uncertainty/dist[i])**2 * (time_uncertainty/time[i])**2)

        ## ??? WHATS A STATISTICS?
        mean_uncertainty = np.sqrt(np.sum(np.square(vel_uncertainty)))
        total_uncertainty = np.sqrt(np.std(vel)**2 + mean_uncertainty**2)

        # janky fucking shit
        vel_Data[j,0] = temperatures[j]
        vel_Data[j,1] = np.mean(vel)
        vel_Data[j,2] = total_uncertainty 
        j = j + 1

    print vel_Data
    vel_Data = vel_Data[vel_Data[:,0].argsort()]
    print vel_Data

    # plot that fucking shit yooooooooo

    # try this stupid analytical function:
    x = np.linspace(1.6,2.17,1000)
    y = 26*np.sqrt((x/2.17)*(1-((x/2.17))**(5.5)))

    plt.figure()
    
    ax = plt.subplot()

    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(18)

    # setup the function we're comparing to
    plt.plot(x,y,linewidth=2, c='blue')

    # errorbar our fucking data yo
    plt.errorbar(vel_Data[:,0],vel_Data[:,1],yerr=vel_Data[:,2],elinewidth = 2,linewidth=2, c ='red',marker='o') 
    plt.title('Velocity of Second Sound', fontsize=36)
    plt.xlabel('Temperature (K)', fontsize=28)
    plt.ylabel('Velocity (m/s)', fontsize=28)
    plt.tight_layout() 
    plt.show()
    
    return vel_Data    
