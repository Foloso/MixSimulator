from typing import List, Dict, Tuple
from .Moderator import Moderator
import json

class Agent:
    
    def __init__(self, id, moderator) -> None:
        self._id = id
        self._moderator = moderator

    def _send_signal(self, signal) -> None:
        ## send signal to moderator
        pass

    def _get_id(self) -> str:
        return self._id

    def _register_to_moderator(self, moderator: Moderator) -> None:
        register_signal = json.loads(open("exchange_code.json"))["100"]
        register_signal["id"] = self._get_id()
        self._send_signal(register_signal)