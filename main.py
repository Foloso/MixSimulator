#from centrals.PowerCentral import PowerCentral
from MixSimlator import MixSimulator
import nevergrad as ng
import numpy as np

#Centrales personnalisées
"""
centrals = []
for i in range (0, 4):
    centrale = False 
    if (i%2==0):
        centrale = True
    centrale = PowerCentral(centrale)
    centrale.set_fuel_consomption(4)
    centrale.setAvailability(1)
    centrale.set_fuel_cost(2000)
    centrale.set_initial_value(5000000)
    centrale.set_lifetime(24*365*50)
    centrale.setCarbonCost(10)
    centrale.setRawPower(1000000*i)
    centrale.set_nb_employees(20)
    centrale.setMeanEmployeesSalary(200000)
    centrals.append(centrale)
"""

#Initialisation of the simulator
mix = MixSimulator()
mix.set_time(2)
centrals=mix.set_data_csv("data/RIToamasina/dataset_RI_Toamasina.csv")
mix.setCentrals(centrals)
print(mix.getOptimumUsageCoef(carbonCostLimit=30))