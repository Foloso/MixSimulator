from Interfaces import Observer
from Interfaces import Observable


class Moderator(Observer):
    def __init__(self) -> None:
        super().__init__()
        self._agent = []

    def __add_observable(self, observable: Observable) -> None:
        if observable not in self._agent:
            self._agent.append(observable)


    def _observe(self, observable, *args, **kwargs):
        super()._observe(observable, *args, **kwargs)
        # print(observable, "sends signal code ", args[0]["code"])
        if args[0]["code"] == 100:
            self.__add_observable(observable)
