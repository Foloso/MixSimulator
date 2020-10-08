import nevergrad as ng
import numpy as np
import math
import time

class Optimizer():
    """
        adaptation of nevergrad optimizers to the project + auto-parametrization
    
        list of available: self.getOptimizerList()
        
    """ 
    def __init__(self):
        self.__max_bound = 1.
        self.set_budget(100)
        self.set_parametrization(ng.p.Array(shape=(2,)), self.__max_bound)

        ### available optimizers
        self.__available_optimizers = {}
        self.__available_optimizers.update({"ASCMA2PDEthird":ng.optimizers.ASCMA2PDEthird})
        self.__available_optimizers.update({"ASCMADEQRthird":ng.optimizers.ASCMADEQRthird})
        self.__available_optimizers.update({"ASCMADEthird":ng.optimizers.ASCMADEthird})
        self.__available_optimizers.update({"AdaptiveDiscreteOnePlusOne":ng.optimizers.AdaptiveDiscreteOnePlusOne})
        self.__available_optimizers.update({"CMandAS":ng.optimizers.CMandAS})
        self.__available_optimizers.update({"CMandAS2":ng.optimizers.CMandAS2})
        self.__available_optimizers.update({"CMandAS3":ng.optimizers.CMandAS3})
        self.__available_optimizers.update({"Cobyla":ng.optimizers.Cobyla})
        self.__available_optimizers.update({"DiagonalCMA":ng.optimizers.DiagonalCMA})
        self.__available_optimizers.update({"DiscreteBSOOnePlusOne":ng.optimizers.DiscreteBSOOnePlusOne})
        self.__available_optimizers.update({"EDA":ng.optimizers.EDA})
        self.__available_optimizers.update({"MEDA":ng.optimizers.MEDA})
        self.__available_optimizers.update({"MPCEDA":ng.optimizers.MPCEDA})
        self.__available_optimizers.update({"MetaModel":ng.optimizers.MetaModel})
        self.__available_optimizers.update({"MixES":ng.optimizers.MixES})
        self.__available_optimizers.update({"MultiCMA":ng.optimizers.MultiCMA})
        self.__available_optimizers.update({"PCEDA":ng.optimizers.PCEDA})
        self.__available_optimizers.update({"PolyCMA":ng.optimizers.PolyCMA})
        self.__available_optimizers.update({"RecMixES":ng.optimizers.RecMixES})
        self.__available_optimizers.update({"RotationInvariantDE":ng.optimizers.RotationInvariantDE})
        self.__available_optimizers.update({"TripleCMA":ng.optimizers.TripleCMA})
        self.__available_optimizers.update({"NGOpt":ng.optimizers.NGOpt})
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
        self.__available_optimizers.update({"LHSSearch":ng.optimizers.LHSSearch})
        self.__available_optimizers.update({"CauchyLHSSearch":ng.optimizers.CauchyLHSSearch})
        self.__available_optimizers.update({"CauchyScrHammersleySearch":ng.optimizers.CauchyScrHammersleySearch})
    
    def __opt_parameters(self, constraints):
        max_bound = self.__max_bound
        for index in range(0, len(constraints["availability"])):
            usage_coef = [0.] * len(constraints["availability"])
            usage_coef[index] = constraints["availability"][index]
            if constraints["production"](usage_coef) > (constraints["demand"]+ constraints["lost"]):
                self.__set_min_loss(constraints)
                tmp_optimizer = Optimizer()
                tmp_optimizer.set_parametrization(ng.p.Array(shape=(len(usage_coef),)), np.amax(np.array(usage_coef)))
                optimizer = ng.optimizers.OnePlusOne(parametrization=tmp_optimizer.get_parametrization(), budget=100)
                optimizer.parametrization.register_cheap_constraint(lambda x: (np.array(x)>np.array([0]*len(usage_coef))).all() )
                recommendation = optimizer.minimize(self.__min_loss, verbosity=0)
                if max_bound > max(recommendation.value):
                    max_bound = max(recommendation.value)
                else:
                    continue
            else:
                continue
        # if (constraints["demand"]+ constraints["lost"]) <= 1:
        #     max_bound = 0.000000000000000000000000001
        self.__max_bound = max_bound
        self.__parametrization.set_bounds(lower=0, upper=self.__max_bound)
        
    def __set_min_loss(self, constraints):
        self.__constraints = constraints

    def __min_loss(self, usage_coef):
        return np.abs(self.__constraints["production"](usage_coef) - (self.__constraints["demand"]+ self.__constraints["lost"]))

    def set_parametrization(self,instrum, max):
        #setting parametrization for our objective function
        #self.__parametrization=ng.p.Array(shape=(instrum,))
        self.__parametrization = instrum
        self.__max_bound = max
    
    def get_parametrization(self):
        return self.__parametrization
        
    def set_budget(self,budget: int=100):
        #setting budget 
        #possible to do? auto calculate a optimal budget depending of the size of data
        self.__budget = budget
    
    def get_budget(self):
        return self.__budget
        
    def getOptimizerList(self):
        tmp = Optimizer()
        return tmp.__available_optimizers.keys()
    
    def getNonAvailableOptimizers(self):
        tmp = Optimizer()
        result = []
        tmp = tmp.__available_optimizers.keys()
        list = sorted(ng.optimizers.registry.keys())
        for opt in list:
            if opt not in tmp:
                result.append(opt)
        return result

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
        if ((np.abs(np.array(recommendation_value) - constraints["availability"]) <= fully_used) + (recommendation_value <= not_used)).all() :       
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
        for checking in self.__check_constraints:
            print(checking)
            print("**************************************************************************************************")
    
    def opt_With(self, func_to_optimize, constraints = None, optimizers : list = ["OnePlusOne"], budgets : list = [100], step : int = 1):
        #Define chaining algo  
        self.__optimizers = []
        for opt in optimizers:
            self.__optimizers.append(self.__available_optimizers.get(opt))
            if None in self.__optimizers:
                print (opt, "optimizer not included. Please Choose one of availible optimizer :\n \t ",self.getOptimizerList(),
                "\n\n (non exhaustive optimizer list, more will be added)\nFor more informations, check https://facebookresearch.github.io/nevergrad/optimizers_ref.html\n")
                raise NameError(opt, "optimizer not included") 
                
        if len(budgets) != len(optimizers) :
            raise IndexError ("\n The length of budgets and the length of optimizers list should be the same.\n")
        
        #setting budgets
        current_budgets = budgets
        self.set_budget(current_budgets[-1])
        
        total_budget = 0
        for algo_budget in budgets:
            total_budget += algo_budget
        result = []
        start_time = time.time()

        # POSSIBLE??
        if (constraints["production"](constraints["availability"]) < (constraints["demand"]+ constraints["lost"])):
            result_per_budget = {}
            result_per_budget.update({"carbonProd": constraints["carbonProd"](constraints["availability"])})
            result_per_budget.update({"production": constraints["production"](constraints["availability"])})
            result_per_budget.update({"production_cost": func_to_optimize(constraints["availability"])})
            result_per_budget.update({"coef": constraints["availability"]})
            result_per_budget.update({"elapsed_time": time.time() - start_time})
            for tmp_budget in range(0, total_budget):
                if (tmp_budget+1)%step == 0:
                    result.append(result_per_budget)
            return result

        # find optimum bounds & optimizer initialization
        self.__opt_parameters(constraints)

        #optimization under constraints
        chaining_algo = ng.optimizers.Chaining(self.__optimizers,current_budgets[:-1])
        optimizer = chaining_algo(parametrization=self.get_parametrization(), budget=self.get_budget())
        if constraints != None:
            #Environmental constraint
            try: 
                optimizer.parametrization.register_cheap_constraint(lambda x: constraints["carbonProd"](x) <= constraints["carbonProdLimit"])
                
            except: #if no contraint assigned
                pass
            
            # try:
            #     tolerance = 2 * 10**(math.log10(constraints["demand"] + constraints["lost"])-2)
            #     min_prod = constraints["demand"] + constraints["lost"]
            #     optimizer.parametrization.register_cheap_constraint(lambda x: np.abs(constraints["production"](x) - min_prod) < tolerance )
            #     #Demand constraint
            # except:
            #     pass
            
            #Availability constraint
            try:
                optimizer.parametrization.register_cheap_constraint(lambda x: (np.array(x) <= constraints["availability"]).all())
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
        # recommendation = optimizer.minimize(func_to_optimize, verbosity=0)
        optimizer.suggest([0.]*len(constraints["availability"]))
        for tmp_budget in range(0, total_budget):
            x = optimizer.ask()
            loss = func_to_optimize(*x.args, **x.kwargs) + 1000000000000 * np.abs(constraints["production"](*x.args, **x.kwargs) - constraints["demand"] + constraints["lost"])
            optimizer.tell(x, loss)
            if (tmp_budget+1)%step == 0:
                result_per_budget = {}
                recommendation = optimizer.provide_recommendation()
                result_per_budget.update({"carbonProd": constraints["carbonProd"](recommendation.value)})
                result_per_budget.update({"production": constraints["production"](recommendation.value)})
                result_per_budget.update({"production_cost": func_to_optimize(recommendation.value)})
                result_per_budget.update({"coef": recommendation.value})
                result_per_budget.update({"elapsed_time": time.time() - start_time})
                result.append(result_per_budget)
        #print(recommendation.satisfies_constraints())
        
        #TODO
        # self.set_satisfied_constraints(recommendation.value, constraints, min_prod, tolerance, fully_used, not_used)
        #self.show_satisfied_constraints()        
        return result
