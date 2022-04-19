from . import MixSimulator as ms
from . import Mas_platform as mp
import warnings

class ElectricityMix:
    """
        Regroup all methods to simulate the electricity mix :
            - classic
            - Multi Agent System (MAS)
    """
    def __init__(self):
        pass

    def mix(method: str = "classic", carbon_cost: float = 0, penalisation_cost: float = 1000000000000):
        if method == "classic":
            return ms.MixSimulator(carbon_cost = carbon_cost,penalisation_cost = penalisation_cost)
        elif method == "MAS":
            return mp.Mas_platform()
        else:
            warnings.warn("Choose an available option : classic or MAS")