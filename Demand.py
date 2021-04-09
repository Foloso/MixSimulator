from math import pi
from math import cos, floor
from prophet import Prophet 
import pandas as pd

class Demand:
    """
        Manage the Demands data
    """    
    
    def __init__(self, demand: float = 20, var_per_day: float = 0.1 , var_per_season: float = 0.1) -> None:
        self.__var_per_day = var_per_day
        self.__var_per_season = var_per_season
        self.__mean_demand = demand
        self.__pt = Prophet(seasonality_mode='multiplicative')
        self.__periods = 12*20
        
        self.data_demand = None

    def set_forcast_periods(self, periods) -> None:
        self.__periods = periods
    
    def set_data_csv(self, bind = None, init_date: str = "2017-01-01", delimiter: str = ";", column: str = "Total Ventes"):
        """
            The method must get a dataset with at least 3 columns
            - month : int, 
            - year : int,
            - the monthly demand in kwh (determinated by the parameter "column")
            
            The method use also a forcast model from prophet to predict future demand.
            The periods can be set by set_forcast_periods.
        """        
        data = pd.read_csv(bind, delimiter = delimiter) 
        data["date"]= data ["month"].astype("str") + "-" + data ["year"].astype("str")
        data["datetime"] = pd.to_datetime(data["date"])
        data_to_use = pd.DataFrame()
        data_to_use[["datetime","demands"]] = data.loc[data["datetime"] >= init_date][["datetime",column]]
        
        #let's forcast
        train = pd.DataFrame()
        train[["ds","y"]] = data[["datetime",column]]
        self.__pt.fit(train)
        future = self.__pt.make_future_dataframe(periods = self.__periods, freq='MS')
        fcst = self.__pt.predict(future)
        fcst = fcst.loc[fcst["ds"] > data["datetime"].tail(1).item()]
        fcst[["datetime","demands"]] = fcst[["ds","yhat"]]
        self.data_demand = data_to_use.append(fcst,ignore_index=True)
        
        return self.data_demand
       
    def get_demand(self, t):
        self.data_demand.reset_index()
        try :
            return self.data_demand.iloc[t]["demands"]/1000 #cause data units in kwh
        except IndexError :
            print("Please check init_date or change the forcasting params : increase periods with Demand.set_forcast_periods")
            raise

    def set_mean_demand(self, demand: float):
        self.__mean_demand = demand

    def get_demand_approxima(self, t, interval):
        demande = self.__mean_demand * (1 + cos(4 * pi * ( t * interval )/ 24)*self.__var_per_day + cos(2 * pi * ( t * interval ) / (24*365))* self.__var_per_season)
        return demande
        
    def get_demand_monthly(self, t, interval):
        m = t/(24*30)
        m = floor(m)
        # for now we divide it by 30*24 (better approximation TO DO)
        demande = (self.get_demand(m)/(30*24)) * (1 + cos(4 * pi * ( t * interval )/ 24)*self.__var_per_day)
        return demande
