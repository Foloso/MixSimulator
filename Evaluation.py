import sys
from MixSimulator import MixSimulator
import matplotlib.pyplot as plt
import numpy as np
from typing import List
from nevergradBased.Optimizer import Optimizer

class Evaluation:

    def __init__(self):
        tmp = Optimizer()
        self.__available_optimizers = tmp.getOptimizerList()

    def plot_evaluation(self, X, Y, label_y : List['str'], label : List = ["Optimizer"], max_budgets = 0):

        """
        # Y units
        N=X[0]
        if N>=1000000: 
            units=1000000
            labelY=label_y+' (Millions)'
        else :
            if N>=1000 and N<1000000:
                units=1000
                labelY=label_y+' (k)'
            else :
                units=1
                labelY=label_y
        """
        
        #init subplot
        fig, axs = plt.subplots(1, len(label_y), figsize=(12, 6))        
        
        # data integration        
        for n_axs in range(0,len(axs)) :
            dict_ = Y[label_y[n_axs]]
            for opt, value in dict_.items():
                axs[n_axs].plot(X, value, alpha=0.5, lw=2, label=str(opt))
        
        # labels and parametrizations    

        for n_axs in range(0,len(axs)) :
            axs[n_axs].grid()
            axs[n_axs].yaxis.set_tick_params(length=0)
            axs[n_axs].xaxis.set_tick_params(length=0)
            axs[n_axs].set_xlabel('Budgets')
            axs[n_axs].set_ylabel(label_y[n_axs])
            axs[n_axs].legend()
        plt.show()
        
    def evaluate(self, mix, sequence, max_budgets, optimizer_list: List['str'], indicator_list: List['str'], bind=None, carbonProdLimit: float = 39500000000, time_interval : float = 2) :        
        #setting dataset
        if bind != None:
            mix.set_data_csv(str(bind))

        for index in range(0, len(optimizer_list)):
            if optimizer_list[index] not in self.__available_optimizers:
                print(optimizer_list[index] , " is not available")
                optimizer_list.pop(index)
        
        if len(optimizer_list) == 0:
            print("Selected optimizers are not avalaible.")
            return

       #process
        y_tmp = {}
        budget = np.arange(0, max_budgets, sequence)

        ind_per_opt = {}
        for opt in optimizer_list:
            ind_per_budget = []
            for b in budget:
                data = mix.simuleMix(current_usage_coef=[0.6, 0.2, 0.7, 0.95], carbonProdLimit= carbonProdLimit, 
                                time_interval = time_interval, optimize_with = [opt], budgets = [b], plot = "none", verbose = 1)
                ind_per_budget.append(data)
            ind_per_opt.update({opt:ind_per_budget})

        for indicator in indicator_list:
            new_ind_per_opt = {}
            for opt in optimizer_list:
                ind_per_budget = []
                for b in range(0, len(budget)):
                    data = ind_per_opt[opt][b]
                    ind_per_budget.append(float(data[indicator]))
                new_ind_per_opt.update({opt:ind_per_budget})
            y_tmp.update({indicator: new_ind_per_opt})
            
        #plotting
        self.plot_evaluation(X=np.array(budget),Y=y_tmp,label_y = indicator_list, label=optimizer_list, max_budgets = max_budgets)