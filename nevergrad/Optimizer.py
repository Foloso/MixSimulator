import nevergrad as ng

class Optimizer():
    def __init__(self):
        self.__instrum=ng.p.Array(shape=(2,))
        self.__budget=100
    
    def set_instrum(self,arg):
        self.__instrum = ng.p.Instrumentation(arg)
    
    def get_instrum(self):
        return self.__instrum
        
    def set_budget(self,budget: int=100):
        self.__budget = budget
    
    def get_budget(self):
        return self.__budget
    
    def opt_OnePlusOne(self,func_to_optimize, **constraints=None):
        optimizer = ng.optimizers.OnePlusOne(parametrization=self.get_instrum, budget=self.get_budget())
        if constraints != None:
            try:
                optimizer.parametrization.register_cheap_constraint(lambda x: constraints["carbonCost"](x) <= constraints["carbonCostLimit"])
            except:
                pass
            try:
                optimizer.parametrization.register_cheap_constraint(lambda x: x <= constraints["availability"])
            except:
                pass
            try:    
                for index in constraints["nonTuneable"]:
                    optimizer.parametrization.register_cheap_constraint(lambda x: x[index] == constraints["availability"][index])
            except:
                pass
            optimizer.parametrization.register_cheap_constraint(lambda x: x[index] == constraints["availability"][index])

        recommendation = optimizer.minimize(func_to_optimize)
        return recommendation.value