import .MixSimulator as ms
import .MasMixSimulator as mms
import warnings

class ElectricityMix:
    """
        Regroup all methods to simulate the electricity mix :
            - classic
            - Multi Agent System (MAS)
    """
    def __init__(self, method: str = "classic", carbon_cost: float = 0, penalisation_cost: float = 1000000000000):
        if method == "classic":
            return ms.MixSimulator(carbon_cost,penalisation_cost)
        elif method == "MAS":
            return mms.MasMixSimulator()
        else:
            warnings.warn("Choose an available option : classic or MAS")