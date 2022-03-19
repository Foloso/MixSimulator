from ast import mod
from typing import List, Dict, Tuple
import json
from Moderator import Moderator
from Interfaces import Observable

class Agent(Observable):
  
    def __init__(self, id) -> None:
        super().__init__()
        self.__code_files = "../params_files/exchange_code.json"
        self.__type = "empty"
      
    def register_observer(self, moderators: List[Moderator]) -> None:
        super().register_observer(moderators)
        register_signal = json.load(open(self._code_files))["100"]
        register_signal["id"] = self.get_id()
        self._notify_observers(register_signal)

    def set_type(self, ntype):
        self.__type = ntype

    def get_type(self):
        return self.__type


