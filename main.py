#from centrals.PowerCentral import PowerCentral
#from SegmentOptimizer import SegmentOptimizer
from MixSimulator import MixSimulator
from Evaluation import Evaluation

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

mix = MixSimulator()
mix.setCentrals(centrals)
mix.simuleMix(current_usage_coef=[0.6, 0.2, 0.7, 0.95], carbonProdLimit= 3950000000000, time_interval = 2, optimize_with = ["PSO","OnePlusOne"], budgets = [60,100] )
"""


"""
    Minimization of the cost production of the energy mix in the inter-connected Grid of Toamasina (time_interval = 2 hours )
"""

mix = MixSimulator()
mix.set_data_csv("data/RIToamasina/dataset_RI_Toamasina.csv")
#mix.simuleMix(current_usage_coef=[0.6, 0.2, 0.7, 0.95], carbonProdLimit= 3950000000000, time_interval = 2, optimize_with = ["OnePlusOne"], budgets = [100])
eva=Evaluation()
eva.evaluate(mix, 10, 300, ["OnePlusOne","DE"], ["production_cost ($)","carbon_impacte (g/MWh)","unsatisfied_demand (MWh)"])