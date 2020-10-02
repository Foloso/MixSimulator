from mixsimulator.centrals.PowerCentral import PowerCentral

class ThermalPowerCentral(PowerCentral):
    """
        Class of power plant with the specifications of a Thermal Power Plant
    """
    def __init__(self):
        self.__tuneable = True