import threading
from MixSimulator import ElectricityMix
from MixSimulator.Evaluation import EvaluationBudget
from MixSimulator.demand.classic.Demand import Demand
import MixSimulator.nevergradBased.Optimizer as opt
import time
from datetime import datetime
from math import ceil
from MixSimulator.agents.Moderator import StoppableThread
import matplotlib.pyplot as plt
import numpy as np
import os
import warnings
from typing import List, Dict
import random

"""
    (0) Check the thread running in background
"""
def generate_random_scenario(centrals: List, time_index: int) -> Dict:
    scenario = {}
    for central in centrals:
        tmp = {"down":[], "up":[]}
        default_proba = random.uniform(0, 0.2)
        
        for i in range(time_index):
            tmp[np.random.choice(["up", "down"], p=[1-default_proba,default_proba])].append(i)

        up = []
        down = []
        for i in range(time_index):
            if i in tmp["down"] and (i-1 not in tmp["down"] or i==0):
                down.append(i)
            if i-1 in tmp["down"] and i in tmp["up"]: 
                up.append(i)
        tmp["up"] = up
        tmp["down"] = down

        scenario.update({central:tmp.copy()})
    
    event_stack = {}
    for i in range(time_index):
        for central in scenario.keys():
            if i in scenario[central]["down"]:
                try:
                    event_stack[i].append(central._notify_is_down)
                except:
                    event_stack.update({i:[central._notify_is_down]})
            elif i in scenario[central]["up"]:
                try:
                    event_stack[i].append(central._notify_is_up)
                except:
                    event_stack.update({i:[central._notify_is_up]})


    # print(numpy.arange(0, 2))
    print("scenario: ", event_stack)
    return event_stack

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
    (0.5) Plot loss evolution 
"""   
def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

def plot_loss(optimum, mode : str = "default", average_wide : int = 0, step : int = 1):
        #set the moving average wide
        if average_wide == 0 :
            average_wide = ceil(len(optimum[-1]["coef"])/4)
    
        if mode == "default" or mode == "save" or mode == "best":
            #set Y
            Y_: Dict[str,List[float]] ={} 
            Y_["lost"] = []
            Y_["demand_gap"] = []
            for t_i in range(0,len(optimum)):
                Y_["lost"].append(optimum[t_i]["loss"])
                Y_["demand_gap"].append(optimum[t_i]["unsatisfied demand"])

            fig, axs = plt.subplots(1, 2, figsize=(10, 10))        
        
            # data integration        
            X = [i*step for i in range(0,len(optimum))]  
            #smooth_value = moving_average(Y_["lost"],average_wide)
            for n_axs in range(0,2) :
                if n_axs == 0:
                    #axs[n_axs].plot(X[(average_wide - 1):], smooth_value, '.-' ,alpha=0.5, lw=2, label="lost")
                    axs[n_axs].plot(X,Y_["lost"],'.-' ,alpha=0.5, lw=2, label="lost")
                else:
                    axs[n_axs].plot(X,Y_["demand_gap"],'-*' ,alpha=0.5, lw=2, label="demand gap")
              
            # Add execution_time and loss information
            try :  
                info = "Final loss: "+ "{:.3f}".format(optimum[-1]["loss"])+" ; run_time: "+"{:.3f}".format(optimum[-1]["elapsed_time"])
            except :
                info = "production_cost: "+ "{:.3f}".format(optimum[-1]["loss"])
            info += ";Final demand gap: "+"{:.3f}".format(optimum[-1]["unsatisfied demand"])                   
            plt.annotate(info,
                xy=(0.5, 0), xytext=(0, 10),
                xycoords=('axes fraction', 'figure fraction'),
                textcoords='offset points',
                size=10, ha='center', va='bottom')
                
            # plots parametrizations
            for n_axs in range(0,2) :  
                axs[n_axs].grid()
                axs[n_axs].yaxis.set_tick_params(length=0)
                axs[n_axs].xaxis.set_tick_params(length=0)
                axs[n_axs].set_xlabel('budgets')
                #axs[n_axs].yaxis.set_major_formatter(StrMethodFormatter("{x}"+units[0]))
                if n_axs == 0 :
                    axs[n_axs].set_ylabel('Loss')
                elif n_axs == 1 :
                    axs[n_axs].set_ylabel('Demand gap')
                axs[n_axs].legend()
                
            fig.tight_layout()
            try :
                path = "results_"+datetime.now().strftime("%d_%m_%Y")
                os.makedirs(path)
                name = path+"/"+"opt_"+str(datetime.now().strftime("%H%M%S"))+".png"
                fig.savefig(name)
                if mode == "default" :
                    plt.show()
                
            except OSError:
                warnings.warn("Can't create the directory "+path+" or already exists")
                try : 
                    name = path+"/"+"opt_"+str(datetime.now().strftime("%H%M%S"))+".png"
                    fig.savefig(name)
                    if mode == "default" :
                        plt.show()
                except FileNotFoundError:
                    name = "opt_"+str(datetime.now().strftime("%H%M%S"))+".png"
                    fig.savefig(name)
                    if mode == "default" :
                        plt.show()

        elif mode == "None" :
            pass
        else :
            warnings.warn("Choose an available option : default, save or None")
            #plt.show()
    

""" 
(1) Configure nevergrad optimizers 

    Default Parameters :
    ----------
    opt = [ng.optimizers.OnePlusOne], 
    budget: List[int] = [100], 
    num_worker: int = 1, 
    instrum = ng.p.Array(shape=(2,))
"""
#opt_OPO = opt.Optimizer(opt = ["OnePlusOne"], budget = [20], num_worker = 1) 
opt_OPO_1 = opt.Optimizer(opt = ["OnePlusOne"], budget = [100], num_worker = 1)

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
(7) ONE SHOT optimization by calling the classic approach

"""
classic_mix.set_data_csv("data/RIToamasina/dataset_RI_Toamasina_v2.csv",delimiter=";")
demand = Demand()
data_demand = demand.set_data_csv("data/RIToamasina/DIR-TOAMASINA_concat.csv", delimiter = ",")
classic_mix.set_demand(demand)
classic_result = classic_mix.optimizeMix(1e10,optimizer = opt_OPO_1, step = 10, penalisation = 100, carbon_cost = 0, time_index = 24, plot = "save")
###
### MODIFY RESULTS SELON EVENTS
###
plot_loss(classic_result,step = 10)

"""
(9) Simulating the mas platform (Manually)
        1 - First, set params by using set_params method
        2 - Run the run_optimization method to initiate the simulation
        3 - Add events
"""
mas_mix.get_moderator().set_params(1e10,optimizer = opt_OPO_1, step = 500, penalisation = 100, carbon_cost = 0, time_index = 12, plot = "None")
mas_mix.get_moderator().run_optimization()
#centrale1 = mas_mix.get_moderator().get_observable()[0]
#centrale2 = mas_mix.get_moderator().get_observable()[1]

#centrale1._notify_is_down(8)
#centrale1._notify_is_up(10)

centrals = mas_mix.get_moderator().get_observable()
scenario = generate_random_scenario(centrals, 12)
for t in scenario.keys():
    for event in scenario[t]:
        event(t)

while True:
    if len(threading.enumerate()) == 2:
        thread_checker.stop()
        break
print("SIMULATION DONE")

print("FINAL RESULT: ", mas_mix.get_moderator().get_results())
mas_mix.get_moderator().plotResults(mas_mix.get_moderator().get_results())