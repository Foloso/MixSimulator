import mixsimulator.MixSimulator as ms 
import mixsimulator.nevergradBased.Optimizer as opt	
from mixsimulator.Evaluation import EvaluationBudget
import mixsimulator.Demand as dm

#Configure nevergrad optimizers
opt_CMA = opt.Optimizer(opt = ["CMA"], budget = [20], num_worker = 1) 
opt_CMA_30 = opt.Optimizer(opt = ["CMA"], budget = [20], num_worker = 30)

#Init MixSimulator instance
mix = ms.MixSimulator()

#Set data to use
mix.set_data_csv("MixSimulator/data/RIToamasina/dataset_RI_Toamasina_v2.csv",delimiter=";")
#or for default dataset
#mix.set_data_to("Toamasina")

#For variation limits dataset, there is not yet default dataset 
# mix.set_variation_csv("MixSimulator/data/RIToamasina/dataset_RI_Toamasina_variation_template.csv",delimiter=";")

demand = dm.Demand()
data_demand = demand.set_data_csv("MixSimulator/data/RIToamasina/DIR-TOAMASINA_concat.csv", delimiter = ",")
#or for default dataset
#demand.set_data_to("Toamasina",delimiter=",")

mix.set_demand(demand)

#Optimize the mix
print(mix.optimizeMix(99999999999999999999,optimizer = opt_CMA, step = 5, time_index = 168),"num_worker <------------ 1")
print(mix.optimizeMix(99999999999999999999,optimizer = opt_CMA_30, step = 5, time_index = 168),"num_worker <------------ 30")

#Evaluation of budget
eva=EvaluationBudget()
eva.evaluate(mix,10,1000,optimizer_list = ["OnePlusOne","DE","CMA","PSO","NGOpt"], indicator_list = ["loss","elapsed_time","production","unsatisfied demand","carbon production"],carbonProdLimit = 9999999999999, time_index = 12, penalisation = 100, carbon_cost = 10)
