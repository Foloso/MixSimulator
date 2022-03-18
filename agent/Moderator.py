from Interfaces import Observer

class Moderator(Observer):
    def __init__(self) -> None:
        super().__init__()
        self.__agent = []

    def _notify(self, observable, *args, **kwargs):
        super()._notify(observable, *args, **kwargs)
        print(observable, "sends signal code ", args[0]["code"])
        if args[0]["code"] == 100:
            self._agent.append(observable)

    def add_agent(self,agent):
        self._agent.append(agent)

    def get_agents(self,agent):
        return self.__agent
