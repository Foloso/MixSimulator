from .PowerPlant import PowerPlant
from math import cos, pi

class Hydropowerplant(PowerPlant):
    """
        Agent simulating a Hydroelectic facility
    """
    def __init__(self, hauteur: float, moyenne_apport: float, capacity: float, available_stock: float, var_per_day: float, var_per_season: float ) -> None:
        super().__init__()
        self.set_type("Hydropowerplant")
        self.__hauteur = hauteur
        self.__moyenne_apport = moyenne_apport # m3/s
        self.__capacity = capacity # m3
        self.__init_stock = available_stock
        self.__available_stock =  [available_stock]# m3
        self.__tuneable = True
        self.__var_per_day = var_per_day
        self.__var_per_season = var_per_season

    def isHydro(self) -> bool:
        return True

    def __get_natural_availability(self, t, init : int = 0) -> float:
        debit_t = self.__moyenne_apport * (1 + (cos(2 * pi * ( t + init )/ 24))* self.__var_per_day + (cos(2 * pi * ( t + init ) / (24*365)))* self.__var_per_season)
        power = (self.__hauteur * debit_t * 9.8 * 0.9 * 997)/1000000 # unit is MW
        if self._raw_power == 0.:
            return 0.
        else :
            return power/self._raw_power

    def __get__artificial_availability(self, t, init : int = 0) ->float:
        debit_t_max = self.__get_available_stock(t + init)/(3600)
        power = (self.__hauteur * debit_t_max * 9.8 * 0.9 * 997) /1000000 # unit is MW
        if self._raw_power == 0.:
            return 0.
        else :
            return power/self._raw_power

    def get_availability(self, t, init : int = 0) -> float:
        dummy_availability = self.__get__artificial_availability(t, init = init) + self.__get_natural_availability(t, init = init)
        if dummy_availability > 1:
            dummy_availability = 1
        return dummy_availability

    def __get_available_stock(self, t):
        return self.__available_stock[t]

    def back_propagate(self, usage_coef, t, interval, init : int = 0):
        super().back_propagate(usage_coef, t, interval, init = init)
        diff = usage_coef - self.__get_natural_availability(t, init = init)
        diff_power = diff * self._raw_power
        # back to m3/s so diff_power has to be in W not in MW ===> *1000
        bandwidth = (diff_power* 1000000) / (9.8*self.__hauteur* 0.9 * 997)  
        self.__update_stock(bandwidth, interval, t, init = init)

    def __update_stock(self, bandwidth, interval, t, init : int = 0):
        # bandwidth can be either positive or negative
        #### if positiv, we have used stocked water
        #### if not the stock has been increased
        current_availability = self.__available_stock[t + init]
        current_availability += -bandwidth*(interval*3600)
        if current_availability > self.__capacity:
            current_availability = self.__capacity
        if init == 0:
            self.__available_stock.append(current_availability)
        else :
            self.__available_stock[t+init] = current_availability

    def get_stock_evolution(self):
        return self.__available_stock

    ### TODO : add/improve prediction function, data monitoring and signal system

