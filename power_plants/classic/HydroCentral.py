from .PowerCentral import PowerCentral as pc
from math import cos, pi
from typing import List

class HydroCentral(pc):
    """
        Class of power plant with the specifications of a HydroElectric Power Plant
    """
    def __init__(self, hauteur: float, moyenne_apport: float, capacity: float, available_stock: float, var_per_day: float, var_per_season: float ) -> None:
        super().__init__()
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

    def __get_natural_availability(self, t) -> float:
        debit_t = self.__moyenne_apport * (1 + (cos(2 * pi * ( t )/ 24))* self.__var_per_day + (cos(2 * pi * ( t ) / (24*365)))* self.__var_per_season)
        power = (self.__hauteur * debit_t * 9.8 * 0.9 * 997)/1000000 # unit is MW
        return power/self._raw_power

    def __get__artificial_availability(self, t) ->float:
        debit_t_max = self.__get_available_stock(t)/(3600)
        power = (self.__hauteur * debit_t_max * 9.8 * 0.9 * 997) /1000000 # unit is MW
        return power/self._raw_power

    def get_availability(self, t) -> float:
        dummy_availability = self.__get__artificial_availability(t) + self.__get_natural_availability(t)
        if dummy_availability > 1:
            dummy_availability = 1
        return dummy_availability

    def __get_available_stock(self, t):
        return self.__available_stock[t]

    def back_propagate(self, usage_coef, t, interval):
        super().back_propagate(usage_coef, t, interval)
        diff = usage_coef - self.__get_natural_availability(t)
        diff_power = diff * self._raw_power
        # back to m3/s so diff_power has to be in W not in MW ===> *1000
        bandwidth = (diff_power* 1000000) / (9.8*self.__hauteur* 0.9 * 997)  
        self.__update_stock(bandwidth, interval, t)

    def __update_stock(self, bandwidth, interval, t):
        # bandwidth can be either positive or negative
        #### if positiv, we have used stocked water
        #### if not the stock has been increased
        current_availability = self.__available_stock[t]
        current_availability += -bandwidth*(interval*3600)
        if current_availability > self.__capacity:
            current_availability = self.__capacity
        self.__available_stock.append(current_availability)

    def reset_central(self):
        super().reset_central()
        self.__available_stock = [self.__init_stock]

    def get_stock_evolution(self):
        return self.__available_stock