from .PowerPlant import PowerPlant

class Thermalpowerplant(PowerPlant):
    """
        Agent simulating a fuel, nuclear or solar thermal power plant
    """

    def __init__(self):
        super().__init__()
        self.set_type("Thermalpowerplant")

    def __get_water_availability(self):
        pass
    
    ### TODO : add/improve prediction function, data monitoring and signal system