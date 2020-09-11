from SegmentOptimizer import SegmentOptimizer
from centrals.PowerCentral import PowerCentral
import pandas as pd
from typing import List


class MixSimulator:
    def __init__(self):
        self.__reset_centrals()

    def __reset_centrals(self):
        self.__centrals = {}
        self.__centrals.update({"green": []})
        self.__centrals.update({"non_green": []})

    def set_data_csv(self, bind: str, delimiter: str=";"):
        try :
            data = pd.DataFrame(pd.read_csv(bind,delimiter=delimiter))
        except : 
            print("Error occured on pandas.read_csv")
        self.__reset_centrals()
        centrale_tmp = []
        try :
            for i in range (0,data.shape[0]):
                centrale = data["tuneable"][i]
                centrale = PowerCentral(centrale)
                centrale.set_id(data["centrals"][i])
                centrale.set_fuel_consumption(data["fuel_consumption"][i])
                centrale.setAvailability(data["availability"][i])
                centrale.set_fuel_cost(data["fuel_cost"][i])
                centrale.set_initial_value(data["init_value"][i])
                centrale.set_lifetime(data["lifetime"][i])
                centrale.setCarbonCost(data["carbon_cost"][i])
                centrale.setRawPower(data["raw_power"][i])
                centrale.set_nb_employees(data["nb_employees"][i])
                centrale.setMeanEmployeesSalary(data["mean_salary"][i])
                centrale.setGreenEnergy(data["green"][i])
                centrale_tmp.append(centrale)
            self.__demand=data["Demand"][0]
            self.__lost=data["lost"][0]
        except KeyError:
            print("One of columns missing : tuneable, centrals, fuel_consumption, availability, fuel_cost, init_value, lifetime, carbon_cost, raw_power, nb_employees, mean_salary")
        self.__splitCentrals(centrale_tmp)

    def setCentrals(self, centrals: List[PowerCentral]):
        self.__reset_centrals()
        self.__splitCentrals(centrals)

    def __splitCentrals(self, centrals: List[PowerCentral]):
        for centrale in centrals:
                if centrale.isGreen():
                    self.__centrals["green"].append(centrale)
                else:
                    self.__centrals["non_green"].append(centrale)


    def optimizeMix(self, carbonCostLimit, demand: float= None, lost: float=None ):
        # default parameter
        usage_coef = []
        productionCost = 0.
        if demand is None:
            demand = self.__demand
        if lost is None:
            lost = self.__lost


        green_mix = SegmentOptimizer()
        non_green_mix = SegmentOptimizer()
        
        green_mix.setCentrals(self.__centrals["green"])
        non_green_mix.setCentrals(self.__centrals["non_green"])

        green_mix.set_time(2)
        non_green_mix.set_time(2)

        # prioriser d'abord les energies renouvelables
        print(green_mix.getOptimumUsageCoef(carbonCostLimit=carbonCostLimit, demand= demand, lost=lost))
        GREEN_RESULT = green_mix.getOptimumUsageCoef(carbonCostLimit=carbonCostLimit, demand= demand, lost=lost)
        carbonCostLimit = carbonCostLimit - GREEN_RESULT["carbonCost"]
        demand = demand - GREEN_RESULT["production"]
        production_cost = GREEN_RESULT["production cost"]
        for coef in GREEN_RESULT["coef"]:
            usage_coef.append(coef)

        print(non_green_mix.getOptimumUsageCoef(carbonCostLimit=carbonCostLimit, demand=demand, lost=lost))
        NON_GREEN_RESULT = non_green_mix.getOptimumUsageCoef(carbonCostLimit=carbonCostLimit, demand=demand, lost=lost)
        carbonCostLimit = carbonCostLimit - NON_GREEN_RESULT["carbonCost"]
        demand = demand - NON_GREEN_RESULT["production"] + lost
        production_cost = production_cost + NON_GREEN_RESULT["production cost"]
        for coef in NON_GREEN_RESULT["coef"]:
            usage_coef.append(coef)

        print(usage_coef)
        print(production_cost, demand, carbonCostLimit)