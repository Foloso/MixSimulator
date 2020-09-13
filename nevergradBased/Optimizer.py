import nevergrad as ng
import numpy as np
import math

class Optimizer():
    """
        adaptation of nevergrad optimizers to the project + auto-parametrization
    
        list of available: 
        - optimization under constraints with OnePlusOne (opt_OnePlusOne)
    """ 
    def __init__(self):
        self.__max_bound = 1.
        self.set_budget(100)
        self.set_parametrization(2, self.__max_bound)
    
    def __opt_parameters(self, constraints):
        max_bound = self.__max_bound
        for index in range(0, len(constraints["availability"])):
            usage_coef = [0.] * len(constraints["availability"])
            usage_coef[index] = constraints["availability"][index]
            if constraints["production"](usage_coef) > (constraints["demand"]+ constraints["lost"]):
                self.__set_min_loss(constraints)
                tmp_optimizer = Optimizer()
                tmp_optimizer.set_parametrization(len(usage_coef), np.amax(np.array(usage_coef)))
                optimizer = ng.optimizers.OnePlusOne(parametrization=tmp_optimizer.get_parametrization(), budget=100)
                optimizer.parametrization.register_cheap_constraint(lambda x: (np.array(x)>np.array([0]*len(usage_coef))).all() )
                recommendation = optimizer.minimize(self.__min_loss, verbosity=0)
                print(recommendation.value)
                if max_bound > max(recommendation.value):
                    max_bound = max(recommendation.value)
                else:
                    continue
            else:
                continue
        self.__max_bound = max_bound
        
    def __set_min_loss(self, constraints):
        self.__constraints = constraints

    def __min_loss(self, usage_coef):
        return np.abs(self.__constraints["production"](usage_coef) - (self.__constraints["demand"]+ self.__constraints["lost"]))

    def set_parametrization(self,arg, max):
        #setting parametrization for our objective function
        self.__nb = arg
        self.__parametrization=ng.p.Array(shape=(arg,))
        self.__max_bound = max
        self.__parametrization.set_bounds(lower=0, upper=self.__max_bound)
    
    def get_parametrization(self):
        return self.__parametrization
        
    def set_budget(self,budget: int=100):
        #setting budget 
        #possible to do? auto calculate a optimal budget depending of the size of data
        self.__budget = budget
    
    def get_budget(self):
        return self.__budget
    
    def opt_OnePlusOne(self, func_to_optimize, constraints=None):
        result = {}

        # POSSIBLE??
        if (constraints["production"](constraints["availability"]) < (constraints["demand"]+ constraints["lost"])):
            result.update({"carbonProd": constraints["carbonProd"](constraints["availability"])})
            result.update({"production": constraints["production"](constraints["availability"])})
            result.update({"production cost": func_to_optimize(constraints["availability"])})
            result.update({"coef": constraints["availability"]})
            return result

        # find optimum bounds
        self.__opt_parameters(constraints)

        #optimization under constraints with OnePlusOnex
        optimizer = ng.optimizers.OnePlusOne(parametrization=self.get_parametrization(), budget=self.get_budget())
        if constraints != None:
            #if contraint initiate
            try: 
                optimizer.parametrization.register_cheap_constraint(lambda x: constraints["carbonProd"](x) <= constraints["carbonProdLimit"])
                #Environmental constraint
                
            except: #if no contraint assigned
                pass
            try:
                tolerance = 2 * 10**(math.log10(constraints["demand"] + constraints["lost"])-2)
                min_prod = constraints["demand"] + constraints["lost"]
                optimizer.parametrization.register_cheap_constraint(lambda x: np.abs(constraints["production"](x) - min_prod) < tolerance )
                #Demand constraint
            except:
                pass
            try:
                optimizer.parametrization.register_cheap_constraint(lambda x: (np.array(x) <= constraints["availability"]).all())
                #Availability constraint
            except:
                pass
            try:
                fully_used = np.array([1]*len(constraints["availability"])).astype("float64")
                not_used = np.array([0]*len(constraints["availability"])).astype("float64")
                for index in constraints["nonTuneable"]:
                    fully_used[index] = 0.1
                    not_used[index] = 0.1
                optimizer.parametrization.register_cheap_constraint(lambda x: ((np.abs(np.array(x) - constraints["availability"]) <= fully_used) + (x <= not_used)).all())
            except:
                pass
        
        #let's minimize
        recommendation = optimizer.minimize(func_to_optimize, verbosity=0)
        result.update({"carbonProd": constraints["carbonProd"](recommendation.value)})
        result.update({"production": constraints["production"](recommendation.value)})
        result.update({"production cost": func_to_optimize(recommendation.value)})
        result.update({"coef": recommendation.value})
        return result