from typing import List
import nevergrad as ng

class PowerCentral:
    """
        Class for basic power plant 
        it has all the common parameters of the control units (central)
    """
    def __init__(self, tuneable:bool=False) -> None:
        self._id = "0" 
        self._changeRate = 0. #(percent)
        self._initial_value = 0.
        self._lifetime = 0 #in hour
        self._carbon_prod = 0. #g/MWh
        self._raw_power = 0. #MW
        self._availability = 1.  #of the source
        self._nb_employes = 1
        self._mean_salary = 0. #per month
        self._tuneable = tuneable
        self.__fuel_cost = 0. #$/g
        self.__fuel_consumption = 0. #g/MWh
        self._init_cur_usage = 0
        self._cur_usage = 0
        self._max_var = 1
        self._lower = 0.
        self._upper = 1.
        self._choices = None

    def set_init_cur_usage(self, init_usage):
        self._init_cur_usage = init_usage
        self._cur_usage = init_usage

    def set_max_var(self, max_var):
        self._max_var = max_var

    def set_id(self, identity):
        self._id = identity

    def get_id(self):
        return self._id

    def set_nb_employees(self, nb_employees):
        self._nb_employes = nb_employees

    def set_initial_value(self, initial_value):
        self._initial_value = initial_value

    def set_lifetime(self, lifetime):
        self._lifetime = lifetime

    def set_fuel_consumption(self, fuel_consumption):
        self._fuel_consumption = fuel_consumption

    def get_fuel_consumption(self):
        return self._fuel_consumption

    def set_fuel_cost(self, fuel_cost):
        self.__fuel_cost = fuel_cost

    def get_fuel_cost(self):
        return self.__fuel_cost

    def get_amortized_cost(self, time_index):
        if time_index > self._lifetime * 365 * 24:
            return 0
        else:
            return ( self._initial_value / ( self._lifetime * 365 * 24 ) ) 

    def is_tuneable(self) -> bool:
        #is controlled or not
        return self._tuneable

    def get_carbon_production(self) -> float: # g/MWh
        return self._carbon_prod

    def set_carbon_prod(self, carbonCost: float=0) -> None:
        self._carbon_prod = carbonCost

    def set_raw_power(self, rawPower):
        self._raw_power = rawPower

    def get_raw_power(self) -> float: # MW
        return self._raw_power

    def get_availability(self, time_index) -> float: # percent
        return self._availability

    def reset_central(self):
        self._cur_usage = self._init_cur_usage

    def get_max_availability(self, time_index) -> float:
        theorical_availability = self.get_availability(time_index)
        if self._cur_usage + self._max_var <= theorical_availability:
            theorical_availability =  self._cur_usage + self._max_var
        return theorical_availability

    def get_min_availability(self, time_index) -> float:
        theorical_availability = 0
        if self._cur_usage - self._max_var >= theorical_availability:
            theorical_availability =  self._cur_usage - self._max_var
        return theorical_availability

    def back_propagate(self, usage_coef, t, time_interval):
        self._cur_usage = usage_coef
        
    def set_availability(self, availability: float):
        self._availability = availability

    def get_employees_salary(self, total_working_time_per_day=8) ->float:
        #mean salary per hour
        perHourMeanSalary = self._mean_salary/(31*total_working_time_per_day)
        return perHourMeanSalary * self._nb_employes

    def set_mean_employees_salary(self, mean_salary):
        self._mean_salary = mean_salary

    def set_tuneable(self, tuneable: bool) -> None:
        self._tuneable = tuneable

    def __getUsageCoef(self, usage_coef: float) -> None:
        if(self._tuneable):
            usage_coef = min(self._availability, usage_coef)
        else:
            usage_coef = self._availability
            
    def set_variation_params(self, lower: float, upper : float, choices : List[float] = None) -> None:
        self._lower = lower
        self._upper = upper
        self._choices = choices
        
    def get_variation_params(self) -> ng.p.Choice:
        final_params = []        
        if self._choices != None :
            if self._lower == self._upper :
                return ng.p.Choice(self._choices)
            else :
                for low, up in zip(self._lower, self._upper):
                    if low == up : continue
                    final_params.append(ng.p.Scalar(lower=low ,upper=up))
                discret = ng.p.Choice(self._choices)
                final_params.append(discret)
                params = ng.p.Choice(final_params)
                return params
            
        else :
            if self._lower != 0. and self._upper != 1. :
                for low, up in zip(self._lower, self._upper):
                    final_params.append(ng.p.Scalar(lower=low ,upper=up))
                params = ng.p.Choice(final_params)
                return params 
            else :
                final_params.append(ng.p.Scalar(lower=self._lower ,upper=self._upper))
                params = ng.p.Choice(final_params)
                return params
                