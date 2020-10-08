from .nevergradBased import Optimizer as opt
from .centrals import PowerCentral as pc
from typing import List
import numpy as np
import pandas as pd
from nevergrad import p
#from centrals.PowerCentral import PowerCentral

class SegmentOptimizer:
    """
        Initiate the appropriate optimization and the power plants:
             Define the objective function;
             Define the constraints;
             Manage data sets;
             Calculates the value of the explanatory variables;
            
    """
    def __init__(self):
        self.__optimizer = opt.Optimizer()
        self.__centrals = []
        self.__demand = 1
        #Static lost
        self.__lost = 0
        self.duration = 1
        self.__time_index = 1
    
    def setCentrals(self, centrals: List[str]):
        self.__centrals.clear()
        for central in centrals:
            self.__centrals.append(central)
    
    def get_fuel_cost(self,centrals: List[str] = None):
        centrals = self.__getCentrals(centrals)
        fuel_costs = []
        for central in centrals:
            if(central.isTuneable()) :
                #waiting better way to specification, we supposed that tuneable == Thermal Power plant 
                fuel_costs.append(central.get_fuel_cost())
            else :
                fuel_costs.append(1)
        return np.array(fuel_costs)
        
    def get_fuel_consumption(self,centrals: List[str] = None):
        centrals = self.__getCentrals(centrals)
        consumption = []
        for central in centrals:
            if(central.isTuneable()) : 
                #waiting better way to specification, we supposed that tuneable == Thermal Power plant 
                consumption.append(central.get_fuel_consumption())
            else:
                consumption.append(1)
        return np.array(consumption)
    
    def get_rawPower(self,centrals: List[str] = None):
        centrals = self.__getCentrals(centrals)
        raw_power = []
        for central in centrals:
            raw_power.append(central.getRawPower())
        return np.array(raw_power)
        
    def get_salary_cost(self,centrals: List[str] = None):
        centrals = self.__getCentrals(centrals)
        salary_cost = []
        for central in centrals:
            salary_cost.append(central.getEmployeesSalary())
        return np.array(salary_cost)
    
    def get_amortized_cost(self,centrals: List[str] = None):
        centrals = self.__getCentrals(centrals)
        amortized_cost = []
        for central in centrals:
            amortized_cost.append(central.get_amortized_cost())
        return np.array(amortized_cost)
    
    def get_carbon_prod(self, centrals: List[str] = None):
        centrals = self.__getCentrals(centrals)
        carbon_prod = []
        for central in centrals:
            carbon_prod.append(central.getCarbonProd())
        return np.array(carbon_prod)
        
    def set_time_index(self,time):
        self.__time_index = time

    def get_avaibility_limit(self, centrals: List[str] = None):
        centrals = self.__getCentrals(centrals)
        avaibility_limit = []
        for central in centrals:
            if central.isGreen():
                 avaibility_limit.append(central.get__availability(self.__time_index,self.get_time()))
            else :
                avaibility_limit.append(central.getAvailability())
        return np.array(avaibility_limit)

    def set_time(self, duration):
        self.duration = duration
    
    def get_time(self):
        return self.duration
    
    def prod_cost_function(self,coef_usage):
        return sum((( self.get_fuel_cost() * self.get_fuel_consumption() * coef_usage * self.get_rawPower() )
        + (self.get_salary_cost() + self.get_amortized_cost()))* self.get_time()) 

    def get_carbon_prod_constraint(self, coef_usage):
        return sum(self.get_carbon_prod() * coef_usage)
    
    def get_production_constraint(self, coef_usage):
        return sum(self.get_rawPower() * coef_usage * self.get_time())
        
    # def get_normalized_production_constraint(self, coef_usage, coef_norm):
        # return sum(self.get_rawPower() * coef_usage * self.get_time())

    def getOptimumUsageCoef(self, carbonProdLimit: float = None, demand: float = None,
                            lost: float = None, optimize_with = ["OnePlusOne"], budgets = [100], instrum = None, step: int =1, penalisation : float = 1000000000000) -> List[float]:
        centrals = self.__getCentrals() 
        if demand == None : 
            demand = self.__demand
            
        #static lost
        if lost == None : 
            lost = self.__lost
            
        # self.set_fuel_cost(centrals)        

        #initiate constraints
        constrains = {}
        constrains.update({"production": self.get_production_constraint})
        constrains.update({"demand": demand})
        constrains.update({"lost": lost})
        constrains.update({"nonTuneable": self.__getNonTuneableCentralIndex(centrals)})
        constrains.update({"carbonProdLimit": carbonProdLimit})
        constrains.update({"carbonProd": self.get_carbon_prod_constraint})
        constrains.update({"availability": self.get_avaibility_limit()})

        #setting all parameters
        if instrum == None :
            self.__optimizer.set_parametrization(p.Array(shape=(len(centrals),)), np.amax(self.get_avaibility_limit()))
        else :
            self.__optimizer.set_parametrization(instrum, np.amax(self.get_avaibility_limit()))

        
        prod_cost_optimal = self.__optimizer.opt_With(self.prod_cost_function, constrains, optimize_with,budgets, step= step, k = penalisation)
        
        return prod_cost_optimal

    def __getNonTuneableCentralIndex(self, centrals: List[str]= None):
        #split tuneable and non tuneable power plant
        i = 0
        nonTuneableCentral = []
        centrals = self.__getCentrals(centrals)
        for central in centrals:
            if central.isTuneable():
                pass
            else:
                nonTuneableCentral.append(i)
            i+=1
        return nonTuneableCentral

    def __getCentrals(self, centrals: List[str]=None):
        if(centrals==None):
            centrals = self.__centrals
        return centrals