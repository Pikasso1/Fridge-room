import math
import random
import pandas as pd
import numpy as np


def komp_start(pris,nuværende_tidspunkt,temperatur):
    """
    Funktionen komp_start tager de nedenstående inputs, og beregner forbruget af el og værdien af C2. 
    Her er C2 ansvarlig for at beskrive om kompressoren er tændt eller ej, når vi udregner næste temperatur

    "pris" er alle el priser i september måned 
    "nuværende_tidspunkt" er nuværende tidspunkt, som vi har kaldt "i" i opgave 1
    "temperatur" er temperaturen i nuværende tidspunkt
    """

    
    # Finder de forskellige værdier for el i september måned
    gennemsnits_pris = np.average(pris) 
    højeste_pris = np.max(pris)
    laveste_pris = np.min(pris)
    første_kvadrant = (gennemsnits_pris - laveste_pris) / 2
    tredje_kvadrant = (højeste_pris - gennemsnits_pris) / 2

    # Finder den nuværende pris for el
    nuværende_pris = pris[nuværende_tidspunkt]
    # Gemmer for at bruge den senere
    mål_temperatur = 0

    # Elpriserne er lave for vi vil gerne køle meget ned
    if laveste_pris <= nuværende_pris < første_kvadrant:
        mål_temperatur = 4
    # Elrpiserne er højere og har dermed ikke så meget lyst til at køl ned
    elif første_kvadrant <= nuværende_pris < gennemsnits_pris:
        mål_temperatur = 4.5
    # Elrpiserne er høj og har dermed ikke så meget lyst til at så meget køl ned
    elif gennemsnits_pris <= nuværende_pris < tredje_kvadrant:
        mål_temperatur = 5
    # Elrpiserne er meget høj og har dermed kølere næsten ikke
    elif tredje_kvadrant <= nuværende_pris <= højeste_pris:
        mål_temperatur = 6.5

    # Tænd kompresseren hvis temperaturen er højere end ønsket
    if temperatur > mål_temperatur:
        C2 = 8*10**-6
        forbrug = 1.0 * nuværende_pris
        kompressor = [C2,forbrug]
        return kompressor
    # Tænder ikke kompresseren
    else:
        C2 = 0
        forbrug = 0 
        kompressor = [C2,forbrug]
        return kompressor

def udregn_madtab(temperatur):
    """
    Udregner tabet af værdi grundet temperaturen. 
    Enten er den for høj og maden bliver dårlig, eller bliver den for lav, og maden dybfryses
    """

    if temperatur < 3.5:
        madtab = 4.39 * math.exp(-0.49 * temperatur)
        return madtab
    elif temperatur < 6.5:
        madtab = 0
        return madtab
    else:
        madtab = 0.11 * math.exp(0.31 * temperatur)
        return madtab

    

def er_døren_åben(): 
    r = random.random()
    if r < 0.1:
        C1 = 3*10**-5
        return C1
    else:
        C1 = 5*10**-7
        return C1   