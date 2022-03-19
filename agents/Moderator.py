from Interfaces import Observer, Observable

class Moderator(Observer):
    def __init__(self) -> None:
        super().__init__()
        self.__agent = []

    def add_agent(self,agent):
        self._agent.append(agent)

    def get_agents(self,agent):
        return self.__agent
      
    def __add_observable(self, observable: Observable) -> None:
        if observable not in self.__agent:
            self.__agent.append(observable)

    def _observe(self, observable, *args, **kwargs):
        super()._observe(observable, *args, **kwargs)
        print(observable, "sends signal code ", args[0]["code"])
        if args[0]["code"] == 100:
            self.__add_observable(observable)
