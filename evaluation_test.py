import sys
from MixSimulator import MixSimulator
import matplotlib.pyplot as plt
import numpy as np

def plot_evaluation(X = 0,Y = 0,label : list = ["Optimizer"],label_y : str = "values",max_budgets = 0):

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
    ax.plot(Y, X, 'b', alpha=0.5, lw=2, label=label[0])
    #ax.plot(max_budgets, I/units, 'r', alpha=0.5, lw=2, label='Infected')
    #ax.plot(max_budgets, R/units, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
    
    # labels and parametrizations    
    ax.set_xlabel('Budgets')
    ax.set_ylabel(labelY)
    ax.set_ylim(0,np.amax(X)+150)
    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)
    ax.grid(b=True, which='major', c='w', lw=2, ls='-')
    legend = ax.legend()
    legend.get_frame().set_alpha(0.5)
    for spine in ('top', 'right', 'bottom', 'left'):
        ax.spines[spine].set_visible(False)
    plt.show()
    
def evaluate(bind,sequence,max_budgets) :
    mix = MixSimulator()
    
    #setting dataset
    mix.set_data_csv(str(bind))
    
    #process
    X=[]
    y=[]
    budget = np.arange(0, max_budgets, sequence)
    for b in budget:
        data=mix.simuleMix(current_usage_coef=[0.6, 0.2, 0.7, 0.95], carbonProdLimit= 3950000000000,
                       time_interval = 2, optimize_with = ["OnePlusOne"], budgets = [b], plot = "none", verbose = 1)
        X.append(float(data["production_cost ($)"]))
        #X.append(float(b+10))
        y.append(b)
    #plotting
    plot_evaluation(X=np.array(X),Y=y,label=["OnePlusOne"], label_y = "production_cost ($)", max_budgets = max_budgets)
    
########EXAMPLES    
evaluate(sys.argv[1], 10, 160)