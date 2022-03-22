from MixSimulator import ElectricityMix
import MixSimulator.nevergradBased.Optimizer as opt	

""" 
(1) Configure nevergrad optimizers 

    Default Parameters :
    ----------
    opt = [ng.optimizers.OnePlusOne], 
    budget: List[int] = [100], 
    num_worker: int = 1, 
    instrum = ng.p.Array(shape=(2,))
"""
opt_CMA = opt.Optimizer(opt = ["CMA"], budget = [20], num_worker = 1) 
opt_CMA_30 = opt.Optimizer(opt = ["CMA"], budget = [20], num_worker = 30)

""" 
(2) Init MixSimulator instance :
    Case one [Default] : "classic" method (see test_classic.py for more use case)
    Case two : "MAS" or Multi Agent System method
"""

classic_mix = ElectricityMix(method="classic",carbon_cost=0,penalisation_cost=100) 
mas_mix = ElectricityMix(method="MAS",carbon_cost=0,penalisation_cost=100)