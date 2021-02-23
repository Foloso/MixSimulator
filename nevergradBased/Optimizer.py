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
            self.__available_optimizers.update({ng_opt:getattr(ng.optimizers, ng_opt)})
        # #self.__available_optimizers.update({"NGOptRL":ng.optimizers.NGOptRL})
        # self.__available_optimizers.update({"ASCMA2PDEthird":ng.optimizers.ASCMA2PDEthird})
        # self.__available_optimizers.update({"ASCMADEQRthird":ng.optimizers.ASCMADEQRthird})
        # self.__available_optimizers.update({"ASCMADEthird":ng.optimizers.ASCMADEthird})
        # self.__available_optimizers.update({"AdaptiveDiscreteOnePlusOne":ng.optimizers.AdaptiveDiscreteOnePlusOne})
        # self.__available_optimizers.update({"CMandAS":ng.optimizers.CMandAS})
        # self.__available_optimizers.update({"CMandAS2":ng.optimizers.CMandAS2})
        # self.__available_optimizers.update({"CMandAS3":ng.optimizers.CMandAS3})
        # self.__available_optimizers.update({"Cobyla":ng.optimizers.Cobyla})
        # self.__available_optimizers.update({"DiagonalCMA":ng.optimizers.DiagonalCMA})
        # self.__available_optimizers.update({"DiscreteBSOOnePlusOne":ng.optimizers.DiscreteBSOOnePlusOne})
        # self.__available_optimizers.update({"EDA":ng.optimizers.EDA})
        # self.__available_optimizers.update({"MEDA":ng.optimizers.MEDA})
        # self.__available_optimizers.update({"MPCEDA":ng.optimizers.MPCEDA})
        # self.__available_optimizers.update({"MetaModel":ng.optimizers.MetaModel})
        # self.__available_optimizers.update({"MixES":ng.optimizers.MixES})
        # self.__available_optimizers.update({"MultiCMA":ng.optimizers.MultiCMA})
        # self.__available_optimizers.update({"PCEDA":ng.optimizers.PCEDA})
        # self.__available_optimizers.update({"PolyCMA":ng.optimizers.PolyCMA})
        # self.__available_optimizers.update({"RecMixES":ng.optimizers.RecMixES})
        # self.__available_optimizers.update({"RotationInvariantDE":ng.optimizers.RotationInvariantDE})
        # self.__available_optimizers.update({"TripleCMA":ng.optimizers.TripleCMA})
        # self.__available_optimizers.update({"NGOpt":ng.optimizers.NGOpt})
        # self.__available_optimizers.update({"cGA":ng.optimizers.cGA})
        # self.__available_optimizers.update({"SplitOptimizer":ng.optimizers.SplitOptimizer})
        # self.__available_optimizers.update({"RecombiningPortfolioOptimisticNoisyDiscreteOnePlusOne":ng.optimizers.RecombiningPortfolioOptimisticNoisyDiscreteOnePlusOne})
        # self.__available_optimizers.update({"RecES":ng.optimizers.RecES})
        # self.__available_optimizers.update({"RealSpacePSO":ng.optimizers.RealSpacePSO})
        # self.__available_optimizers.update({"RandomSearchPlusMiddlePoint":ng.optimizers.RandomSearchPlusMiddlePoint})
        # self.__available_optimizers.update({"QrDE":ng.optimizers.QrDE})
        # self.__available_optimizers.update({"QORandomSearch":ng.optimizers.QORandomSearch})
        # self.__available_optimizers.update({"OptimisticNoisyOnePlusOne":ng.optimizers.OptimisticNoisyOnePlusOne})
        # self.__available_optimizers.update({"OptimisticDiscreteOnePlusOne":ng.optimizers.OptimisticDiscreteOnePlusOne})
        # self.__available_optimizers.update({"ORandomSearch":ng.optimizers.ORandomSearch})
        # self.__available_optimizers.update({"NoisyOnePlusOne":ng.optimizers.NoisyOnePlusOne})
        # self.__available_optimizers.update({"NoisyDiscreteOnePlusOne":ng.optimizers.NoisyDiscreteOnePlusOne})
        # self.__available_optimizers.update({"NoisyDE":ng.optimizers.NoisyDE})
        # self.__available_optimizers.update({"NoisyBandit":ng.optimizers.NoisyBandit})
        # self.__available_optimizers.update({"NelderMead":ng.optimizers.NelderMead})
        # self.__available_optimizers.update({"NaiveTBPSA":ng.optimizers.NaiveTBPSA})
        # self.__available_optimizers.update({"NaiveIsoEMNA":ng.optimizers.NaiveIsoEMNA})
        # self.__available_optimizers.update({"LhsDE":ng.optimizers.LhsDE})
        # self.__available_optimizers.update({"FCMA":ng.optimizers.FCMA})
        # self.__available_optimizers.update({"ES":ng.optimizers.ES})
        # self.__available_optimizers.update({"DoubleFastGADiscreteOnePlusOne":ng.optimizers.DoubleFastGADiscreteOnePlusOne})
        # self.__available_optimizers.update({"DiscreteOnePlusOne":ng.optimizers.DiscreteOnePlusOne})
        # self.__available_optimizers.update({"CauchyOnePlusOne":ng.optimizers.CauchyOnePlusOne})
        # self.__available_optimizers.update({"CM":ng.optimizers.CM})
        # self.__available_optimizers.update({"AlmostRotationInvariantDE":ng.optimizers.AlmostRotationInvariantDE})
        # self.__available_optimizers.update({"TwoPointsDE":ng.optimizers.TwoPointsDE})
        # self.__available_optimizers.update({"RandomSearch":ng.optimizers.RandomSearch})
        # self.__available_optimizers.update({"OnePlusOne":ng.optimizers.OnePlusOne})
        # self.__available_optimizers.update({"DE":ng.optimizers.DE})
        # self.__available_optimizers.update({"CMA":ng.optimizers.CMA})
        # self.__available_optimizers.update({"PSO":ng.optimizers.PSO})
        # self.__available_optimizers.update({"TBPSA":ng.optimizers.TBPSA})
        # self.__available_optimizers.update({"LHSSearch":ng.optimizers.LHSSearch})
        # self.__available_optimizers.update({"CauchyLHSSearch":ng.optimizers.CauchyLHSSearch})
        # self.__available_optimizers.update({"CauchyScrHammersleySearch":ng.optimizers.CauchyScrHammersleySearch})
        
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
    
    def optimize(self, mix = None , func_to_optimize = None, constraints = None, step : int = 1):
        
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
            loss = func_to_optimize(*x.args, constraints["time_interval"])
            optimizer.tell(x, loss)
            if (tmp_budget+1)%step == 0:
                result_per_budget = {}
                recommendation = optimizer.provide_recommendation()
                result_per_budget.update({"loss": func_to_optimize(recommendation.value, constraints["time_interval"])})
                result_per_budget.update({"coef": recommendation.value})
                
                #Readjustment
                if mix is not None :
                    usage_coef = mix.arrange_coef_as_array_of_array(recommendation.value)
                    weighted_coef = mix.get_weighted_coef(usage_coef, time_interval=constraints["time_interval"])
                    production = 0
                    u_demand = 0
                    for t in range(0, len(weighted_coef)):
                        production +=  mix.get_production_cost_at_t(weighted_coef[t], t, constraints["time_interval"])
                        u_demand = mix.get_unsatisfied_demand_at_t(weighted_coef[t], t, constraints["time_interval"])
                    result_per_budget.update({"production": production})
                    result_per_budget.update({"unsatisfied demand": u_demand})
                    result_per_budget.update({"carbon production": mix.get_carbon_production_at_t(weighted_coef[t], constraints["time_interval"])})
                result_per_budget.update({"elapsed_time": time.time() - start_time})
                result.append(result_per_budget)
                
        #TODO --> Check Constraints     
        return result
