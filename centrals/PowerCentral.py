class PowerCentral:
    """
        Class for basic power plant 
        it has all the common parameters of the control units (central)
    """
    def __init__(self, tuneable:bool=False):
        self.__id = "0" 
        self.__changeRate = 0 #(percent)
        self.__initial_value = 0
        self.__lifetime = 0 #in hour
        self.__carbon_prod = 0 #g/MWh
        self.__rawPower = 0 #MWh
        self.__availability = 1  # # of the source
        self.__nbEmployes = 1
        self.__meanSalary = 0#per month
        self.__tuneable = tuneable
        self.__fuel_cost = 0 #$/L
        self.__fuel_consumption = 0 #L/MWh
        self.__isGreen  = False #bool

    def setGreenEnergy(self, isGreen: bool):
        self.__isGreen = isGreen

    def isGreen(self):
        return self.__isGreen

    def set_id(self,identity):
        self.__id=identity

    def get_id(self):
        return self.__id

    def set_nb_employees(self, nb_employees):
        self.__nbEmployes = nb_employees

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

    def get_amortized_cost(self):
        return ( self.__initial_value / ( self.__lifetime * 365 * 24 ) ) 

    def isTuneable(self) -> bool:
        #is controlled or not
        return self.__tuneable

    def getCarbonProd(self) -> float:
        return self.__carbonCost

    def setCarbonProd(self, carbonCost: float=0) -> None:
        self.__carbonCost = carbonCost

    def setRawPower(self, rawPower):
        self.__rawPower = rawPower

    def getRawPower(self) -> float: #MWh
        return self.__rawPower

    def getAvailability(self) -> float: # percent
        return self.__availability

    def setAvailability(self, availability: float):
        self.__availability = availability

    def getEmployeesSalary(self, total_working_time_per_day=8) ->float:
        #mean salary per hour
        perHourMeanSalary = self.__meanSalary/(31*total_working_time_per_day)
        return perHourMeanSalary * self.__nbEmployes

    def setMeanEmployeesSalary(self, mean_salary):
        self.__meanSalary = mean_salary

    def __getUsageCoef(self, usage_coef: float) -> float:
        if(self.__tuneable):
            usage_coef = min(self.__availability, usage_coef)
        else:
            usage_coef = self.__availability