import math
import random
import pandas as pd
import numpy as np
import Opgave_2 as Fie

El_pris = pd.read_csv("elpris.csv")
pris = pd.to_numeric(El_pris['Pris']).values


# Simulation af september
def simuler_september():

    T_rum = 20.0
    T_komp = -5.0
    dt = 5 * 60                # 5 minutter i sekunder
    N = 30 * 24 * 60 // 5      # antal 5-minutters intervaller

    T = 5.0

    total_madtab = 0.0
    total_udgift = 0.0

    for i in range(N):

        Elpris = pris[i]  

        # C1 (døren)
        C1 = Fie.er_døren_åben()


        # Kompressor - tilkalder vores funktion med vores C2 og forbrug værdier 
        kompressor = Fie.komp_start(pris,i,T)
        # Læser værdierne ud af listen vi kalder kompressor
        C2 = kompressor[0]                
        forbrug = kompressor[1]           

        
        # Temperaturmodel
        T = T + (C1 * (T_rum - T) + C2 * (T_komp - T)) * dt
        

        # Madtab
        madtab = Fie.udregn_madtab(T)

        
        total_madtab += madtab
        total_udgift += (forbrug + madtab)

    return total_udgift


# MONTE CARLO
def monte_carlo(M):
    resultater = []
    for _ in range(M):
        resultater.append(simuler_september())
    gennemsnit = sum(resultater) / M
    return gennemsnit, resultater

def main():
    # KØR 200 SIMULERINGER
    M = 100
    gennemsnit, alle = monte_carlo(M)

    print(f"Gennemsnitlig udgift for september: {gennemsnit:.2f} kr")






def er_døren_åben():
    if r < 0.1:
        return åben
    else:
        return lukket