from .centrals import PowerCentral as pc
from .centrals import HydroCentral as hc 
from .Demand import Demand
import nevergrad as ng
from .nevergradBased.Optimizer import Optimizer
import numpy as np
import pandas as pd
import pkgutil
import csv
#import warnings
#import time
#from typing import List
#from datetime import datetime
#import matplotlib.pyplot as plt

class MixSimulator:
    """
        The simulator Base            
    """
    def __init__(self, carbon_cost: float = 0, penalisation_cost: float = 1000000000000):
        self.__centrals = []
        self.__reset_centrals()
        self.__demand = Demand(20, 0.2, 0.2)
        self.__lost = 0
        self.__penalisation_cost = penalisation_cost
        self.__optimizer =  Optimizer()
        self.__carbon_cost = carbon_cost
        self.__carbon_quota = 800139 # (g/MWh)

    def __reset_centrals(self):
        self.__centrals = []

    def set_data_csv(self, bind = None, raw_data = None, delimiter: str=";"):
        if raw_data is not None :
            data = pd.DataFrame(raw_data)
            #set columns & index           
            header = data.iloc[0]
            data = data[1:]
            data.columns = header
            data = data.reset_index(drop=True)
            for column in data.columns.tolist():
                try:
                    # convert numeric values
                    data[column] = pd.to_numeric(data[column])
                except:
                    pass
        else :
            try :
                data = pd.DataFrame(pd.read_csv(bind,delimiter=delimiter))
                print(data)
            except FileNotFoundError as e :
                print("Error occured on pandas.read_csv : ",e)
                print("Please check your file")
                raise           
            except Exception as e:
                print("Error occured on pandas.read_csv : ",e)
                raise
            
        self.__reset_centrals()
        try :
            for i in range (0,data.shape[0]):
                isHydro = data["hydro"][i]
                if isHydro == True :
                    centrale = hc.HydroCentral(data["height"][i],data["flow"][i],data["capacity"][i],data["stock_available"][i],0.1,0.8)
                else :
                    centrale = pc.PowerCentral()
                centrale.set_tuneable(data["tuneable"][i])
                centrale.set_id(str(data["centrals"][i]))
                centrale.set_fuel_consumption(data["fuel_consumption"][i])
                centrale.set_availability(data["availability"][i])
                centrale.set_fuel_cost(data["fuel_cost"][i])
                centrale.set_initial_value(data["init_value"][i])
                centrale.set_lifetime(data["lifetime"][i])
                centrale.set_carbon_prod(data["carbon_production"][i])
                centrale.set_raw_power(data["raw_power"][i])
                centrale.set_nb_employees(data["nb_employees"][i])
                centrale.set_mean_employees_salary(data["mean_salary"][i])
                self.__centrals.append(centrale)
            self.__demand.set_mean_demand(data["Demand"][0])
            self.__lost=data["lost"][0]
        except KeyError:
            print("Columns must be in: tuneable, centrals, fuel_consumption, availability, fuel_cost, init_value, lifetime, carbon_cost, raw_power, nb_employees, mean_salary, demand, lost")
            raise
            
    def set_data_to(self, dataset):
        #if dataset == "Toamasina":
        #by defaut we keep it "Toamasina"
        data = pkgutil.get_data('MixSimulator', '/data/RIToamasina/dataset_RI_Toamasina.csv')
        data = csv.reader(data.decode('utf-8').splitlines(), delimiter=';')
        self.set_data_csv(raw_data=data)
            
    def set_demand(self, demand: Demand):
        self.__demand = demand
    
    # def get_demand(self, t, time_interval: float = 1):
    #     return self.__demand.get_demand_approxima(t, time_interval)

    def set_penalisation_cost(self, k):
        self.__penalisation_cost = k

    def get_penalisation_cost(self):
        return self.__penalisation_cost
        
    def set_carbon_cost(self, carbon_cost):
        self.__carbon_cost = carbon_cost

    def get_carbon_cost(self):
        return self.__carbon_cost

    ## EVALUATION FONCTION ##
    def get_production_cost_at_t(self, usage_coef, time_index, time_interval):
        production_cost = 0
        for centrale_index in range (0, len(self.__centrals)):
            central = self.__centrals[centrale_index]
            production_cost += ( (central.get_fuel_cost() * central.get_fuel_consumption() 
            * central.get_raw_power() * usage_coef[centrale_index]) + ( central.get_employees_salary()
            + central.get_amortized_cost(time_index) ) ) * time_interval
        return production_cost

    def get_production_at_t(self, usage_coef, time_interval):
        production = 0
        for centrale_index in range (0, len(self.__centrals)):
            central = self.__centrals[centrale_index]
            production += (central.get_raw_power() * usage_coef[centrale_index]) * time_interval
        return production

    def get_unsatisfied_demand_at_t(self, usage_coef, time_index, time_interval):
        return ( self.__demand.get_demand_approxima(time_index, time_interval) - self.get_production_at_t(usage_coef, time_interval))
        
    def get_carbon_production_at_t(self, usage_coef, time_interval):
        carbon_prod = 0
        for centrale_index in range (0, len(self.__centrals)):
            central = self.__centrals[centrale_index]
            carbon_prod += (central.get_carbon_production() * usage_coef[centrale_index] * central.get_raw_power()) * time_interval
        return carbon_prod
        
    def get_carbon_over_production(self, usage_coef, time_interval):
        emited_carbon = 0 # (g)
        total_production = 1
        for t in range(0, len(usage_coef)):
            emited_carbon += self.get_carbon_production_at_t(usage_coef[t], time_interval)
            total_production += self.get_production_at_t(usage_coef[t], time_interval)
        carbon_production = emited_carbon/total_production
        return max(0, carbon_production - self.__carbon_quota) # (g/MWh)

    def get_weighted_coef(self, usage_coef, time_interval):
        for central_index in range(0, len(usage_coef[0])):
            try:
                self.__centrals[central_index].reset_stock()
            # Not a hydro power plant, so the methode does not exist
            except:
                pass
        weighted_coef = usage_coef.copy()
        for t in range(0, len(weighted_coef)):
            for central_index in range(0, len(weighted_coef[t])):
                weighted_coef[t][central_index] = weighted_coef[t][central_index] * self.__centrals[central_index].get_availability(t)
                try:
                    self.__centrals[central_index].back_propagate(weighted_coef[t][central_index], t, time_interval)
                # Not a hydro power plant, so the methode does not exist
                except:
                    pass
        return weighted_coef

    def loss_function(self, usage_coef, time_interval : int = 1) -> float :
        usage_coef = self.__arrange_coef_as_array_of_array(usage_coef)
        weighted_coef = self.get_weighted_coef(usage_coef, time_interval=time_interval)
        loss = 0
        for t in range(0, len(weighted_coef)):
            loss += self.get_production_cost_at_t(weighted_coef[t], t, time_interval) + ( self.get_penalisation_cost() * np.abs( self.get_unsatisfied_demand_at_t(weighted_coef[t], t, time_interval)) )
        loss +=  self.get_carbon_cost() * (self.get_carbon_over_production(weighted_coef, time_interval) )
        return loss

    def __arrange_coef_as_array_of_array(self, raw_usage_coef):
        ordered_coef = []
        cur_time_coef = []
        for coef_index in range(len(raw_usage_coef)):
            cur_time_coef.append(raw_usage_coef[coef_index])
            ## indice de la premiere cenrtale a t+1
            if (coef_index+1)%len(self.__centrals) == 0:
                ordered_coef.append(cur_time_coef)
                cur_time_coef = []
        return ordered_coef


    ## OPTiMiZATION ##

    def __opt_params(self, time_index):
        variable_parametrization = []
        for _ in range(time_index):
            for central_index in range(len(self.__centrals)):
                if not self.__centrals[central_index].is_tuneable():
                    variable_parametrization += [ng.p.Choice([0.,1.])]
                else:
                    variable_parametrization += [ng.p.Scalar(lower=0., upper=1.)]
        self.__optimizer.set_parametrization(variable_parametrization)
        
    def get_opt_params(self, time_index):
        variable_parametrization = []
        for _ in range(time_index):
            for central_index in range(len(self.__centrals)):
                if not self.__centrals[central_index].is_tuneable():
                    variable_parametrization += [ng.p.Choice([0.,1.])]
                else:
                    variable_parametrization += [ng.p.Scalar(lower=0., upper=1.)]
        return ng.p.Tuple(*variable_parametrization)

    def optimizeMix(self, carbon_quota: float = None, demand: Demand = None, lost: float = None, 
                    optimizer: Optimizer = None, step : int = 1,
                    time_index: int = 24*365, time_interval: float = 1,
                    penalisation : float = None, carbon_cost : float = None):

        self.__time_index = time_index
        
        # init params                
        if demand is not None : self.__demand = demand
        if lost is not None : self.__lost = lost
        if penalisation is not None : self.set_penalisation_cost(penalisation)
        if carbon_cost is not None : self.set_carbon_cost(carbon_cost)
        if carbon_quota is not None : self.__carbon_quota = carbon_quota
        if optimizer is not None : self.__optimizer = optimizer
        
        # tune optimizer parametrization
        self.__opt_params(time_index)
        
        #init constraints
        constraints = {}
        constraints.update({"time_interval":time_interval})
        
        #let's optimize
        results = self.__optimizer.optimize(self.loss_function, constraints=constraints, step = step)
        
        results = self.__reshape_results(results, time_interval)
        return results

    def __reshape_results(self, results, time_interval):
        for tmp in results:
            usage_coef = self.__arrange_coef_as_array_of_array(tmp['coef'])
            tmp.update({"coef":self.get_weighted_coef(usage_coef, time_interval)})

        for central_index in range(0, len(self.__centrals)):
            try:
                print(self.__centrals[central_index].get_stock_evolution())
            # Not a hydro power plant, so the methode does not exist
            except:
                pass
        return results