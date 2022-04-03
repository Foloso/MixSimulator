from .Interfaces import Observer, Observable
from ..power_plants.mas.PowerPlant import PowerPlant
from ..demand.mas.Demand import Demand
import nevergrad as ng
from ..nevergradBased.Optimizer import Optimizer
import numpy as np # type: ignore
import pandas as pd # type: ignore
import pkgutil
import csv
import os
import warnings
from math import ceil
#import time
from typing import List, Any, Type, Dict
from datetime import datetime
import matplotlib.pyplot as plt # type: ignore

class Moderator(Observer):
    def __init__(self,carbon_cost, penalisation_cost) -> None:
        super().__init__()
        self.__observable : List[PowerPlant] = []
        self.__powerplants_down : List[PowerPlant] = []
        dm = Demand(demand= 20, var_per_day= 0.2, var_per_season= 0.2)
        dm.set_data_to("Toamasina",delimiter=",")
        self.__demand = dm
        self.__cst_lost = 0.
        self.__penalisation_cost = penalisation_cost
        self.__optimizer =  Optimizer()
        self.__carbon_cost = carbon_cost
        self.__carbon_quota = 800139. # (g/MWh)
        self.__planning = ...
        
        # for reuse and get_params()
        self.time_index = 24*7
        self.step = 1
        self.time_interval = 1
        self.plot = "default"
        self.average_wide = 0

    def __reset_powerplant(self):
        self.__observable : List[PowerPlant] = []

    def get_observable(self) -> List[Observable]:
        return self.__observable

    def set_observable(self, observables: List[Observable]) -> None:
        self.__observable = observables
      
    def __add_observable(self, observable: Observable, id_ = None) -> None:
        if id_ is None:
            if observable not in self.__observable:
                self.__observable.append(observable)
        else:
            for observable in self.__powerplants_down:
                if observable.get_id() == id_:
                    self.__observable.append(observable)

    def __detach_observable(self, id_: str = None) -> None:
        for i, observable in enumerate(self.__observable):
            if observable.get_id() == id_ :
                self.__powerplants_down.append(self.__observable.pop(i))
    
    ### COMMUNICATION
    def update(self, observable, signal, *args, **kwargs) -> None:
        print(observable, "sends signal code ", signal["code"])
        if signal["code"] == 100:
            self.__add_observable(observable)
        elif signal["code"] == 400:
            self.__detach_observable(id_ = signal["id"])
        elif signal["code"] == 200:
            self.__add_observable(observable, id_ = signal["id"])



    ### PARAMETRIZATION
    def set_demand(self, demand_agent) -> None:
        self.__demand = demand_agent

    def get_demand(self):
        return self.__demand

    def set_mean_demand(self, mean_demand) -> None:
        self.__demand = mean_demand

    def set_constant_lost(self, lost) -> None:
        self.__cst_lost = lost

    def set_optimizer(self, optimizer: Optimizer):
        self.__optimizer = optimizer
        
    def get_optimizer(self) -> Optimizer:
        return self.__optimizer

    def set_carbon_quota(self, cb_quota: float ):
        self.__carbon_quota = cb_quota

    def set_penalisation_cost(self, k):
        self.__penalisation_cost = k

    def get_penalisation_cost(self):
        return self.__penalisation_cost
        
    def set_carbon_cost(self, carbon_cost):
        self.__carbon_cost = carbon_cost

    def get_carbon_cost(self):
        return self.__carbon_cost

    ### EVALUATION FUNCTIONS
    def get_production_cost_at_t(self, usage_coef, time_index, time_interval):
        production_cost = 0
        for powerplant_index in range (0, len(self.__observable)):
            if self.__observable[powerplant_index].get_type() != "Demand":
                powerplant = self.__observable[powerplant_index]
                production_cost += ( (powerplant.get_fuel_cost() * powerplant.get_fuel_consumption() 
                * powerplant.get_raw_power() * usage_coef[powerplant_index]) + ( powerplant.get_employees_salary()
                + powerplant.get_amortized_cost(time_index) ) ) * time_interval
        return production_cost

    def get_production_at_t(self, usage_coef, time_interval):
        production = 0
        for powerplant_index in range (0, len(self.__observable)):
            if self.__observable[powerplant_index].get_type() != "Demand":
                powerplant = self.__observable[powerplant_index]
                production += (powerplant.get_raw_power() * usage_coef[powerplant_index]) * time_interval
        return production

    def get_unsatisfied_demand_at_t(self, usage_coef, time_index, time_interval, init : int = 0):
        #return ( self.__demand.get_demand_approxima(time_index, time_interval) - self.get_production_at_t(usage_coef, time_interval))
        return ( self.__demand.get_demand_monthly(time_index, time_interval, init = init) - self.get_production_at_t(usage_coef, time_interval))
        
    def get_carbon_production_at_t(self, usage_coef, time_interval):
        carbon_prod = 0
        for powerplant_index in range (0, len(self.__observable)):
            if self.__observable[powerplant_index].get_type() != "Demand":
                powerplant = self.__observable[powerplant_index]
                carbon_prod += (powerplant.get_carbon_production() * usage_coef[powerplant_index] * powerplant.get_raw_power()) * time_interval
        return carbon_prod
        
    def get_carbon_over_production(self, usage_coef, time_interval):
        emited_carbon = 0 # (g)
        total_production = 1
        for t in range(0, len(usage_coef)):
            emited_carbon += self.get_carbon_production_at_t(usage_coef[t], time_interval)
            total_production += self.get_production_at_t(usage_coef[t], time_interval)
        carbon_production = emited_carbon/total_production
        return max(0, carbon_production - self.__carbon_quota) # (g/MWh)

    def get_weighted_coef(self, usage_coef, time_interval, init : int = 0):
        if init == 0 :
            for powerplant_index in range(0, len(usage_coef[0])):                                       
                if self.__observable[powerplant_index].get_type() not in ["Demand"] :  
                    self.__observable[powerplant_index].reset_powerplant()  
        else :
            for powerplant_index in range(0, len(usage_coef[0])):                                        ###########################################
                if self.__observable[powerplant_index].get_type() not in ["Demand","Hydropowerplant"] :  ## Keep previous history stock for hydro ##
                    self.__observable[powerplant_index].reset_powerplant()                               ###########################################

        weighted_coef = usage_coef.copy()
        for t in range(0, len(weighted_coef)):
            for powerplant_index in range(0, len(weighted_coef[t])):
                if self.__observable[powerplant_index].get_type() != "Demand":
                    min_av = self.__observable[powerplant_index].get_min_availability()
                    max_av = self.__observable[powerplant_index].get_max_availability(t, init = init)
                    if max_av < min_av:
                        min_av = 0 # a verifier 
                    weighted_coef[t][powerplant_index] = min_av + weighted_coef[t][powerplant_index]*(max_av-min_av)
                    self.__observable[powerplant_index].back_propagate(weighted_coef[t][powerplant_index], t, time_interval)
        return weighted_coef

    def loss_function(self, usage_coef, time_interval : int = 1) -> float :
        usage_coef = self.arrange_coef_as_array_of_array(usage_coef)
        weighted_coef = self.get_weighted_coef(usage_coef, time_interval=time_interval)
        loss = 0
        for t in range(0, len(weighted_coef)):
            loss += self.get_production_cost_at_t(weighted_coef[t], t, time_interval) + ( self.get_penalisation_cost() * np.abs( self.get_unsatisfied_demand_at_t(weighted_coef[t], t, time_interval)) )
        loss +=  self.get_carbon_cost() * (self.get_carbon_over_production(weighted_coef, time_interval) )
        return loss

    def arrange_coef_as_array_of_array(self, raw_usage_coef):
        ordered_coef = []
        cur_time_coef = []
        for coef_index in range(len(raw_usage_coef)):
            cur_time_coef.append(raw_usage_coef[coef_index])
            ## indice de la premiere powerplant a t+1
            if (coef_index+1)%len(self.__observable) == 0:
                ordered_coef.append(cur_time_coef)
                cur_time_coef = []
        return ordered_coef


    ### OPTiMiZATION
    def __opt_params(self, time_index):
        self.__optimizer.set_parametrization(self.get_opt_params(time_index))
        
    def get_opt_params(self, time_index):
        variable_parametrization = []
        for _ in range(time_index):
            for powerplant_index in range(len(self.__observable)):
                if self.__observable[powerplant_index].get_type() != "Demand":
                    if not self.__observable[powerplant_index].is_tuneable():
                        variable_parametrization += [ng.p.Choice([0.,1.])]
                    else:
                        #check the params by 
                        #print(self.__observable[powerplant_index].get_variation_params())
                        variable_parametrization += [self.__observable[powerplant_index].get_variation_params()]
        return ng.p.Tuple(*variable_parametrization)

    def __reshape_results(self, results, time_interval):
        for tmp in results:
            usage_coef = self.arrange_coef_as_array_of_array(tmp['coef'])
            tmp.update({"coef":self.get_weighted_coef(usage_coef, time_interval)})

        # for powerplant_index in range(0, len(self.__observable)):
        #     try:
        #         print(self.__observable[powerplant_index].get_stock_evolution())
        #     # Not a hydro power plant, so the methode does not exist
        #     except:
        #         pass
        return results

    def optimizeMix(self, carbon_quota: float = None, demand: Demand = None, lost: float = None, 
                    optimizer: Optimizer = None, step : int = 1,
                    time_index: int = 24*7, time_interval: float = 1,
                    penalisation : float = None, carbon_cost : float = None, plot : str = "default", average_wide : int = 0, init : int = 0):

        # init params                
        self.time_index = time_index
        self.__init = init
        # step is the step of opt budget
        self.step = step
        self.time_interval = time_interval
        self.plot = plot
        self.average_wide = average_wide
        if demand is not None : self.set_demand(demand)
        if lost is not None : self.set_constant_lost(lost)
        if penalisation is not None : self.set_penalisation_cost(penalisation)
        if carbon_cost is not None : self.set_carbon_cost(carbon_cost)
        if carbon_quota is not None : self.set_carbon_quota(carbon_quota)
        if optimizer is not None : self.set_optimizer(optimizer)
        
        # tune optimizer parametrization
        self.__opt_params(self.time_index)
        
        #init constraints
        constraints = {}
        constraints.update({"time_interval":self.time_interval})
        
        #let's optimize
        results = self.__optimizer.optimize(mix = self , func_to_optimize = self.loss_function, constraints=constraints, step = self.step, init = self.__init)
        
        results = self.__reshape_results(results, self.time_interval)

        self.plotResults(results, mode = self.plot , time_interval = self.time_interval, time_index =self.time_index, average_wide = self.average_wide)
        
        return results

    def get_params(self) -> dict:
        return {"agents" : self.__observable, "optimizer" : self.get_optimizer(),
                "penalisation_cost" : self.get_penalisation_cost(), "carbon_cost" : self.get_carbon_cost(),
                "demand" : self.__demand, "lost" : self.__lost, "carbon_quota" : self.__carbon_quota,
                "step" : self.step, "time_interval" : self.time_interval, "time_index" : self.time_index,
                "plot" : self.plot, "moving average_wide" : self.average_wide, "initial time_index" : self.__init}

    def set_params(self, carbon_quota: float = None, demand: Demand = None, lost: float = None, 
                    optimizer: Optimizer = None, step : int = 1,
                    time_index: int = 24*7, time_interval: float = 1,
                    penalisation : float = None, carbon_cost : float = None, plot : str = "default", average_wide : int = 0, init : int = 0):

        # init params                
        self.time_index = time_index
        self.__init = init
        # step is the step of opt budget
        self.step = step
        self.time_interval = time_interval
        self.plot = plot
        self.average_wide = average_wide
        if demand is not None : self.set_demand(demand)
        if lost is not None : self.set_constant_lost(lost)
        if penalisation is not None : self.set_penalisation_cost(penalisation)
        if carbon_cost is not None : self.set_carbon_cost(carbon_cost)
        if carbon_quota is not None : self.set_carbon_quota(carbon_quota)
        if optimizer is not None : self.set_optimizer(optimizer)

    def __update_planning(self, original, new, init):
        coef = original[-1]["coef"][:init]
        coef = coef + new[-1]["coef"]
        loss = self.loss_function(coef, self.time_interval)
        usage_coef = self.arrange_coef_as_array_of_array(coef)
        weighted_coef = self.get_weighted_coef(usage_coef, time_interval=self.time_interval])
        production = 0
        u_demand = 0
        for t in range(0, len(weighted_coef)):
            production +=  mix.get_production_cost_at_t(weighted_coef[t], t, self.time_interval)
            u_demand += mix.get_unsatisfied_demand_at_t(weighted_coef[t], t, self.time_interval)
            carbon_prod = self.get_carbon_production_at_t(weighted_coef[t], self.time_interval)

        return [{"loss":loss, "coef":coef, "production":production, "unsatisfied demand":u_demand, "carbon production":carbon_prod}]

    def simulate(events):
        """
            Simulating the mas platform over a specific time index
            'events' parameter must be a dict structured like this : 
                {
                    "code signal":[("name of the powerplant",init),...],
                    ...
                    ...
                }
        """
        ### STEP 1 : initial planning
        self.__planning = self.optimizeMix(carbon_quota = None, demand = self.__demand, lost = self.__cst_lost, 
                                            optimizer = self.__optimizer, step = self.step,
                                            time_index = self.time_index, time_interval = self.time_interval,
                                            penalisation = self.__penalisation_cost, carbon_cost = self.__carbon_cost,
                                            plot = self.plot, average_wide = self.average_wide)

        ### STEP 2 : check the events list
        for key, n_events in events.items():
            if key == "400":
                for value in n_events:
                    for element in get_observable():
                        if element.get_name() == value[0]:
                            element._notify_is_down()
                            ### Relaunch optimizeMix() but with new initial time_index
                            new_next_planning = self.optimizeMix(carbon_quota = None, demand = self.__demand, lost = self.__cst_lost, 
                                                                    optimizer = self.__optimizer, step = self.step,
                                                                    time_index = self.time_index-value[1], time_interval = self.time_interval,
                                                                    penalisation = self.__penalisation_cost, carbon_cost = self.__carbon_cost,
                                                                    plot = self.plot, average_wide = self.average_wide, init = value[1])

                            ### UPDATE self.__planning
                            self.__planning = self.__update_planning(self.__planning, new_next_planning, value[1])

            elif key == "200":
                for value in n_events:
                    for element in get_observable():
                        if element.get_name() == value[0]:
                            element._notify_is_up()
                            ### Relaunch optimizeMix() but with new initial time_index
                            new_next_planning = self.optimizeMix(carbon_quota = None, demand = self.__demand, lost = self.__cst_lost, 
                                                                    optimizer = self.__optimizer, step = self.step,
                                                                    time_index = self.time_index-value[1], time_interval = self.time_interval,
                                                                    penalisation = self.__penalisation_cost, carbon_cost = self.__carbon_cost,
                                                                    plot = self.plot, average_wide = self.average_wide, init = value[1])

                            ### UPDATE self.__planning
                            self.__planning = self.__update_planning(self.__planning, new_next_planning, value[1]) 

        ### STEP 3 : return the final plan
        return self.__planning

    
    
    ###########
    ## PLOTS ##
    ###########    
    def moving_average(self, x, w):
        return np.convolve(x, np.ones(w), 'valid') / w
        
    def plotResults(self, optimum : dict = {} , mode : str = "default", time_interval : float = 1, time_index : float = 1, average_wide : int = 0):
        #set the moving average wide
        if average_wide == 0 :
            average_wide = ceil(len(optimum[-1]["coef"])/4)
    
        if mode == "default" or mode == "save" or mode == "best":
            #set Y of axe 1
            Y: Dict[str,List[float]] ={}
            label_y: List[str]=[]
            sum_prod = []
            for c in self.__observable :
                label_y.append(c.get_name())
                Y.update({c.get_name():[]})
            if mode != "best":
                for array in optimum[-1]["coef"] :
                    sum_t = 0.
                    for enum, value in enumerate(array) :
                        Y[label_y[enum]].append(value)
                        sum_t = sum_t + (value*self.get_observable()[enum].get_raw_power())
                    sum_prod.append(sum_t)
            else :
                ##TODO get best loss
                pass

            
            #set Y of axe 2
            Y_: Dict[str,List[float]] ={} 
            Y_["demand"] = []
            Y_["production"] = sum_prod
            for t_i in range(0,time_index):
                Y_["demand"].append(self.__demand.get_demand_monthly(t_i, time_interval))

            fig, axs = plt.subplots(1, 2, figsize=(12, 6))        
        
            # data integration        
            X = [i for i in range(0,len(optimum[-1]["coef"]))]  
            for n_axs in range(0,2) :
                if n_axs == 0 :
                    for central, value in Y.items():
                        smooth_value = self.moving_average(value,average_wide)
                        axs[n_axs].plot(X[(average_wide - 1):], smooth_value, '.-' ,alpha=0.5, lw=2, label=central)
                elif n_axs == 1 :
                    axs[n_axs].plot(X,Y_["demand"],label="demand")
                    axs[n_axs].plot(X,Y_["production"],label="production")
            
              
            # Add execution_time and loss information  
            info = "production_cost: "+ "{:.3f}".format(optimum[-1]["loss"])+" ; execution_time: "+"{:.3f}".format(optimum[-1]["elapsed_time"])  
            info += "; demand gap: "+"{:.3f}".format(optimum[-1]["unsatisfied demand"])                   
            plt.annotate(info,
                xy=(0.5, 0), xytext=(0, 10),
                xycoords=('axes fraction', 'figure fraction'),
                textcoords='offset points',
                size=10, ha='center', va='bottom')
                
            # plots parametrizations
            for n_axs in range(0,2) :  
                axs[n_axs].grid()
                axs[n_axs].yaxis.set_tick_params(length=0)
                axs[n_axs].xaxis.set_tick_params(length=0)
                axs[n_axs].set_xlabel('hours')
                #axs[n_axs].yaxis.set_major_formatter(StrMethodFormatter("{x}"+units[0]))
                if n_axs == 0 :
                    axs[n_axs].set_ylabel('coef (%)')
                elif n_axs == 1 :
                    axs[n_axs].set_ylabel('MWh')
                axs[n_axs].legend()
                
            fig.tight_layout()
            try :
                path = "results_"+datetime.now().strftime("%d_%m_%Y")
                os.makedirs(path)
                name = path+"/"+"opt_"+str(self.get_optimizer().get_optimizers())+"_"+datetime.now().strftime("%H%M%S")+".png"
                fig.savefig(name)
                if mode == "default" :
                    plt.show()
                
            except OSError:
                warnings.warn("Can't create the directory "+path+" or already exists")
                try : 
                    name = path+"/"+"opt_"+str(self.get_optimizer().get_optimizers())+"_"+datetime.now().strftime("%H%M%S")+".png"
                    fig.savefig(name)
                    if mode == "default" :
                        plt.show()
                except FileNotFoundError:
                    name = "opt_"+str(self.get_optimizer().get_optimizers())+"_"+datetime.now().strftime("%H%M%S")+".png"
                    fig.savefig(name)
                    if mode == "default" :
                        plt.show()

        elif mode == "None" :
            pass
        else :
            warnings.warn("Choose an available option : default, save or None")
            #plt.show()