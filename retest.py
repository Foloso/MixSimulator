# Two way to import from package mixsimulator
#import mixsimulator.MixSimulator as ms
#from mixsimulator.Evaluation import Evaluation

#Way to import from local
import MixSimulator.MixSimulator as ms 
import MixSimulator.nevergradBased.Optimizer as opt
from MixSimulator.Evaluation import EvaluationBudget

#opt_CMA = opt.Optimizer(opt = ["OnePlusOne"], budget = [20], num_worker = 1) 
#opt_CMA_30 = opt.Optimizer(opt = ["OnePlusOne"], budget = [20], num_worker = 30)

mix = ms.MixSimulator()
mix.set_data_csv("MixSimulator/data/RIToamasina/dataset_RI_Toamasina.csv")

#print(mix.optimizeMix(99999999999999999999,optimizer = opt_CMA, step = 5),"num_worker <------------ 1")
#print(mix.optimizeMix(99999999999999999999,optimizer = opt_CMA_30, step = 5),"num_worker <------------ 30")

eva=EvaluationBudget()
eva.evaluate(mix,10,40,optimizer_list = ["OnePlusOne","DE"], indicator_list = ["loss","elapsed_time"],carbonProdLimit = 9999999999999999999999, time_index = 3)
