from ast import mod
from typing import List, Dict, Tuple
import json
from . import Moderator
from .Interfaces import Observable

class Agent(Observable):
  
    def __init__(self) -> None:
        ### Temporary disable id
        super().__init__()
        self.__code_files = "params_files/exchange_code.json" ### TEMPORARY CHANGE FILE PATH
        self.__type = "empty"
      
    def register_observer(self, moderators: List) -> None:
        super().register_observer(moderators)
        register_signal = json.load(open(self.__code_files))["100"]
        register_signal["id"] = self.get_id()
        self.__notify_observers(register_signal)

    def __notify_observers(self, signal:str) -> None:
        for obs in self.get_observers():
            obs.update(self, signal)

    def set_type(self, ntype):
        self.__type = ntype

    def get_type(self):
        return self.__type


