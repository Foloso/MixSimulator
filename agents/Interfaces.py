from typing import List

class Observable:
    def __init__(self):
        self._observers = []
        self._id = None

    def get_id(self) -> str:
        return self._id

    def set_id(self, id) -> None:
        self._id = id

    def register_observer(self, observers: List) -> None:
        for observer in observers:
            if observer not in self._observers:
                self._observers.append(observer)

    def _notify_observers(self, *args, **kwargs) -> None:
        for obs in self._observers:
            obs._observe(self, *args, **kwargs)



class Observer:
  
    def _observe(self, observable, *args, **kwargs):
        pass