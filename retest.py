import mixsimulator.MixSimulator as ms 
import mixsimulator.nevergradBased.Optimizer as opt	
from mixsimulator.Evaluation import EvaluationBudget

opt_CMA = opt.Optimizer(opt = ["CMA"], budget = [20], num_worker = 1) 
opt_CMA_30 = opt.Optimizer(opt = ["CMA"], budget = [20], num_worker = 30)

mix = ms.MixSimulator()
mix.set_data_to("MixSimulator/data/RIToamasina/dataset_RI_Toamasina.csv")

print(mix.optimizeMix(99999999999999999999,optimizer = opt_CMA, step = 5, time_index = 168),"num_worker <------------ 1")
print(mix.optimizeMix(99999999999999999999,optimizer = opt_CMA_30, step = 5, time_index = 168),"num_worker <------------ 30")

eva=EvaluationBudget()
eva.evaluate(mix,10,1000,optimizer_list = ["OnePlusOne","DE","CMA","PSO","NGOpt"], indicator_list = ["loss","elapsed_time"],carbonProdLimit = 9999999999999, time_index = 12, penalisation = 100, carbon_cost = 10)
