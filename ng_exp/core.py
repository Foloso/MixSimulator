"""
CORE FUNCTION
"""

import numpy as np
from nevergrad.parametrization import parameter as p
from ..base import ExperimentFunction
#from .rocket import rocket as rocket
from mixsimulator.MixSimulator import MixSimulator


class OptimizeMix(ExperimentFunction):

    def __init__(self) -> None:
        super().__init__(self._simulate_mix, p.Array(shape=(168,4)))
        self.register_initialization()

    def _simulate_mix(self, x: np.ndarray) -> float:
        mix=MixSimulator()
        mix.set_data_to("Toamasina")
        mix.set_penalisation_cost(1000)
        return mix.loss_func(x)