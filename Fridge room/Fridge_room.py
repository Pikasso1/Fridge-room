import random
import math
import pandas as pd
import numpy as np


def fridge_room(goal_temp):
    tot_temp = 0
    pris = np.genfromtxt("elpris.csv", delimiter=",", usecols=[1])
    T = np.zeros(len(pris))
    forbrug = np.zeros(len(pris))
    madtab = np.zeros(len(pris))

    Temp_rum = 20
    Temp_komp = -5

    deltat = 300

    for i in range(len(pris)):
            tot_temp = tot_temp + T[i-1]    

            c_1 = 0
            c_2 = 0

            r = random.random()
            if r < 0.1:
                c_1 = 3*10**(-5)
            else:
                c_1 = 5*10**(-7)

            if T[i-1] > goal_temp:
                c_2 = 8*10**(-6)
                forbrug[i] = pris[i]
            else:
                c_2 = 0

            T[i] = T[i-1] + (c_1*(Temp_rum - T[i-1]) + c_2*(Temp_komp - T[i-1]))*deltat
            
        
            if T[i] < 3.5:
                madtab[i] = 4.39*math.exp(-0.49*T[i])
            elif 6.5 < T[i]:
                madtab[i] = 0.11*math.exp(0.31*T[i])
    
    tot_forbrug = 0
    tot_madtab = 0

    for i in range(len(pris)):
        tot_forbrug = tot_forbrug + forbrug[i]
        tot_madtab = tot_madtab + madtab[i]

    print(f"Gennemsnits temperatur er: {tot_temp/len(T)}")
    # print(f"Gennemsnits forbrug er: {tot_forbrug/len(forbrug)}")
    # print(f"Gennemsnits madtab er: {tot_madtab/len(madtab)}")
    return tot_forbrug+tot_madtab

montecarlo = 0
count = 100

for i in range(count):
    montecarlo = montecarlo + fridge_room(4)

print("\n")
print(f"Gennemsnits omkostningerne er: {montecarlo/count}")