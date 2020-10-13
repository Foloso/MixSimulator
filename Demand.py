from math import pi
from math import cos

class Demand:
    """
        Manage the Demands data
    """
    def __init__(self,demand,var_per_day,var_per_season):
        self.__var_per_day = var_per_day
        self.__var_per_season = var_per_season
        self.__mean_demand = demand

    def set_mean_demand(self, demand: float):
        self.__mean_demand = demand

    def get_demand_approxima(self,t,interval):
        demande = self.__mean_demand * (1 + cos(2 * pi * ( t * interval )/ 24)*self.__var_per_day + cos(2 * pi * ( t * interval ) / (24*365))* self.__var_per_season)
        return demande

    #def getDemande(self, timerange: range=range(0,24)) -> dict[float, float]:
        #get demand per hour in a day 
    #    demand = {}
    #    for i in timerange:
    #        demand.update(i, self.__demandData.get(i))
    #    return demand