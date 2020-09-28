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

    def plot_evaluation(self, X = 0,Y = 0,label : list = ["Optimizer"],label_y : str = "values",max_budgets = 0):

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
        
        #init
        fig = plt.figure(facecolor='w')
        ax = fig.add_subplot(111,axisbelow=True)
        
        # data integration
        for i in range(0,len(Y)):            
            ax.plot(X, Y[i]/units, alpha=0.5, lw=2, label=label[i])
            #ax.plot(max_budgets, I/units, 'r', alpha=0.5, lw=2, label='Infected')
            #ax.plot(max_budgets, R/units, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
        
        # labels and parametrizations    
        ax.set_xlabel('Budgets')
        ax.set_ylabel(labelY)
        ax.set_ylim(0,np.amax(Y[0])+300)
        ax.yaxis.set_tick_params(length=0)
        ax.xaxis.set_tick_params(length=0)
        ax.grid(b=True, which='major', c='w', lw=2, ls='-')
        legend = ax.legend()
        legend.get_frame().set_alpha(0.5)
        for spine in ('top', 'right', 'bottom', 'left'):
            ax.spines[spine].set_visible(False)
        plt.show()
        
    def evaluate(self, mix, sequence, max_budgets, optimizer_list: List['str'] ,bind=None) :        
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
        y=[]
        budget = np.arange(0, max_budgets, sequence)
        for opt in optimizer_list:
            y_tmp = [] 
            for b in budget:
                data=mix.simuleMix(current_usage_coef=[0.6, 0.2, 0.7, 0.95], carbonProdLimit= 3950000000000,
                            time_interval = 2, optimize_with = [opt], budgets = [b], plot = "none", verbose = 1)
                y_tmp.append(float(data["production_cost ($)"]))
                #X.append(float(b+10))
            #plotting
            y.append(np.array(y_tmp))
        self.plot_evaluation(X=np.array(budget),Y=y,label=optimizer_list, label_y = "production_cost ($)", max_budgets = max_budgets)
        
    ########EXAMPLES    
    # evaluate(sys.argv[1], 10, 160)