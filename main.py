#from centrals.PowerCentral import PowerCentral
from SegmentOptimizer import SegmentOptimizer
from MixSimulator import MixSimulator
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
# mix = SegmentOptimizer()
# mix.set_time(2)
# centrals=mix.set_data_csv("data/RIToamasina/dataset_RI_Toamasina.csv")
#  ##########

# green = []
# non_green = []
# for centrale in centrals:
#     if centrale.isGreen():
#         green.append(centrale)
#     else:
#         non_green.append(centrale)

#         #######

# mix.setCentrals(green)
# green_result = mix.getOptimumUsageCoef(carbonCostLimit=30)
# print(green_result)

###############
# mix.setCentrals(centrals)
# print(mix.getOptimumUsageCoef(carbonCostLimit=30))
mix = MixSimulator()
mix.set_data_csv("data/RIToamasina/dataset_RI_Toamasina.csv")
mix.optimizeMix(carbonCostLimit= 30)