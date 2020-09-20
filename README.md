# MixSimulator (Version 0.1)
MixSimulator is an application with an optimization model for calculating and simulating the least cost of an energy mix under certain constraints. The optimizers used are based on the Nevergrad Python 3.6+ library.

The primary objective of the simulator is to study the relevance of an energy mix connected to each Inter-connected Grid through the coefficient of usage of each unit in the production cost.

Specifications :
- 
- Generic simulator, compatible with data from Madagascar and those from abroad (but may require pre-processing beforehand);
- Optimization of duty cycle (or usage coefficient) under the chosen constraints ;
- Deduction of production costs and various performance indicators (CO2 emission);
- Evaluation of the relevance of the installation of a new plant ;
- Comparison between the usage coefficients of the current mix and the calculated optimal mix.


Perspectives :
- 
- Add other constraints (storage of hydroelectric plants, variation in production) ;
- Estimate of the costs of a mix or a power plant over the long term ;
- Pair with a transmission and distribution power grid simulator (MixSimulator can provide input data).

Suggestions are welcome!

# Requirements
MixSimulator is written in Python 3.6 and requires the following Python packages : nevergrad, typing, numpy, pandas and matplotlib. (make sure you have those packages)

# How to run
As MixSimulator is a python package, it can be called and used as we can see in main.py.

- The main class is in MixSimlator.py ;
- It uses the nevergrad adapted class nevergradBased/Optimizer ;
- And the centrals manager centrals/PowerCentral ;
- There is an exemple of use in main.py.

Official documentation will accompany the first release version.

# DataSet
The dataset "data/dataset_RI_Toamasina" is for the test and it comes from the Inter-connected energy mix of Toamasina Madagascar (2018) and Some information from the dataset is estimated.

# Contact
For questions and feedbacks related to the project, please send an email to r.andry.rasoanaivo@gmail.com or soloforahamefy@gmail.com or tokyandriaxel@gmail.com

# Note
This project is a work in progress so it can not yet used in production (Many changes are on their way). Feedbacks are welcome!
