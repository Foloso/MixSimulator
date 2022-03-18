from typing import List, Dict, Tuple
import json
from Moderator import Moderator
from Interfaces import Observable

class Agent(Observable):
    
    def __init__(self, id) -> None:
        self._code_files = "../params_files/exchange_code.json"
        self._id = id
        self._observers = []

    def _notify_moderator(self, signal) -> None:
        self.notify_observers(signal)

    def get_id(self) -> str:
        return self._id

    def register_to_moderator(self, moderators: List[Moderator]) -> None:
        self._observers += moderators
        self._observers = list(set(self._observers))
        register_signal = json.load(open(self._code_files))["100"]
        register_signal["id"] = self.get_id()
        self._notifiy_moderator(register_signal)