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
        self._nbEmployes = 1
        self._meanSalary = 0#per month
        self._tuneable = tuneable
        self.__fuel_cost = 0 #$/g
        self.__fuel_consumption = 0 #g/MWh
        self._isGreen  = False #bool

    def setGreenEnergy(self, isGreen: bool):
        self._isGreen = isGreen

    def isGreen(self):
        return self._isGreen

    def set_id(self,identity):
        self._id=identity

    def get_id(self):
        return self._id

    def set_nb_employees(self, nb_employees):
        self._nbEmployes = nb_employees

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

    def get_amortized_cost(self):
        return ( self._initial_value / ( self._lifetime * 365 * 24 ) ) 

    def isTuneable(self) -> bool:
        #is controlled or not
        return self._tuneable

    def getCarbonProd(self) -> float: # g/MWh
        return self._carbon_prod

    def setCarbonProd(self, carbonCost: float=0) -> None:
        self._carbon_prod = carbonCost

    def setRawPower(self, rawPower):
        self._rawPower = rawPower

    def getRawPower(self) -> float: # MW
        return self._rawPower

    def getAvailability(self) -> float: # percent
        return self._availability

    def setAvailability(self, availability: float):
        self._availability = availability

    def getEmployeesSalary(self, total_working_time_per_day=8) ->float:
        #mean salary per hour
        perHourMeanSalary = self._meanSalary/(31*total_working_time_per_day)
        return perHourMeanSalary * self._nbEmployes

    def setMeanEmployeesSalary(self, mean_salary):
        self._meanSalary = mean_salary

    def __getUsageCoef(self, usage_coef: float) -> float:
        if(self._tuneable):
            usage_coef = min(self._availability, usage_coef)
        else:
            usage_coef = self._availability