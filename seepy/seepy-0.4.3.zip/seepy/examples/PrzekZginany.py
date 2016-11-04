# -*- coding: utf-8 -*-
from strupy import units as u

#!
'''
##*Obliczenie zbrojenia w przekroju zginanym prostokątnym*

*(metoda maksymalnie uproszczona)*
'''

#! ###1.Wymiary przekroju
h = 1200 *   u.mm  #<< - wysoko
b = 400 * u.mm #<< - szerokość przekroju

#! ###2.Obciążenie
Msd = 1200 *  u.kNm #<< - moment obliczeniowy

#! ###3.Materiał
materials = [300 * u.MPa, 400 * u.MPa, 500 * u.MPa]
fyd = materials[1] #<< - stal zbrojeniowaśćą

#! ---

#%img PrzekZginany_fig_1.png

#! Ze wzoru:

As1 = (  Msd / (0.8 * h) * 1 / fyd  ).asUnit(u.mm2) #%requ

#!
'''
---
###Podsumowanie
Dla przekroju o wymiarach val_b x val_h i obciażeniu var_Msd 
potrzebne zbrojenie dołem var_As1.
'''












