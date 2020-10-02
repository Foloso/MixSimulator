#import sys
#from MixSimulator import MixSimulator
import matplotlib.pyplot as plt
#from matplotlib.ticker import StrMethodFormatter
import numpy as np
from math import ceil
from typing import List
import mixsimulator.nevergradBased.Optimizer as opt

class Evaluation:

    def __init__(self):
        tmp = opt.Optimizer()
        self.__available_optimizers = tmp.getOptimizerList()
        
    def moving_average(self, x, w):
        return np.convolve(x, np.ones(w), 'valid') / w

    def set_units(self,value):
        # Y units
        N=value
        if N>=1000000: 
            units=1000000
            labelY=' Millions'
        else :
            if N>=1000 and N<1000000:
                units=1000
                labelY='k'
            else :
                units=1
                labelY=''
        return [labelY,units]
                
    def plot_evaluation(self, X, Y, label_y : List['str'], label : List = ["Optimizer"], max_budgets = 0):
        #init subplot
        fig, axs = plt.subplots(1, len(label_y), figsize=(12, 4))        
        
        #set the moving average wide
        for opt_name, value in Y[label_y[0]].items():
            average_wide = ceil(len(value)/4)
            #units=self.set_units(value[0])
            break
     
        # data integration        
        for n_axs in range(0,len(axs)) :
            dict_ = Y[label_y[n_axs]]
            for opt_name, value in dict_.items():
                smooth_value = self.moving_average(value,average_wide)
                axs[n_axs].plot(X[(average_wide - 1):], smooth_value, alpha=0.5, lw=2, label=str(opt_name))
        
        # plots parametrizations    
        for n_axs in range(0,len(axs)) :
            axs[n_axs].grid()
            axs[n_axs].yaxis.set_tick_params(length=0)
            axs[n_axs].xaxis.set_tick_params(length=0)
            axs[n_axs].set_xlabel('Budgets')
            #axs[n_axs].yaxis.set_major_formatter(StrMethodFormatter("{x}"+units[0]))
            axs[n_axs].set_ylabel(label_y[n_axs])
            axs[n_axs].legend()
            
        fig.tight_layout()
        plt.show()
        
    def check_opt_list(self,optimizer_list):
        for index in range(0, len(optimizer_list)):
            try :
                if optimizer_list[index] not in self.__available_optimizers:
                    optimizer_list.pop(index)
            except IndexError :
                self.check_opt_list(optimizer_list)
        
    def evaluate(self, mix, sequence, max_budgets, optimizer_list: List['str'], indicator_list: List['str'], bind=None, carbonProdLimit: float = 39500000000, time_interval : float = 2) :        
        #setting dataset
        if bind != None:
            mix.set_data_csv(str(bind))

        self.check_opt_list(optimizer_list) 
        if optimizer_list == [] :
            raise IndexError("Selected optimizers are not available.")

       #process
        y_tmp = {}
        budget = np.arange(0, max_budgets, sequence)

        ind_per_opt = {}
        for opt_name in optimizer_list:
            #print(opt,":")
            ind_per_budget = []
            for b in budget:
                #print(b)
                data = mix.optimizeMix(carbonProdLimit= carbonProdLimit,
                                time_interval = time_interval, optimize_with = [opt_name], budgets = [b])
                ind_per_budget.append(data)
            ind_per_opt.update({opt_name:ind_per_budget})

        for indicator in indicator_list:
            new_ind_per_opt = {}
            for opt_name in optimizer_list:
                ind_per_budget = []
                for b in range(0, len(budget)):
                    data = ind_per_opt[opt_name][b]
                    ind_per_budget.append(float(data[indicator]))
                new_ind_per_opt.update({opt_name:ind_per_budget})
            y_tmp.update({indicator: new_ind_per_opt})
            
        #plotting
        self.plot_evaluation(X=np.array(budget),Y=y_tmp,label_y = indicator_list, label=optimizer_list, max_budgets = max_budgets)