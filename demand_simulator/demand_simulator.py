import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


def get_accuracy(original_score, pred):
    return ((original_score-pred)**2).sum()


data = pd.read_csv("../data/RIToamasina/demand/toamasina_demand.csv")
columns = ['MT/HT Abonnes', 'BT Abonnes', 'Total Abonnes', 'year', 'month']
train = data.loc[data["year"]!=2017]
test = data.loc[data["year"]==2017]

X_train = train[columns] 
y_1_train = train["Production Brute Totale"]
y_2_train = train["Total Ventes"]

X_test = test[columns]
y_1_test = test["Production Brute Totale"]
y_2_test = test["Total Ventes"]


reg = LinearRegression().fit(X_train, y_1_train)

pred = reg.predict(X_test)

print(get_accuracy(pred, y_1_test))