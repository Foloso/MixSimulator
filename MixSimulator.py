import matplotlib.pyplot as plt
from . import SegmentOptimizer as sOpt
from .centrals import PowerCentral as pc
from .centrals import HydroCentral as hc 
from . import Demand as de
import numpy as np
import pandas as pd
import warnings
import time
from typing import List

class MixSimulator:
    """
        The simulator Base            
    """
    def __init__(self):
        self.__reset_centrals()
        self.__demand = 0
        self.__lost = 0
        

    def __reset_centrals(self):
        self.__centrals = {}
        self.__init_list = []
        self.__centrals.update({"green": []})
        self.__centrals.update({"non_green": []})

    def set_data_csv(self, bind: str, delimiter: str=";"):
        try :
            data = pd.DataFrame(pd.read_csv(bind,delimiter=delimiter))
            
        except FileNotFoundError as e :
            print("Error occured on pandas.read_csv : ",e)
            print("Please check your file")
            raise           
        except Exception as e:
            print("Error occured on pandas.read_csv : ",e)
            raise
            
        self.__reset_centrals()
        centrale_tmp = []
        try :
            for i in range (0,data.shape[0]):
                centrale = data["tuneable"][i]
                if centrale == False :
                    centrale = hc.HydroCentral(data["height"][i],data["flow"][i],data["capacity"][i],data["stock_available"][i],0.1,0.8)
                else :
                    centrale = pc.PowerCentral(centrale)
                centrale.set_id(str(data["centrals"][i]))
                centrale.set_fuel_consumption(data["fuel_consumption"][i])
                centrale.setAvailability(data["availability"][i])
                centrale.set_fuel_cost(data["fuel_cost"][i])
                centrale.set_initial_value(data["init_value"][i])
                centrale.set_lifetime(data["lifetime"][i])
                centrale.setCarbonProd(data["carbon_production"][i])
                centrale.setRawPower(data["raw_power"][i])
                centrale.set_nb_employees(data["nb_employees"][i])
                centrale.setMeanEmployeesSalary(data["mean_salary"][i])
                centrale.setGreenEnergy(data["green"][i])
                centrale_tmp.append(centrale)
                self.__init_list.append(centrale.get_id())
            self.__demand=data["Demand"][0]
            self.__lost=data["lost"][0]
        except KeyError:
            print("Columns must be in: tuneable, green, centrals, fuel_consumption, availability, fuel_cost, init_value, lifetime, carbon_cost, raw_power, nb_employees, mean_salary, demand, lost")
            raise
            
        self.__splitCentrals(centrale_tmp)

    def setCentrals(self, centrals: List[str]):
        self.__reset_centrals()
        self.__splitCentrals(centrals)

    def set_demand(self,demand):
        self.__demand = demand

    def __splitCentrals(self, centrals: List[str]):
        for centrale in centrals:
                if centrale.isGreen():
                    self.__centrals["green"].append(centrale)
                else:
                    self.__centrals["non_green"].append(centrale)

    def optimizeMix(self, carbonProdLimit, demand: float= None, lost: float=None, 
                    time_interval: float = 1, carbon_cost: float = None, optimize_with = ["OnePlusOne"], budgets = [100], instrum = None, step: int = 1, time_index: int = 24*365):
        
        """Initiate the Mix's parameters and calculate the optimal coef_usage with the given optimizer"""
        # default parameter
        results = []

        if demand is None:
            demand = self.__demand
        if lost is None:
            lost = self.__lost

        #Get GREEN and the NON-GREEN PowerPlant
        green_mix = sOpt.SegmentOptimizer()
        non_green_mix = sOpt.SegmentOptimizer()
        
        green_mix.setCentrals(self.__centrals["green"])
        non_green_mix.setCentrals(self.__centrals["non_green"])

        green_mix.set_time(time_interval)
        non_green_mix.set_time(time_interval)

        # prioriser d'abord les energies renouvelables
        green_mix.set_time_index(time_index)
        GREEN_RESULT = green_mix.getOptimumUsageCoef(carbonProdLimit=carbonProdLimit, 
                                                     demand= demand, lost=lost, optimize_with = optimize_with, budgets = budgets, instrum = instrum, step=step)
        new_carbonProdLimit = carbonProdLimit - GREEN_RESULT[len(GREEN_RESULT)-1]["carbonProd"]
        new_demand = demand - GREEN_RESULT[len(GREEN_RESULT)-1]["production"]
        i=0        
        for green in self.__centrals["green"]:
            green.back_propagate(GREEN_RESULT[len(GREEN_RESULT)-1]["coef usage"][i], time_index, time_interval)
            i=i+1
            

        # ensuite s'occuper des centrales "non-green"
        NON_GREEN_RESULT = non_green_mix.getOptimumUsageCoef(carbonProdLimit=new_carbonProdLimit, 
                                                             demand=new_demand, lost=lost, optimize_with = optimize_with, budgets = budgets, instrum = instrum, step=step)        

        for budget_step in range(0, len(GREEN_RESULT)):
            tmp_result = {}
            usage_coef = {}
            index_central = 0
            for coef in GREEN_RESULT[budget_step]["coef"]:
                usage_coef.update({self.__centrals["green"][index_central].get_id():coef})
                index_central += 1
            
            index_central = 0
            for coef in NON_GREEN_RESULT[budget_step]["coef"]:
                usage_coef.update({self.__centrals["non_green"][index_central].get_id():coef})
                index_central += 1

            tmp_result.update({"execution_time (s)": NON_GREEN_RESULT[budget_step]["elapsed_time"] + GREEN_RESULT[budget_step]["elapsed_time"]})
            tmp_result.update({"production_cost ($)": NON_GREEN_RESULT[budget_step]["production_cost"] + GREEN_RESULT[budget_step]["production_cost"]})
            tmp_result.update({"carbon_impacte (g/MWh)": NON_GREEN_RESULT[budget_step]["carbonProd"] + GREEN_RESULT[budget_step]["carbonProd"]})
            if carbon_cost is None:
                pass
            else :
                tmp_result.update({"carbon_cost ($/MWh)":   (NON_GREEN_RESULT[budget_step]["carbonProd"] + GREEN_RESULT[budget_step]["carbonProd"])* carbon_cost})
            tmp_result.update({"unsatisfied_demand (MWh)": demand - (NON_GREEN_RESULT[budget_step]["production"] + GREEN_RESULT[budget_step]["production"])})
            tmp_result.update({"usage_coefficient": usage_coef})
            results.append(tmp_result)

        return results

    def simuleMix(self, current_usage_coef, carbonProdLimit: float = 99999999999, demand: float = None, 
                  lost: float = None, time_interval: float = 1, carbon_cost: float = None, 
                  optimize_with = ["OnePlusOne"], budgets = [100], instrum = None, verbose: int = 0, plot: str = "default", step : int = None, time_index : int = 24*365):
        
        """Simulate and compare the current_mix and the theorical_optimum Mix"""
        # initialization
        if demand is None :
            demand = self.__demand
        if lost is None :
            lost = self.__lost
        if step is None :
            step = budgets

        ##### actual perf
        current_perf = {}

        # current Mix initialization
        current_mix = sOpt.SegmentOptimizer()
        centrals = []
        for key in self.__centrals.keys():
            for central in self.__centrals[key]:
                centrals.append(central)
        current_mix.setCentrals(centrals)
        current_mix.set_time(time_interval)
        current_perf.update({"production_cost ($)": current_mix.prod_cost_objective_function(current_usage_coef)})
        current_perf.update({"carbon_impacte (g/MWh)": current_mix.get_carbon_prod_constraint(current_usage_coef)})
        current_perf.update({"unsatisfied_demand (MWh)": demand - current_mix.get_production_constraint(current_usage_coef)})
        coef_dict = {}
        for index in range(0, len(current_usage_coef)):
            coef_dict.update({self.__init_list[index]:current_usage_coef[index]})
        current_perf.update({"usage_coefficient": coef_dict})
        
        # optimization over  
        data_per_interval = []
        current_demand=de.Demand(self.__demand,0.5,0.8)
        for t in range(0,time_index):
            self.set_demand(current_demand.get_demand_approxima(t,time_interval))
            data = self.optimizeMix(carbonProdLimit= carbonProdLimit,
                                time_interval = time_interval, optimize_with = optimize_with, budgets = budgets, step = step, time_index = t)
        data_per_interval.append(data)

        # verbosity
        if verbose == 1 :
            print("theorical_optimum : ",data_per_interval)
            print("current_perf : ", current_perf)
        
        #plotting
        if plot == "default" :
            self.plotResults(data_per_interval[-1][-1], current_perf, mode = plot , time_interval = time_interval)
        else :
            if plot == "none" :
                pass
            else :
                warnings.warn("Available plot options : \n \t 'default' : show and save the results plots; \n \t 'none' : no plots.")
        
        return data_per_interval

    def plotResults(self, optimum : dict = {}, current : dict = {}, mode : str = "default", time_interval : int = 1) :
        columns=[]
        tmp=[]
        data=[]
        
        #handle data
        for keys, values in optimum.items():
            if keys == "usage_coefficient":
                for k, v in values.items():
                    columns.append(k)
                    tmp.append(v)
        data.append(tmp)
        tmp=[]        
        for keys, values in current.items():
            if keys == "usage_coefficient":
                for k, v in values.items():
                    tmp.append(v)
        data.append(tmp)

        tmp = []
        time_data = {}
        for keys, values in optimum.items():
            if keys == "execution_time (s)":
                time_data.update({keys:values})
            elif keys != "usage_coefficient":
                columns.append(keys)
                tmp.append(values)
        data.append(tmp)
        tmp=[]        
        for keys, values in current.items():
            if keys != "usage_coefficient":
                tmp.append(values)
        data.append(tmp)
                
        rows = ["current","optimum"]        
              
        # Get some pastel shades for the colors
        colors = plt.cm.autumn(np.linspace(0, 0.5, len(rows)))
        n_rows = len(rows)
        
        index = np.arange(len(columns[:-3])) + 0.3
        bar_width = 0.4
        
        # Initialize the vertical-offset for the stacked bar chart.
        y_offset = np.zeros(len(columns[:-3]))
        
        # Plot bars and create text labels for the table
        cell_text = []
        correction = np.zeros(len(columns[:-3]))
        to_plot = data[:-2]
        
        for row in range(n_rows):
            for i in range(len(columns[:-3])):
                if y_offset[i] < to_plot[row][i]:
                    correction[i] = y_offset[i]
                    color_correction = row-1
            y_offset = np.zeros(len(columns[:-3]))
            plt.bar(index, to_plot[row], bar_width, bottom=y_offset, color=colors[row])
            y_offset = to_plot[row]
            cell_text.append(['%f' % x for x in y_offset])
            
        # Correction to avoid hidden bar
        y_offset = np.zeros(len(columns[:-3]))
        plt.bar(index, correction, bar_width, bottom=y_offset, color=colors[color_correction])            


        # Reverse colors and text labels to display the last value at the top.
        colors = colors[::-1]
        cell_text.reverse()
        
        # Add tables 
        plt.table(cellText=cell_text,
                              rowLabels=rows,
                              rowColours=colors,
                              colLabels=columns[:-3],
                              loc='bottom')
        
        cell_text=data[-2:]
        cell_text.reverse()
        plt.table(cellText=cell_text,
                              rowLabels=rows,
                              rowColours=colors,
                              colLabels=columns[-3:],
                              loc='upper center')
        
        # Add exection_time information
        for time_k, time_v in time_data.items():
            time_str = time_k+": "+str(time_v)                       
        plt.annotate(time_str,
            xy=(0.5, 0), xytext=(0, 10),
            xycoords=('axes fraction', 'figure fraction'),
            textcoords='offset points',
            size=10, ha='center', va='bottom')
        plt.annotate("Best coef. in last: "+str(time_interval)+"hour(s)",
            xy=(0.5, 0), xytext=(0, 10),
            xycoords=('axes fraction', 'figure fraction'),
            textcoords='offset points',
            size=10, ha='center', va='top')
                              
        # Adjust layout to make room for the table:
        plt.subplots_adjust(left=0.2, bottom=0.2)
        values = np.arange(0, 140, 20)
        value_increment = 100 
        plt.ylabel("Usage coef. in % ")
        plt.yticks(values / value_increment, ['%d' % val for val in values])
        plt.xticks([])
        plt.title('Optimum and Current values')

        plt.show()