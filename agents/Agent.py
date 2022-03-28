from typing import List, Dict
import json
from .Interfaces import Observable
from threading import Timer, Lock


class Periodic(object):
    """
    A periodic task running in threading.Timers
    """
    def __init__(self):
        self._lock = Lock()
        self._timer = None
        self._stopped = True

    def set_function(self, function, *args, **kwargs):
        self.__function = function
        self.args = args
        self.kwargs = kwargs

    def set_interval(self, interval):
        self.__interval = interval

    def start(self, from_run=False):
        self._lock.acquire()
        if from_run or self._stopped:
            self._stopped = False
            self._timer = Timer(self.__interval, self._run)
            self._timer.start()
        self._lock.release()

    def _run(self):
        self.start(from_run=True)
        self.__function(*self.args, **self.kwargs)

    def stop(self):
        self._lock.acquire()
        self._stopped = True
        self._timer.cancel()
        self._lock.release()



class Agent(Observable):
  
    def __init__(self) -> None:
        ### Temporary disable id
        super().__init__()
        self._code_files = "params_files/exchange_code.json" ### TEMPORARY CHANGE FILE PATH
        self.__type = "empty"
        self._scheduled_actions = {}

    def _schedule_action(self, actions: Dict) -> None:
        ## action is a dict {function, interval}
        for action in actions.keys():
            if action not in self._scheduled_actions.keys():
                ## self._schedule_actions is a dict {function, Periodic --the class above--)}
                periodic = Periodic()
                periodic.set_function(action)
                periodic.set_interval(actions[action])
                self._scheduled_actions.update({action: periodic})
                self._scheduled_actions[action].start()
      
    def register_observer(self, moderators: List) -> None:
        super().register_observer(moderators)
        register_signal = json.load(open(self._code_files))["100"]
        register_signal["id"] = self.get_id()
        self._notify_observers(register_signal)

    def _notify_observers(self, signal:str) -> None:
        for obs in self.get_observers():
            obs.update(self, signal)

    def set_type(self, ntype):
        self.__type = ntype

    def get_type(self):
        return self.__type


