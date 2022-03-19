from .agent import Moderator
from .agent import Hydropowerplant
from .agent import Thermalpowerplant
from .agent import Demand
import nevergrad as ng
from .nevergradBased.Optimizer import Optimizer
import numpy as np # type: ignore
import pandas as pd # type: ignore
import pkgutil
import csv
import os
import warnings
from math import ceil
#import time
from typing import List, Any, Type, Dict
from datetime import datetime
import matplotlib.pyplot as plt # type: ignore

class Mas_platform():
    """
        Platform of a multi agent system :
            - Initialisation of the agents from original dataset
            - Get and initiate the optimizer
            - Data visualization
    """

    def __init__(self, carbon_cost: float = 0, penalisation_cost: float = 1000000000000, bind = None, raw_data = None, variation_data = None, delimiter: str=";", variation_delimiter: str=";",) -> None:
        self.set_data_csv(bind = bind, raw_data =raw_data, delimiter = delimiter)
        self.set_variation_csv(bind = variation_data, delimiter = variation_delimiter)
        self.__moderator = Moderator.Moderator()


    def get_moderator(self) -> Moderator:
        return self.__moderator

    def set_moderator(self, new_moderator) -> None :
        self.__moderator = new_moderator

    def set_variation_csv(self, bind = None, delimiter: str=";") -> None:
        if self.__moderator.get_agents() == []:
             warnings.warn("Please load a original dataset by using MixSimulator.set_data_csv(...)")
             raise 
        else :
            try :
                data = pd.DataFrame(pd.read_csv(bind,delimiter=delimiter))
            except FileNotFoundError as e :
                    print("Error occured on pandas.read_csv : ",e)
                    print("Please check your file")
                    raise           
            except Exception as e:
                    print("Error occured on pandas.read_csv : ",e)
                    raise
                    
            for central_index in range(len(self.__moderator.get_agents())):
                if self.__moderator.get_agents()[central_index].is_tuneable():
                    for i in range (0,data.shape[0]):
                        if self.__moderator.get_agents()[central_index].get_id() == data["centrals"][i]:
                            tmp_list=[]
                            upper = str(data["upper"][i]).split(":")
                            upper = [float(numeric_string) for numeric_string in upper]
                            lower = str(data["lower"][i]).split(":")
                            lower = [float(numeric_string) for numeric_string in lower]
                            discrete = str(data["discrete"][i]).split(":")
                            discrete = [float(numeric_string) for numeric_string in discrete]
                            self.__moderator.get_agents()[central_index].set_variation_params(lower = lower, upper = upper, choices = discrete)
        
    def set_data_csv(self, bind = None, raw_data = None, delimiter: str=";"):
        if raw_data is not None :
            data = pd.DataFrame(raw_data)
            #set columns & index           
            header = data.iloc[0]
            data = data[1:]
            data.columns = header
            data = data.reset_index(drop=True)
            for column in data.columns.tolist():
                try:
                    # convert numeric values
                    data[column] = pd.to_numeric(data[column])
                except:
                    pass
        else :
            try :
                data = pd.DataFrame(pd.read_csv(bind,delimiter=delimiter))
            except FileNotFoundError as e :
                print("Error occured on pandas.read_csv : ",e)
                print("Please check your file")
                raise           
            except Exception as e:
                print("Error occured on pandas.read_csv : ",e)
                raise
            
        #self.__reset_centrals()
        #powerplant = pc.PowerCentral()
        try :
            for i in range (0,data.shape[0]):
                isHydro = data["hydro"][i]
                if isHydro == True :
                    powerplant = Hydropowerplant.Hydropowerplant(data["height"][i],data["flow"][i],data["capacity"][i],data["stock_available"][i],0.1,0.8)
                else :
                    powerplant = Thermalpowerplant.PowerCentral()
                powerplant.set_tuneable(data["tuneable"][i])
                powerplant.set_id(str(data["centrals"][i]))
                powerplant.set_fuel_consumption(data["fuel_consumption"][i])
                powerplant.set_availability(data["availability"][i])
                powerplant.set_fuel_cost(data["fuel_cost"][i])
                powerplant.set_initial_value(data["init_value"][i])
                powerplant.set_lifetime(data["lifetime"][i])
                powerplant.set_carbon_prod(data["carbon_production"][i])
                powerplant.set_raw_power(data["raw_power"][i])
                powerplant.set_nb_employees(data["nb_employees"][i])
                powerplant.set_mean_employees_salary(data["mean_salary"][i])
                powerplant.set_max_var(data["max_var"][i])
                self.__moderator.add_agent(powerplant)
            #self.__demand.set_mean_demand(data["Demand"][0])
            #self.__lost=data["lost"][0]
        except KeyError:
            print("Columns must be in: tuneable, centrals, fuel_consumption, availability, fuel_cost, init_value, lifetime, carbon_cost, raw_power, nb_employees, mean_salary, demand, lost, height, flow, capacity, stock_available")
            raise
            
    def set_data_to(self, dataset, delimiter: str=";"):
        if dataset == "Toamasina":
            #by defaut we keep it "Toamasina"
            data = pkgutil.get_data('mixsimulator', '/data/RIToamasina/dataset_RI_Toamasina_v2.csv')
            data = csv.reader(data.decode('utf-8').splitlines(), delimiter = delimiter)
            self.set_data_csv(raw_data=data)
        else :
            #by defaut we keep it "Toamasina"
            data = pkgutil.get_data('mixsimulator', '/data/RIToamasina/dataset_RI_Toamasina_v2.csv')
            data = csv.reader(data.decode('utf-8').splitlines(), delimiter = delimiter)
            self.set_data_csv(raw_data=data)