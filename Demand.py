class Demand:
    """
        Manage the Demands data
    """
    def __init__(self):
        self.__demandeData = {}
        pass

    def getDemande(self, timerange: range=range(0,24)) -> dict[float, float]:
        #get demand per hour in a day 
        demand = {}
        for i in timerange:
            demand.update(i, self.__demandData.get(i))
        return demand