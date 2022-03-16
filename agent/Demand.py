import pandas as pd
import json
from typing import List, Dict
from .Agent import Agent



def massive_divergence(demande, demande2):
    return True

class Demand(Agent):
    def __init__(self, id, moderator) -> None:
        super().__init__(id, moderator)

    def set_model(self, model) -> None:
        self.__model = model

    def predict_demand(self, time_series: pd.DataFrame) -> List[float]:
        self.__demand =  list(self.__model.predict(time_series))

    def __notify_demand_value_change(self):
        signal = json.loads(open(self._code_files))["8080"]
        signal["id"] - self._get_id()
        signal["values"] = self.__demand
        signal["t_from"] = 3
        self._send_signal(signal)

    def set_demande_change(self, demand: List[float]) -> None:
        errored_demand = self.__demand
        self.__demand = demand
        if massive_divergence(errored_demand, self.__demand):
            self.__notify_demand_value_change()