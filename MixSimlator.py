from nevergradBased.Optimizer import Optimizer
from centrals.PowerCentral import PowerCentral
from typing import List
import numpy as np
import pandas as pd
from centrals.PowerCentral import PowerCentral

class MixSimulator:
    """
        The simulator Base Version 0.1
        Initiate the appropriate optimization and the power plants:
             Define the objective function;
             Define the constraints;
             Manage data sets;
             Calculates the value of the explanatory variables;
            
    """
    def __init__(self):
        self.__optimizer = Optimizer()
        self.__centrals = []
        self.__demand = 1
        #Static lost
        self.__lost = 0
        pass
    
    def set_data_csv(self, bind: str, delimiter: str=";"):
        try :
            data = pd.DataFrame(pd.read_csv(bind,delimiter=delimiter))
        except : 
            print("Error occured on pandas.read_csv")
        centrals = []
        
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
                centrals.append(centrale)
            self.__demand=data["Demand"][0]
            self.__lost=data["lost"][0]
        except KeyError:
            print("One of columns missing : tuneable, centrals, fuel_consumption, availability, fuel_cost, init_value, lifetime, carbon_cost, raw_power, nb_employees, mean_salary")
        return centrals
        

    def setCentrals(self, centrals: List[PowerCentral]):
        self.__centrals.clear()
        for central in centrals:
            self.__centrals.append(central)
    
    def get_fuel_cost(self,centrals: List[PowerCentral] = None):
        centrals = self.__getCentrals(centrals)
        fuel_costs = []
        for central in centrals:
            if(central.isTuneable()) :
                #waiting better way to specification, we supposed that tuneable == Thermal Power plant 
                fuel_costs.append(central.get_fuel_cost())
            else :
                fuel_costs.append(1)
        return np.array(fuel_costs)
        
    def get_fuel_consumption(self,centrals: List[PowerCentral] = None):
        centrals = self.__getCentrals(centrals)
        consumption = []
        for central in centrals:
            if(central.isTuneable()) : 
                #waiting better way to specification, we supposed that tuneable == Thermal Power plant 
                consumption.append(central.get_fuel_consumption())
            else:
                consumption.append(1)
        return np.array(consumption)
    
    def get_rawPower(self,centrals: List[PowerCentral] = None):
        centrals = self.__getCentrals(centrals)
        raw_power = []
        for central in centrals:
            raw_power.append(central.getRawPower())
        return np.array(raw_power)
        
    def get_salary_cost(self,centrals: List[PowerCentral] = None):
        centrals = self.__getCentrals(centrals)
        salary_cost = []
        for central in centrals:
            salary_cost.append(central.getEmployeesSalary())
        return np.array(salary_cost)
    
    def get_amortized_cost(self,centrals: List[PowerCentral] = None):
        centrals = self.__getCentrals(centrals)
        amortized_cost = []
        for central in centrals:
            amortized_cost.append(central.get_amortized_cost())
        return np.array(amortized_cost)
    
    def get_carbon_cost(self, centrals: List[PowerCentral] = None):
        centrals = self.__getCentrals(centrals)
        carbon_cost = []
        for central in centrals:
            carbon_cost.append(central.getCarBonCost())
        return np.array(carbon_cost)

    def get_avaibility_limit(self, centrals: List[PowerCentral] = None):
        centrals = self.__getCentrals(centrals)
        avaibility_limit = []
        for central in centrals:
            avaibility_limit.append(central.getAvailability())
        return np.array(avaibility_limit)

    def set_time(self, duration):
        self.duration = duration
    
    def get_time(self):
        return self.duration
    
    def prod_cost_objective_function(self,coef_usage):
        return sum((( self.get_fuel_cost() * self.get_fuel_consumption() * coef_usage * self.get_rawPower() )
        + (self.get_salary_cost() + self.get_amortized_cost()))* self.get_time()) 

    def get_carbon_cost_constraint(self, coef_usage):
        return sum(self.get_carbon_cost() * coef_usage)
    
    def get_production_constraint(self, coef_usage):
        return sum(self.get_rawPower() * coef_usage * self.get_time())
        
    def getOptimumUsageCoef(self, time_range : range=range(0,24), carbonCostLimit: float = None, demand: float = None, lost: float = None) -> List[float]:
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
        constrains.update({"carbonCostLimit": carbonCostLimit})
        constrains.update({"carbonCost": self.get_carbon_cost_constraint})
        constrains.update({"availability": self.get_avaibility_limit()})

        #setting all parameters
        self.__optimizer.set_parametrization(len(centrals), np.amax(self.get_avaibility_limit()))
        prod_cost_optimal= self.__optimizer.opt_OnePlusOne(self.prod_cost_objective_function, constrains) #Optimisation
        return prod_cost_optimal

    def __getNonTuneableCentralIndex(self, centrals: List[PowerCentral]= None):
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

    def __getCentrals(self, centrals: List[PowerCentral]=None):
        if(centrals==None):
            centrals = self.__centrals
        return centrals