import pandas as pd
import sklearn.linear_model as linear_model
import json
from typing import List
from ..Agent import Agent
import nevergrad as ng

class PowerPlant(Agent):
    """
        Agent simulating all the common functions of a power plant
    """
    def __init__(self, tuneable:bool=False) -> None:
        super().__init__()
        self.__changeRate = 0. #(percent)
        self.__initial_value = 0.
        self.__lifetime = 0 #in hour
        self.__carbon_prod = 0. #g/MWh
        self.__raw_power = 0. #MW
        self.__availability = 1.  #of the source
        self.__nb_employes = 1
        self.__mean_salary = 0. #per month
        self.__tuneable = tuneable
        self.__fuel_cost = 0. #$/g
        self.__fuel_consumption = 0. #g/MWh
        self.__init_cur_usage = 0
        self.__cur_usage = 0
        self.__max_var = 1
        self.__lower = 0.
        self.__upper = 1.
        self.__choices = None
        self.__environement = {"precipitation":None, "temps":None, "solar_exposition":None, "wind_exposition":None}

    ### ENVIRONEMENT MONITORING & MODELISATION
    def _modelise_environnement(self, data: pd.DataFrame, model_type: str = "LinearRegression"):
        X_train = data["X_train"]
        Y_train = data["Y_train"]
        X_test = data["X_test"]
        Y_test = data["Y_test"]

        model = eval("linear_model." + model_type +"()")
        model.fit(X_train, Y_train)
        return model


    def set_environement(self, precipitations=None, temps=None, solar_exposition=None, wind_exposition=None):
        self.__environement.update({"precipitation":precipitations, "temps":temps, "solar_exposition":solar_exposition, "wind_exposition":wind_exposition})
        for key in self.__environement.keys():
            if self.__environement[key] is not None: self.__environement.update({key: self._modelise_environnement(self.__environement[key])})

    def get_environement(self, to_predict):
        result = {}
        for key in self.__environement.keys():
            if self.__environement[key] is not None: result.update({key: self.__environement[key].predict(to_predict)})
            else: result.update({key: None})
        return result

    ### COMMUNICATION
    def _notify_is_up(self) -> None:
        signal = json.load(open(self._code_files))["200"]
        signal["id"] = self.get_id()
        self._notify_observers(signal)

    def _notify_is_down(self) -> None:
        signal = json.load(open(self._code_files))["400"]
        signal["id"] = self.get_id()
        self._notify_observers(signal)

    def _notify_disponibility(self) -> None:
        pass

    ### PARAMETRIZATION
    def set_init_cur_usage(self, init_usage):
        self.__init_cur_usage = init_usage
        self.__cur_usage = init_usage

    def set_max_var(self, max_var):
        self.__max_var = max_var

    def set_nb_employees(self, nb_employees):
        self.__nb_employes = nb_employees

    def set_initial_value(self, initial_value):
        self.__initial_value = initial_value

    def set_lifetime(self, lifetime):
        self.__lifetime = lifetime

    def set_fuel_consumption(self, fuel_consumption):
        self.__fuel_consumption = fuel_consumption

    def get_fuel_consumption(self):
        return self.__fuel_consumption

    def set_fuel_cost(self, fuel_cost):
        self.__fuel_cost = fuel_cost

    def get_fuel_cost(self):
        return self.__fuel_cost

    def get_amortized_cost(self, time_index):
        if time_index > self.__lifetime * 365 * 24:
            return 0
        else:
            return ( self.__initial_value / ( self.__lifetime * 365 * 24 ) ) 

    def is_tuneable(self) -> bool:
        #is controlled or not
        return self.__tuneable

    def get_carbon_production(self) -> float: # g/MWh
        return self.__carbon_prod

    def set_carbon_prod(self, carbonCost: float=0) -> None:
        self.__carbon_prod = carbonCost

    def set_raw_power(self, rawPower):
        self.__raw_power = rawPower

    def get_raw_power(self) -> float: # MW
        return self.__raw_power

    def get_availability(self, time_index) -> float: # percent
        return self.__availability

    def reset_powerplant(self):
        self.__cur_usage = self.__init_cur_usage

    def get_max_availability(self, time_index) -> float:
        theorical_availability = self.get_availability(time_index)
        if self.__cur_usage + self.__max_var <= theorical_availability:
            theorical_availability =  self.__cur_usage + self.__max_var
        return theorical_availability

    def get_min_availability(self, time_index) -> float:
        theorical_availability = 0
        if self.__cur_usage - self.__max_var >= theorical_availability:
            theorical_availability =  self.__cur_usage - self.__max_var
        return theorical_availability

    def back_propagate(self, usage_coef, t, time_interval):
        self.__cur_usage = usage_coef
        
    def set_availability(self, availability: float):
        self.__availability = availability

    def get_employees_salary(self, total_working_time_per_day=8) ->float:
        #mean salary per hour
        perHourMeanSalary = self.__mean_salary/(31*total_working_time_per_day)
        return perHourMeanSalary * self.__nb_employes

    def set_mean_employees_salary(self, mean_salary):
        self.__mean_salary = mean_salary

    def set_tuneable(self, tuneable: bool) -> None:
        self.__tuneable = tuneable

    def __getUsageCoef(self, usage_coef: float) -> None:
        if(self.__tuneable):
            usage_coef = min(self.__availability, usage_coef)
        else:
            usage_coef = self.__availability
            
    def set_variation_params(self, lower: float, upper : float, choices : List[float] = None) -> None:
        self.__lower = lower
        self.__upper = upper
        self.__choices = choices
        
    def get_variation_params(self) -> ng.p.Choice:
        final_params = []        
        if self.__choices != None :
            if self.__lower == self._upper :
                return ng.p.Choice(self.__choices)
            else :
                for low, up in zip(self.__lower, self.__upper):
                    if low == up : continue
                    final_params.append(ng.p.Scalar(lower=low ,upper=up))
                discret = ng.p.Choice(self.__choices)
                final_params.append(discret)
                params = ng.p.Choice(final_params)
                return params
            
        else :
            if self.__lower != 0. and self.__upper != 1. :
                for low, up in zip(self.__lower, self.__upper):
                    final_params.append(ng.p.Scalar(lower=low ,upper=up))
                params = ng.p.Choice(final_params)
                return params 
            else :
                final_params.append(ng.p.Scalar(lower=self.__lower ,upper=self.__upper))
                params = ng.p.Choice(final_params)
                return params
