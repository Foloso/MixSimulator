import nevergrad as ng
import numpy as np # type: ignore
import math
import time
from typing import Type, List

class Optimizer():
    """
        adaptation of nevergrad optimizers to the project + auto-parametrization
    
        list of available: self.getOptimizerList()
        
    """ 
    def __init__(self, opt = [ng.optimizers.OnePlusOne], budget: List[int] = [100], num_worker: int = 1, instrum = ng.p.Array(shape=(2,))):
        self.set_budget(budget)
        self.set_parametrization(instrum)
        self.set_num_worker(num_worker)
        
        ### available optimizers
        self.__available_optimizers = {Type[str]:Type[object]}
        nevergrad_optimizers = list(ng.optimizers.registry.keys())
        for ng_opt in nevergrad_optimizers:
            self.__available_optimizers.update({ng_opt:ng.optimizers.registry[ng_opt]})
  
        convert_opt = []
        for opt_ng in opt:
            if opt_ng in list(self.__available_optimizers.values()):
                convert_opt.append(opt_ng)
                continue
            try:
                convert_opt.append(self.__available_optimizers[str(opt_ng)])
            except:
                raise KeyError(str(opt_ng) + " not available")
        self.__optimizers = convert_opt
        
    def get_available_optimizers(self):
        tmp = Optimizer()
        return tmp.__available_optimizers.keys()
    
    def get_unavailable_optimizers(self):
        tmp = Optimizer()
        result = []
        tmp = tmp.__available_optimizers.keys()
        list = sorted(ng.optimizers.registry.keys())
        for opt in list:
            if opt not in tmp:
                result.append(opt)
        return result
    
    def get_optimizers(self):
        return self.__optimizers
    
    def set_parametrization(self, instrum):
        self.__parametrization = instrum
        
    def get_parametrization(self):
        return self.__parametrization
        
    def set_budget(self,budget: List[int] = [100]):
        #setting budget 
        #possible to do? auto calculate a optimal budget depending of the size of data
        self.__budget = budget
    
    def get_budget(self):
        return self.__budget
    
    def set_num_worker(self,n_work):
        #setting budget 
        #possible to do? auto calculate a optimal budget depending of the size of data
        self.__num_worker = n_work
    
    def get_num_worker(self):
        return self.__num_worker
        
    def get_params(self) -> dict:
        return {"optimizer(s)" : self.__optimizers, "budget(s)" : self.get_budget(),
                "parametrization" : self.get_parametrization(), "num_worker" : self.get_num_worker()}
    
    def optimize(self, mix = None , func_to_optimize = None, constraints = None, step : int = 1, init : int = 0):
        
        #setting budgets
        budgets = self.get_budget()
        
        if len(budgets) != len(self.__optimizers) :
            raise IndexError ("\n The length of budgets and the length of optimizers list should be the same.\n")
        
        total_budget = 0
        for algo_budget in budgets:
            total_budget += algo_budget
        result = []
        start_time = time.time()

        #optimization under constraints
        chaining_algo = ng.optimizers.Chaining(self.__optimizers, budgets[:-1])
        optimizer = chaining_algo(parametrization=self.get_parametrization(), budget = budgets[-1], num_workers=self.get_num_worker())
         
        #let's minimize
        for tmp_budget in range(0, total_budget):
            x = optimizer.ask()
            loss = func_to_optimize(*x.args, constraints["time_interval"],init = init)
            optimizer.tell(x, loss)
            if (tmp_budget+1)%step == 0:
                result_per_budget = {}
                recommendation = optimizer.provide_recommendation()
                result_per_budget.update({"loss": func_to_optimize(recommendation.value, constraints["time_interval"])})
                result_per_budget.update({"coef": recommendation.value})
                
                #Readjustment
                if mix is not None :
                    usage_coef = mix.arrange_coef_as_array_of_array(recommendation.value)
                    try :
                        weighted_coef = mix.get_weighted_coef(usage_coef, time_interval=constraints["time_interval"], init = init)
                    except:
                        weighted_coef = mix.get_weighted_coef(usage_coef, time_interval=constraints["time_interval"])
                    production = 0
                    u_demand = 0
                    carbon_prod = 0
                    for t in range(0, len(weighted_coef)):
                        production +=  mix.get_production_cost_at_t(weighted_coef[t], t, constraints["time_interval"])
                        try:
                            u_demand += np.abs(mix.get_unsatisfied_demand_at_t(weighted_coef[t], t, constraints["time_interval"], init = init))
                        except:
                            u_demand += np.abs(mix.get_unsatisfied_demand_at_t(weighted_coef[t], t, constraints["time_interval"]))
                        carbon_prod += mix.get_carbon_production_at_t(weighted_coef[t], constraints["time_interval"])
                    result_per_budget.update({"production": production})
                    result_per_budget.update({"unsatisfied demand": u_demand})
                    result_per_budget.update({"carbon production": carbon_prod})
                result_per_budget.update({"elapsed_time": time.time() - start_time})
                result.append(result_per_budget)
                
        #TODO --> Check Constraints     
        return result
