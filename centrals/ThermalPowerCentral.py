from .centrals import PowerCentral as pc

class ThermalPowerCentral(pc):
    """
        Class of power plant with the specifications of a Thermal Power Plant
    """
    def __init__(self):
        self.__tuneable = True