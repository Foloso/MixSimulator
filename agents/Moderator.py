from typing import List
from Interfaces import Observer, Observable

class Moderator(Observer):
    def __init__(self) -> None:
        super().__init__()
        self.__observable = []

    def get_observable(self) -> List[Observable]:
        return self.__observable

    def set_observable(self, observables: List[Observable]) -> None:
        self.__observable = observables
      
    def __add_observable(self, observable: Observable) -> None:
        if observable not in self.__observable:
            self.__observable.append(observable)

    def _observe(self, observable, *args, **kwargs) -> None:
        super()._observe(observable, *args, **kwargs)
        print(observable, "sends signal code ", args[0]["code"])
        if args[0]["code"] == 100:
            self.__add_observable(observable)
