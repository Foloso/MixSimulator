from .PowerCentral import PowerCentral as pc
from math import cos, pi
from typing import List

class HydroCentral(pc):
    """
        Class of power plant with the specifications of a HydroElectric Power Plant
    """
    def __init__(self, hauteur, moyenne_apport, capacity, available_stock, var_per_day, var_per_season ):
        super().__init__()
        self.__hauteur = hauteur
        self.__moyenne_apport = moyenne_apport # m3/s
        self.__capacity = capacity # m3
        self.__available_stock =  available_stock# m3
        self.__tuneable = True
        self.__var_per_day = var_per_day
        self.__var_per_season = var_per_season

    def isHydro(self):
        return True

    def __get_natural_availability(self, t, interval) -> float:
        debit_t = self.__moyenne_apport * (1 + (cos(2 * pi * ( t * interval )/ 24))* self.__var_per_day + (cos(2 * pi * ( t * interval ) / (24*365)))* self.__var_per_season)
        power = (self.__hauteur * debit_t * 9.8 * 0.9 * 997)/1000000 # unit is MW
        return power/self._rawPower

    def __get__artificial_availability(self, t, interval) ->float:
        print("T", t)
        print("STOCK", self.__available_stock)
        debit_t_max = self.__available_stock/(interval*3600)
        power = (self.__hauteur * debit_t_max * 9.8 * 0.9 * 997) /1000000 # unit is MW
        return power/self._rawPower

    def get__availability(self, t, interval) -> float:
        dummy_availability = self.__get__artificial_availability(t, interval) + self.__get_natural_availability(t, interval)
        print("ART", self.__get__artificial_availability(t, interval))
        if dummy_availability > 1:
            dummy_availability = 1
        return dummy_availability

    def back_propagate(self, usage_coef, t, interval):
        print("usage, ", usage_coef)
        diff = usage_coef - self.__get_natural_availability(t, interval)
        diff_power = diff * self._rawPower
        # back to m3/s so diff_power has to be in W not in MW ===> *1000
        bandwidth = (diff_power* 1000000) / (9.8*self.__hauteur* 0.9 * 997)  
        self.__update_stock(bandwidth, interval)

    def __update_stock(self, bandwidth, interval):
        # bandwidth can be either positive or negative
        #### if positiv, we have used stocked water
        #### if not the stock has been increased
        self.__available_stock += -bandwidth*(interval*3600)
        if self.__available_stock > self.__capacity:
            self.__available_stock = self.__capacity
        
