import mixsimulator.MixSimulator as ms 
import mixsimulator.nevergradBased.Optimizer as opt	
from mixsimulator.Evaluation import EvaluationBudget
from .demand.classic.Demand import Demand

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
(2) Init MixSimulator instance 
"""
mix = ms.MixSimulator()


"""
(3) Set dataset to use
    - all datasets available on : 
        https://github.com/Foloso/MixSimulator/tree/master/data/RIToamasina

"""
mix.set_data_csv("data/RIToamasina/dataset_RI_Toamasina_v2.csv",delimiter=";")

### or use it for default dataset (RI_Toamasina version 2)
#mix.set_data_to("Toamasina")

"""
(4) For variation limits dataset, there is not yet default dataset 
    - the "dataset_RI_Toamasina_variation_template.csv" is a random dataset
    - Description (fr): 
        COLONNES	DESCRIPTION
        --------    --------------------------------------------------------
        centrals	Nom ou identifiant de la centrale
        lower	    Les bornes inférieurs des variations continue (en %)
        upper	    Les bornes supérieurs des variations continue (en  %)
        discrete	Les valeurs discrètes des variations fixes des centrales

"""
mix.set_variation_csv("data/RIToamasina/dataset_RI_Toamasina_variation_template.csv",delimiter=";")


"""
(5) Load the dataset demand to use : based on a monthly data (column "Total Ventes") from 2008 to 2017
    Beyond that date it's a forecasting by prophet!
    - data available on : 
        https://github.com/Foloso/MixSimulator/tree/master/data/RIToamasina/demand

"""
demand = Demand()
data_demand = demand.set_data_csv("data/RIToamasina/DIR-TOAMASINA_concat.csv", delimiter = ",")
"""
    The method must get a dataset with at least 3 columns
    - month : int, 
    - year : int,
    - the monthly demand in kwh (determinated by the parameter "column")
            
    The method also use a forcast model from prophet to predict future demand.
    The periods can be set by set_forcast_periods.
"""
#or for default dataset
#demand.set_data_to("Toamasina",delimiter=",")

""" 
(6) Then set the demand 
"""
mix.set_demand(demand)

""" 
(7) OPTIMIZATION :
    
    Default parameters :
    ---------------------------
    carbon_quota: float = None,     --> carbon limitation (example : 99999999999999999999)
    demand: Demand = None,          --> you can use it to fix a constant demand for each time step (eliminates (5))
    lost: float = None,             --> you can use it to fix a constant lost for each time step
    optimizer: Optimizer = None,    --> nevergrad optimizer initiate in (1)
    step : int = 1,                 --> the number of step of budget where each time the candidates are registered
    time_index: int = 24*7,         --> duration over which we optimize (in hour)
    time_interval: float = 1,       --> the number of step of time where we evaluate the loss function (by default each 1 hour)
    penalisation : float = None,    --> penalisation cost 
    carbon_cost : float = None,     --> penalisation cost of carbon_quota
    plot : str = "default",         --> write "None" for no plot
    average_wide : int = 0          --> average_wide of moving average plot parameter
    
    Output: 
    -------
    List of results in each step of budget (here step = 20, that means only one step cause budget is set to 20)
    --> each result is a dict of "loss", "coef", "production", "unsatisfied demand", "carbon production" and "elapsed_time"

"""
print(mix.optimizeMix(1e10,optimizer = opt_CMA, step = 20, penalisation = 100, carbon_cost = 0, time_index = 168, plot = "None"),"num_worker <------------ 1")
print(mix.optimizeMix(1e10,optimizer = opt_CMA_30, step = 20, penalisation = 100, carbon_cost = 0, time_index = 168, plot = "None"),"num_worker <------------ 30")
### Get all parameters used by the mix 
print(mix.get_params())

""" 
(8) Evaluation of results by budget for each selected optimizer
    Default parameters :
    --------------------
    mix,                            --> the mix to evaluate
    sequence,                       --> each budget to evaluate
    max_budgets, 
    optimizer_list: List['str'],    
    indicator_list: List['str'],    --> indicators are ["loss","elapsed_time","production","unsatisfied demand","carbon production"]
    num_worker: int = 1, 
    bind: str = None,               --> path to dataset
    time_index: int = 24, 
    carbonProdLimit: float = 39500000000,   --> equal to carbon_quota
    time_interval : float = 1, 
    average_wide : int = 0, 
    penalisation : float = 1000000000000,   --> equal to penalisation cost
    carbon_cost: float = 0
"""
eva=EvaluationBudget()
eva.evaluate(mix,10,100,optimizer_list = ["OnePlusOne","DE","CMA","PSO","NGOpt"], indicator_list = ["loss","elapsed_time","production","unsatisfied demand","carbon production"],carbonProdLimit = 1e10, time_index = 24, penalisation = 100, carbon_cost = 10)
