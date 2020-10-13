class PowerCentral:
    """
        Class for basic power plant 
        it has all the common parameters of the control units (central)
    """
    def __init__(self, tuneable:bool=False):
        self._id = "0" 
        self._changeRate = 0 #(percent)
        self._initial_value = 0
        self._lifetime = 0 #in hour
        self._carbon_prod = 0 #g/MWh
        self._rawPower = 0 #MW
        self._availability = 1  #of the source
        self._nb_employes = 1
        self._mean_salary = 0#per month
        self._tuneable = tuneable
        self.__fuel_cost = 0 #$/g
        self.__fuel_consumption = 0 #g/MWh

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

    def __getUsageCoef(self, usage_coef: float) -> float:
        if(self._tuneable):
            usage_coef = min(self._availability, usage_coef)
        else:
            usage_coef = self._availability