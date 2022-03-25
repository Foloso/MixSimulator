#import sys
#from MixSimulator import MixSimulator
import matplotlib.pyplot as plt # type: ignore
#from matplotlib.ticker import StrMethodFormatter
import numpy as np # type: ignore
from math import ceil
from math import floor
#import itertools
from typing import List
import warnings
from .nevergradBased import Optimizer as opt
from .demand.classic import Demand as de
from datetime import datetime
#from matplotlib import ticker

class EvaluationBudget:

    def __init__(self) -> None :
        tmp = opt.Optimizer()
        self.__available_optimizers = tmp.get_available_optimizers()
        self.__marker = [',', '+', '.','<','>','p','h','H','*','x','v','^','s','1','2','3','4','8']
        
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
        
    def plot_evaluation(self, X, Y, label_y : List['str'], label : List = ["Optimizer"], max_budgets = 0, average_wide : int = 0, plot = "save"):
        #reset all possible previous plots
        try :
            plt.close("all")  
        except :
            pass              
        
        #set the moving average wide
        if average_wide == 0 :
            for opt_name, value in Y[label_y[0]].items():
                average_wide = ceil(len(value)/4)
                #units=self.set_units(value[0])
                break
                
        #Label y = 1
        if len(label_y) == 1 or len(label_y) == 2 : 
            fig, axs = plt.subplots(2, figsize=(6, 6))        
            
            # data integration        
            it = 3 #index debut cycle
            for n_axs in range(0,len(label_y)):
                dict_ = Y[label_y[n_axs]]
                for opt_name, value in dict_.items():
                    smooth_value = self.moving_average(value,average_wide)
                    axs[n_axs].plot(X[(average_wide - 1):], smooth_value, marker = self.__marker[it % len(dict_)],markevery = 0.1, alpha=0.5, lw=2, label=opt_name)
                    #axs[0][n_axs].xaxis.set_minor_locator(ticker.MultipleLocator(len(smooth_value)))
                    #axs[0][n_axs].yaxis.set_major_locator(ticker.MultipleLocator(1))                 
                    it = it + 1                 
                    #axs[0][n_axs].xaxis.set_ticks(np.arange(min(X),max(X)+1,1.0))
                    #axs[0][n_axs].yticks(np.arrange(min(smooth_value),max(smooth_value)+1,1.0))
                    #label_per_opt = axs[0][n_axs].text(X[-1],smooth_value[-1],opt_name+"("+str(float("{:.2f}".format(smooth_value[-1])))+")")
                    #texts.append(label_per_opt)
                    #axs[0][n_axs].annotate( label_per_opt,
                    #              xy     = (     X[-1], smooth_value[-1]),
                    #              xytext = (1.02*X[-1], smooth_value[-1]),
                    #            )
                #adjust_text(texts)            
                
                    # plots parametrizations    
                    axs[n_axs].grid()
                    axs[n_axs].yaxis.set_tick_params(which='major', width=1.00, length=5)
                    axs[n_axs].xaxis.set_tick_params(which='major', width=1.00, length=5)
                    axs[n_axs].xaxis.set_tick_params(which='minor', width=0.75, length=2.5, labelsize=10)
                    axs[n_axs].set_xlabel('Budgets')
                    #axs[n_axs].yaxis.set_major_formatter(StrMethodFormatter("{x}"+units[0]))
                    try :
                        axs[n_axs].set_ylabel(label_y[n_axs])
                    except :
                        pass
                    axs[n_axs].legend()
            

            for n_axs in range(0,2) :
                if not axs[n_axs].has_data():
                    fig.delaxes(axs[n_axs])
                
            fig.tight_layout()
            
            if plot == "save": 
                try:
                    path = "results_"+datetime.now().strftime("%d_%m_%Y")
                    name = path+"/Evaluation_"+datetime.now().strftime("%d%m%Y_%H%M%S")+".png"
                    fig.savefig(name)
                    plt.show()
                except FileNotFoundError:
                    warnings.warn("Can't find the directory "+path)
                    name = "Evaluation_"+datetime.now().strftime("%d%m%Y_%H%M%S")+".png"
                    fig.savefig(name)
                    plt.show()
                    
            else :
                plt.show()
            
        else :
            #For label y more than 2
            max_col = ceil(len(label_y)/2)
            min_col = floor(len(label_y)/2)
            fig, axs = plt.subplots(2, max_col, figsize=(10, 8))        
         
            # data integration
            #texts=[]        
            for n_axs in range(0,max_col) :
                dict_ = Y[label_y[n_axs]]
                it = 3 #index debut cycle
                for opt_name, value in dict_.items():
                    smooth_value = self.moving_average(value,average_wide)
                    axs[0][n_axs].plot(X[(average_wide - 1):], smooth_value, marker = self.__marker[it % len(dict_)],markevery = 0.1, alpha=0.5, lw=2, label=opt_name)
                    #axs[0][n_axs].xaxis.set_minor_locator(ticker.MultipleLocator(len(smooth_value)))
                    #axs[0][n_axs].yaxis.set_major_locator(ticker.MultipleLocator(1))                 
                    it = it + 1                 
                    #axs[0][n_axs].xaxis.set_ticks(np.arange(min(X),max(X)+1,1.0))
                    #axs[0][n_axs].yticks(np.arrange(min(smooth_value),max(smooth_value)+1,1.0))
                    #label_per_opt = axs[0][n_axs].text(X[-1],smooth_value[-1],opt_name+"("+str(float("{:.2f}".format(smooth_value[-1])))+")")
                    #texts.append(label_per_opt)
                    #axs[0][n_axs].annotate( label_per_opt,
                    #              xy     = (     X[-1], smooth_value[-1]),
                    #              xytext = (1.02*X[-1], smooth_value[-1]),
                    #            )
            #adjust_text(texts)       
            
            for n_axs in range(0,min_col) :
                dict_ = Y[label_y[max_col+n_axs]]
                it = 3 #index debut cycle
                for opt_name, value in dict_.items():
                    smooth_value = self.moving_average(value,average_wide)
                    axs[1][n_axs].plot(X[(average_wide - 1):], smooth_value, marker = self.__marker[it % len(dict_)],markevery = 0.1, alpha=0.5, lw=2, label=opt_name)
                    #axs[1][n_axs].xaxis.set_minor_locator(ticker.MultipleLocator(len(smooth_value)))
                    #axs[1][n_axs].yaxis.set_major_locator(ticker.MultipleLocator(1))                
                    it = it + 1                
                    #axs[1][n_axs].xaxis.set_ticks(np.arange(min(X),max(X)+1,1.0))
                    #axs[1][n_axs].yticks(np.arrange(min(smooth_value),max(smooth_value)+1,1.0))
                    #axs[1][n_axs].annotate(opt_name+"("+str(float("{:.2f}".format(smooth_value[-1])))+")",
                    #              xy     = (     X[-1], smooth_value[-1]),
                    #              xytext = (1.02*X[-1], smooth_value[-1]),
                    #            )
    
            
            # plots parametrizations   
            for row in range (0,2):
                if row == 0 :
                    for n_axs in range(0,max_col) :
                        axs[row][n_axs].grid()
                        axs[row][n_axs].yaxis.set_tick_params(which='major', width=1.00, length=5)
                        axs[row][n_axs].xaxis.set_tick_params(which='major', width=1.00, length=5)
                        axs[row][n_axs].xaxis.set_tick_params(which='minor', width=0.75, length=2.5, labelsize=10)
                        axs[row][n_axs].set_xlabel('Budgets')
                        #axs[n_axs].yaxis.set_major_formatter(StrMethodFormatter("{x}"+units[0]))
                        axs[row][n_axs].set_ylabel(label_y[n_axs])
                        axs[row][n_axs].legend()
                else :
                    for n_axs in range(0,min_col) :
                        axs[row][n_axs].grid()
                        axs[row][n_axs].yaxis.set_tick_params(which='major', width=1.00, length=5)
                        axs[row][n_axs].xaxis.set_tick_params(which='major', width=1.00, length=5)
                        axs[row][n_axs].xaxis.set_tick_params(which='minor', width=0.75, length=2.5, labelsize=10)
                        axs[row][n_axs].set_xlabel('Budgets')
                        #axs[n_axs].yaxis.set_major_formatter(StrMethodFormatter("{x}"+units[0]))
                        axs[row][n_axs].set_ylabel(label_y[max_col+n_axs])
                        axs[row][n_axs].legend()                        
            
            for row in range (0,2):
                for n_axs in range(0,max_col) :
                    if not axs[row][n_axs].has_data():
                        fig.delaxes(axs[row][n_axs])
                    
            fig.tight_layout()
            
            if plot == "save": 
                try:
                    path = "results_"+datetime.now().strftime("%d_%m_%Y")
                    name = path+"/Evaluation_"+datetime.now().strftime("%d%m%Y_%H%M%S")+".png"
                    fig.savefig(name)
                    plt.show()
                except FileNotFoundError:
                    warnings.warn("Can't find the directory "+path)
                    name = "Evaluation_"+datetime.now().strftime("%d%m%Y_%H%M%S")+".png"
                    fig.savefig(name)
                    plt.show()
                    
            else :
                plt.show()

    def plot_time_evolution(self, data, label_y : List['str'], label : List = ["Optimizer"], max_budgets = 0):
        #init subplot
        print(data)
        
        fig, axs = plt.subplots(1, len(label_y)-1, figsize=(12, 4))        
        
        # data integration        
        for n_axs in range(1,len(axs)) :
            dict_ = data[label_y[n_axs]]
            for opt_name, value in dict_.items():
                axs[n_axs].scatter(data["execution_time (s)"][opt_name], value, alpha=0.5, lw=2, label=str(opt_name))
        
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


    def evaluate(self, mix, sequence, max_budgets, optimizer_list: List['str'], indicator_list: List['str'], num_worker: int = 1, bind: str = None, time_index: int = 24, carbonProdLimit: float = 39500000000, time_interval : float = 1, average_wide : int = 0, penalisation : float = 1000000000000, carbon_cost: float = 0) :        
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
            opt_index = opt.Optimizer(opt=[opt_name], budget = [max_budgets], num_worker = num_worker)
            data = mix.optimizeMix(carbon_quota = carbonProdLimit,
                            time_interval = time_interval, optimizer = opt_index, step = sequence, penalisation = penalisation, time_index = time_index, carbon_cost = carbon_cost, plot = "save")
            ind_per_opt.update({opt_name:data})

        for indicator in indicator_list:
            new_ind_per_opt = {}
            for opt_name, values in ind_per_opt.items():
                ind_per_budget = []
                for budget_value in values:
                    ind_per_budget.append(float(budget_value[indicator]))
                new_ind_per_opt.update({opt_name:ind_per_budget})
            y_tmp.update({indicator: new_ind_per_opt})
            
        #plotting
        self.plot_evaluation(X=np.array(budget),Y=y_tmp,label_y = indicator_list, label=optimizer_list, max_budgets = max_budgets, average_wide = average_wide)
        
        #return X, Y, opt_list, max_budgets
        return [np.array(budget),y_tmp,optimizer_list,max_budgets]
        
    # NOT USE : NEED VERIFICATION
    def evaluate_total_time(self, mix, sequence, max_budgets, optimizer_list: List['str'],
                            indicator_list: List['str'], bind = None, carbonProdLimit: float = 500000,
                            time_index: int = 24*265, time_interval : float = 1, average_wide : int = 0, penalisation : float = 1000000000000, plot : str = "default"):
        #setting dataset
        
        budget = np.arange(0, max_budgets, sequence)

        if bind != None:
            mix.set_data_csv(str(bind))

        self.check_opt_list(optimizer_list) 
        if optimizer_list == [] :
            raise IndexError("Selected optimizers are not available.")
        
       #process
        data_interval = []
        current_demand=de.Demand(mix.get_demand(),0.2,0.2)
        for time in range(0,time_index):
            mix.set_demand(current_demand.get_demand_approxima(time,time_interval))
            ind_per_opt = {}
            for opt_name in optimizer_list:
                data = mix.optimizeMix(carbonProdLimit= carbonProdLimit,
                                time_interval = time_interval, optimize_with = [opt_name], budgets = [max_budgets], step = sequence,  penalisation = penalisation)
                ind_per_opt.update({opt_name:data})
            data_interval.append(ind_per_opt)
        
        Y = []
        indicator_list_WO_penalisation = indicator_list.copy()
        try:
            indicator_list_WO_penalisation.remove("penalized production cost (loss)")
        except:
            pass
        for time in range(0,time_index):
            y_tmp = {}
            for indicator in indicator_list_WO_penalisation:
                new_ind_per_opt = {}
                for opt_name, values in ind_per_opt.items():
                    ind_per_budget = []
                    for budget_value in values:
                        ind_per_budget.append(float(budget_value[indicator]))
                    new_ind_per_opt.update({opt_name:ind_per_budget})
                y_tmp.update({indicator: new_ind_per_opt})
            Y.append(y_tmp)

        result = {}
        for indicator in indicator_list:
            optimizers_dict = {}
            for opt_name in optimizer_list:
                per_budget = []
                for budget_step in range(0,len(budget)):
                    value = 0.
                    for time in range (0, time_index):
                        if indicator == "penalized production cost (loss)":
                            value += Y[time]["production_cost ($)"][opt_name][budget_step] + np.abs((mix.get_penalisation_cost() * Y[time]["unsatisfied_demand (MWh)"][opt_name][budget_step]))
                        else :
                            value += Y[time][indicator][opt_name][budget_step]
                    if indicator == "penalized production cost (loss)":
                        value = np.log10(value)
                    per_budget.append(value)
                optimizers_dict.update({opt_name:per_budget})
            result.update({indicator: optimizers_dict})

        #plotting
        self.plot_evaluation(X=np.array(budget),Y=result,label_y = indicator_list, label=optimizer_list, max_budgets = max_budgets,average_wide = average_wide, plot = plot)
        
        #return X, Y, opt_list, max_budgets
        return [np.array(budget),result,optimizer_list,max_budgets]
                