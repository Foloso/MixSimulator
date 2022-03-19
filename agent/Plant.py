import json
from typing import List
from Agent import Agent
from Moderator import Moderator

class Plant(Agent):
 
    def _notify_is_up(self) -> None:
        signal = json.load(open(self._code_files))["200"]
        signal["id"] = self.get_id()
        self._notify_observers(signal)

    def _notify_is_down(self) -> None:
        signal = json.load(open(self._code_files))["400"]
        signal["id"] = self.get_id()
        self._notify_observers(signal)

    def _notify_disponibility(self) -> None:
        pass