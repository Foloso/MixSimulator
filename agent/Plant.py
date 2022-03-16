from signal import signal
from .Agent import Agent
from .Moderator import Moderator
import json

class Plant(Agent):

    def __init__(self, id, moderator) -> None:
        super().__init__(id, moderator)

    def _notify_is_up(self) -> None:
        signal = json.loads(open("exchange_code.json"))["200"]
        signal["id"] = self._get_id()
        self._send_signal(signal)

    def _notify_is_down(self) -> None:
        signal = json.loads(open("exchange_code.json"))["400"]
        signal["id"] = self._get_id()
        self._send_signal(signal)

    def _notify_disponibility(self) -> None:
        pass