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

"""
    Minimization of the cost production of the energy mix in the inter-connected Grid of Toamasina (time_interval = 2 hours)
"""

mix = MixSimulator()
mix.set_data_csv("data/RIToamasina/dataset_RI_Toamasina.csv")
# print(mix.optimizeMix(carbonProdLimit= 3950000000000, time_interval = 2))
mix.simuleMix(current_usage_coef=[0.6, 0.2, 0.7, 0.8], carbonProdLimit= 3950000000000, time_interval = 2, optimize_with = ["PSO","CMA","OnePlusOne","TBPSA"], budgets = [60,100,99])
