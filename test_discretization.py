import MixSimulator.MixSimulator as ms 
import MixSimulator.nevergradBased.Optimizer as opt	
#from MixSimulator.Evaluation import EvaluationBudget

opt_CMA = opt.Optimizer(opt = ["CMA"], budget = [100], num_worker = 1) 
opt_CMA_30 = opt.Optimizer(opt = ["CMA"], budget = [20], num_worker = 30)

mix = ms.MixSimulator()
mix.set_data_csv("MixSimulator/data/RIToamasina/dataset_RI_Toamasina.csv",delimiter=",")
mix.set_variation_csv("MixSimulator/data/RIToamasina/dataset_RI_Toamasina_variation.csv",delimiter=",")
#CHECK params name
#params = mix.get_opt_params(2)
#print("**************************")
#print(params.name)
#params.set_name("rename")
#print(params.name)

print(mix.optimizeMix(99999999999999999999,optimizer = opt_CMA, step = 100, time_index = 24, penalisation = 100, carbon_cost = 10),"num_worker <------------ 1")
#print(mix.optimizeMix(99999999999999999999,optimizer = opt_CMA_30, step = 5, time_index = 168),"num_worker <------------ 30")

#eva=EvaluationBudget()
#eva.evaluate(mix,10,1000,optimizer_list = ["OnePlusOne","DE","CMA","PSO","NGOpt"], indicator_list = ["loss","elapsed_time"],carbonProdLimit = 9999999999999, time_index = 12, penalisation = 100, carbon_cost = 10)
