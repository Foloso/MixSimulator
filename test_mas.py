import threading
from MixSimulator import ElectricityMix
from MixSimulator.Evaluation import EvaluationBudget
import MixSimulator.nevergradBased.Optimizer as opt
import time
from MixSimulator.agents.Moderator import StoppableThread

"""
    (0) Check the thread running in background
"""
def check_thread_running():
    list_ = []
    while True:
        tmp = threading.enumerate().copy()
        if tmp != list_:
            list_ = tmp
            for thread in list_:
                if thread.is_alive():
                    print("THREAD:  " + thread.name)
        time.sleep(10)

thread_checker = StoppableThread(target=check_thread_running, name="thread_checker")
thread_checker.start()

""" 
(1) Configure nevergrad optimizers 

    Default Parameters :
    ----------
    opt = [ng.optimizers.OnePlusOne], 
    budget: List[int] = [100], 
    num_worker: int = 1, 
    instrum = ng.p.Array(shape=(2,))
"""
opt_OPO = opt.Optimizer(opt = ["OnePlusOne"], budget = [20], num_worker = 1) 
opt_OPO_20 = opt.Optimizer(opt = ["OnePlusOne"], budget = [20], num_worker = 30)

""" 
(2) Init MixSimulator instance :
    Case one [Default] : "classic" method (see test_classic.py for more use case)
    Case two : "MAS" or Multi Agent System method

    Default parameters :
    ------------------------
    method : string = "classic",    --> method explain above
    carbon_cost : float = 0         --> cost of the CO2 production 
    penalisation_cost: float = 1e7  --> penalisation cost when production is more or less than the demand #NEED VERIFICATION
"""

classic_mix = ElectricityMix.mix(method="classic",carbon_cost=0,penalisation_cost=100) 
mas_mix = ElectricityMix.mix(method="MAS",carbon_cost=0,penalisation_cost=100)

""" 
(7) ONE SHOT optimization by calling the moderator of the MAS platform
    
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
# print(mas_mix.get_moderator().optimizeMix(1e10,optimizer = opt_OPO, step = 20, penalisation = 100, carbon_cost = 0, time_index = 168, plot = "default"))


""" 
(8) Evaluation of results by budget for each selected optimizer
    Default parameters :
    --------------------
    mix (or moderator),                     --> the mix or moderator to evaluate
    sequence,                               --> each budget to evaluate
    max_budgets, 
    optimizer_list: List['str'],    
    indicator_list: List['str'],            --> indicators are ["loss","elapsed_time","production","unsatisfied demand","carbon production"]
    num_worker: int = 1, 
    bind: str = None,                       --> path to dataset
    time_index: int = 24, 
    carbonProdLimit: float = 39500000000,   --> equal to carbon_quota
    time_interval : float = 1, 
    average_wide : int = 0, 
    penalisation : float = 1000000000000,   --> equal to penalisation cost
    carbon_cost: float = 0
"""
# eva=EvaluationBudget()
# eva.evaluate(mas_mix.get_moderator(),10,100,optimizer_list = ["OnePlusOne","DE","CMA","PSO","NGOpt"], indicator_list = ["loss","elapsed_time","production","unsatisfied demand","carbon production"],carbonProdLimit = 1e10, time_index = 24, penalisation = 100, carbon_cost = 10)

"""
(9) Simulating the mas platform (Manually)
        1 - First, set params by using set_params method
        2 - Run the run_optimization method to initiate the simulation
        3 - Add events
"""
mas_mix.get_moderator().set_params(1e10,optimizer = opt_OPO_20, step = 20, penalisation = 100, carbon_cost = 0, time_index = 24, plot = "default")
mas_mix.get_moderator().run_optimization()
#time.sleep(3)
#print(mas_mix.get_moderator().simulate({"400":[("Tm/ENELEC 3",40)],"400":[("Tm/ENELEC 2",135)], "200":[("Tm/ENELEC 2",136)]}))
centrale1 = mas_mix.get_moderator().get_observable()[0]
centrale2 = mas_mix.get_moderator().get_observable()[1]

centrale1._notify_is_down(6)
#centrale2._notify_is_down(100)
centrale1._notify_is_up(21)
#centrale2._notify_is_up(150)

while True:
    if len(threading.enumerate()) == 2:
        thread_checker.stop()
        break
print("SIMULATION DONE")