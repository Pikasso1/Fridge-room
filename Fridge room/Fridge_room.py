import random
import math
import pandas as pd
import numpy as np


def fridge_room(goal_temp, pris):
    tot_temp = 0
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

        gennemsnits_pris = np.average(pris)
        højeste_pris = np.max(pris)
        laveste_pris = np.min(pris)

        første_kvadrant = (gennemsnits_pris - laveste_pris) / 2
        tredje_kvadrant = (højeste_pris - gennemsnits_pris) / 2

        nuværende_pris = pris[i]
        mål_temperatur = 0

        if laveste_pris <= nuværende_pris < første_kvadrant:
            mål_temperatur = 4
        elif første_kvadrant <= nuværende_pris < gennemsnits_pris:
            mål_temperatur = 4.5
        elif gennemsnits_pris <= nuværende_pris < tredje_kvadrant:
            mål_temperatur = 5
        elif tredje_kvadrant <= nuværende_pris <= højeste_pris:
            mål_temperatur = 6

        if T[i-1] > mål_temperatur:
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

    # for i in range(len(pris)):
    #     tot_forbrug = tot_forbrug + forbrug[i]
    #     tot_madtab = tot_madtab + madtab[i]
    tot_forbrug = forbrug.sum()
    tot_madtab = madtab.sum()

    print(f"Gennemsnits temperatur er: {tot_temp/len(T)}")
    print(f"Gennemsnits forbrug er: {tot_forbrug/len(forbrug)}")
    print(f"Gennemsnits madtab er: {tot_madtab/len(madtab)}\n")
    return tot_forbrug+tot_madtab


def monte_carlo_simple(count, goal_temp, pris):
    monte_carlo_sum = 0
    best_guess = 0
    best_temp = 0

    for i in range(count):
        monte_carlo_sum = monte_carlo_sum + fridge_room(goal_temp, pris)
    monte_carlo_gennemsnit = monte_carlo_sum/count

    print(f"Gennemsnits omkostningerne er: {monte_carlo_gennemsnit} for mål temperatur {goal_temp}")
    return monte_carlo_gennemsnit
    

def main():
    pris = np.genfromtxt("elpris.csv", delimiter=",", usecols=[1])
    temperatures = np.linspace(3.5, 6.5, num=1)
    best_guess = 0
    best_temp = 0

    for goal_temp in temperatures:
        gennemsnit_omkostninger = monte_carlo_simple(100, goal_temp, pris)

        if gennemsnit_omkostninger < best_guess or best_guess == 0:
            best_guess = gennemsnit_omkostninger
            best_temp = goal_temp

    print(f"\nOmkostninger på: {best_guess}")


main()