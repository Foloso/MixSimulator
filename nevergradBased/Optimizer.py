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

        ### available optimizers
        self.__available_optimizers = {}
        self.__available_optimizers.update({"cGA":ng.optimizers.cGA})
        self.__available_optimizers.update({"SplitOptimizer":ng.optimizers.SplitOptimizer})
        self.__available_optimizers.update({"RecombiningPortfolioOptimisticNoisyDiscreteOnePlusOne":ng.optimizers.RecombiningPortfolioOptimisticNoisyDiscreteOnePlusOne})
        self.__available_optimizers.update({"RecES":ng.optimizers.RecES})
        self.__available_optimizers.update({"RealSpacePSO":ng.optimizers.RealSpacePSO})
        self.__available_optimizers.update({"RandomSearchPlusMiddlePoint":ng.optimizers.RandomSearchPlusMiddlePoint})
        self.__available_optimizers.update({"QrDE":ng.optimizers.QrDE})
        self.__available_optimizers.update({"QORandomSearch":ng.optimizers.QORandomSearch})
        self.__available_optimizers.update({"OptimisticNoisyOnePlusOne":ng.optimizers.OptimisticNoisyOnePlusOne})
        self.__available_optimizers.update({"OptimisticDiscreteOnePlusOne":ng.optimizers.OptimisticDiscreteOnePlusOne})
        self.__available_optimizers.update({"ORandomSearch":ng.optimizers.ORandomSearch})
        self.__available_optimizers.update({"NoisyOnePlusOne":ng.optimizers.NoisyOnePlusOne})
        self.__available_optimizers.update({"NoisyDiscreteOnePlusOne":ng.optimizers.NoisyDiscreteOnePlusOne})
        self.__available_optimizers.update({"NoisyDE":ng.optimizers.NoisyDE})
        self.__available_optimizers.update({"NoisyBandit":ng.optimizers.NoisyBandit})
        self.__available_optimizers.update({"NelderMead":ng.optimizers.NelderMead})
        self.__available_optimizers.update({"NaiveTBPSA":ng.optimizers.NaiveTBPSA})
        self.__available_optimizers.update({"NaiveIsoEMNA":ng.optimizers.NaiveIsoEMNA})
        self.__available_optimizers.update({"LhsDE":ng.optimizers.LhsDE})
        self.__available_optimizers.update({"FCMA":ng.optimizers.FCMA})
        self.__available_optimizers.update({"ES":ng.optimizers.ES})
        self.__available_optimizers.update({"DoubleFastGADiscreteOnePlusOne":ng.optimizers.DoubleFastGADiscreteOnePlusOne})
        self.__available_optimizers.update({"DiscreteOnePlusOne":ng.optimizers.DiscreteOnePlusOne})
        self.__available_optimizers.update({"CauchyOnePlusOne":ng.optimizers.CauchyOnePlusOne})
        self.__available_optimizers.update({"CM":ng.optimizers.CM})
        self.__available_optimizers.update({"AlmostRotationInvariantDE":ng.optimizers.AlmostRotationInvariantDE})
        self.__available_optimizers.update({"TwoPointsDE":ng.optimizers.TwoPointsDE})
        self.__available_optimizers.update({"RandomSearch":ng.optimizers.RandomSearch})
        self.__available_optimizers.update({"OnePlusOne":ng.optimizers.OnePlusOne})
        self.__available_optimizers.update({"DE":ng.optimizers.DE})
        self.__available_optimizers.update({"CMA":ng.optimizers.CMA})
        self.__available_optimizers.update({"PSO":ng.optimizers.PSO})
        self.__available_optimizers.update({"TBPSA":ng.optimizers.TBPSA})
    
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
        
    def getOptimizerList(self):
        tmp = Optimizer()
        return tmp.__available_optimizers.keys()
    
    def get_budget(self):
        return self.__budget
    
    def set_satisfied_constraints(self, recommendation_value, constraints, min_prod, tolerance, fully_used, not_used):    
        #check satisfied constraints
        self.__check_constraints=[]
        items={}
        if constraints["carbonProd"](recommendation_value) <= constraints["carbonProdLimit"]:
            check=True
        else : check = False
        items.update({"carbon_constraint_satisfied": check})
        items.update({"value": constraints["carbonProd"](recommendation_value)})
        items.update({"constraint": constraints["carbonProdLimit"]})
        self.__check_constraints.append(items)
        
        items={}
        if np.abs(constraints["production"](recommendation_value) - min_prod) < tolerance:
            check=True
        else : check = False
        items.update({"demand_constraint_satisfied": check})
        items.update({"value": constraints["production"](recommendation_value)})
        items.update({"constraint": min_prod})
        self.__check_constraints.append(items)
        
        items={}
        if (np.array(recommendation_value) <= constraints["availability"]).all() :
            check=True
        else : check = False
        items.update({"availability_constraint_satisfied": check})
        items.update({"value": np.array(recommendation_value)})
        items.update({"constraint": constraints["availability"]})
        self.__check_constraints.append(items)
        
        items={}
        if (np.abs(np.array(recommendation_value) - constraints["availability"]) <= fully_used).all() and ((recommendation_value <= not_used)).all() :
            check=True
        else : check = False
        items.update({"used_constraint_satisfied": check})
        items.update({"value": [np.abs(np.array(recommendation_value) - constraints["availability"]),recommendation_value]})
        items.update({"constraint": [fully_used, not_used]})
        self.__check_constraints.append(items) 
    
    def get_satisfied_constraints(self):
        return self.__check_constraints
        
    def show_satisfied_constraints(self):
        print("**************************************************************************************************")
        for i in self.__check_constraints:
            print(i)
            print("**************************************************************************************************")
    
    def opt_With(self, func_to_optimize, constraints = None, optimizers : list = ["OnePlusOne"], budgets : list = [100]):
        #Define chaining algo  
        self.__optimizers = []
        for opt in optimizers:
            try:
                self.__optimizers.append(self.__available_optimizers.get(opt))
            except KeyError:
                print(opt, "not included. Use of default optimizer instead.\n Please use one of availible optimizer :\n \t (non exhaustive optimizer list, more will be added)\nFor more informations, check https://facebookresearch.github.io/nevergrad/optimizers_ref.html")
                self.__optimizers = [ng.optimizers.OnePlusOne]
                budgets=[100]
                
        if len(budgets) != len(optimizers) :
            print("\n The length of budgets and the length of optimizers should be the same. Use of default optimizer instead.\n")
            budgets=[100]
            self.__optimizers = [ng.optimizers.OnePlusOne]
            
        
        #setting budgets
        self.set_budget(budgets[-1])
        current_budgets = budgets[:-1]
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

        #optimization under constraints
        chaining_algo = ng.optimizers.Chaining(self.__optimizers,current_budgets)
        optimizer = chaining_algo(parametrization=self.get_parametrization(), budget=self.get_budget())
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
        
        self.set_satisfied_constraints(recommendation.value, constraints, min_prod, tolerance, fully_used, not_used)
        self.show_satisfied_constraints()        
        
        return result
