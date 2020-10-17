"""
CORE FUNCTION
"""

import numpy as np
#from nevergrad.parametrization import parameter as p
from ..base import ExperimentFunction
#from .rocket import rocket as rocket
from mixsimulator.MixSimulator import MixSimulator


class OptimizeMix(ExperimentFunction):

    def __init__(self) -> None:
        mix = MixSimulator()
        #If time == one_week --> dim = 676
        super().__init__(self._simulate_mix, mix.get_opt_params(self, 676))
        self.register_initialization()

    def _simulate_mix(self, x: np.ndarray) -> float:
        mix = MixSimulator()
        mix.set_data_to("Toamasina")
        mix.set_penalisation_cost(100)
        mix.set_carbon_cost(1000)
        return mix.loss_func(x)