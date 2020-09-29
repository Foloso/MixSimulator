# MixSimulator (Version 0.2)
MixSimulator is an application with an optimization model for calculating and simulating the least cost of an energy mix under certain constraints. The optimizers used are based on the Nevergrad Python 3.6+ library.

The primary objective of the simulator is to study the relevance of an energy mix connected to each Inter-connected Grid through the coefficient of usage of each unit in the production cost.

Specifications :
- 
- Generic simulator, compatible with data from Madagascar and those from abroad (but may require pre-processing beforehand);
- Optimization of duty cycle (or usage coefficient) under the chosen constraints ;
- Deduction of production costs and various performance indicators (CO2 emission, unsatisfied demand);
- Comparison between the usage coefficients of the current mix and the calculated optimal mix ;
- Comparison of the performance indicators on different optimizers.


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

List of classes and directories :
- MixSimulator : System basis (Simulation with / without optimization) ;
- SegmentOptimizer : Initiate appropriate optimization and power plants (Define objective function and constraints; Manage data entries; Calculate value of explanatory variables) ;
- nevergradBased/Optimizer : Adaptation of the Nevergrad optimizers to the project and auto-parameterization ;
- centrals/PowerCentral : Gathers all the common specifications of the control units (central) ;
- Evaluation : Class for evaluating mix based on performance indicators on several optimizers ;
- data/ : Groups the available datasets. 

Official documentation will accompany the first release version.

# DataSet
The dataset "data/dataset_RI_Toamasina" is for the test and it comes from the Inter-connected energy mix of Toamasina Madagascar (2018) and Some information from the dataset is estimated.

Dataset features needed:
- tuneable (boolean): is the control unit controllable or not?
- green (boolean): is it a renewable energy plant?
- centrals : identification
- fuel_consumption (g/MWh): fuel consumption (in the case of a fossil fuel power plant)
- availability (%): plant availability
- fuel_cost ($/g): price of fuel used
- init_value ($): initial investment in setting up the plant
- lifetime (years): plant lifetime
- carbon_production (g/MWh): emission rate of CO2 from the power plant
- raw_power (MW): nominal power of the plant
- nb_employees: number of employees at the central level
- mean_salary ($): average salary of plant employees
- demand (MWh): electricity demand
- lost (MWh): electrical loss at another level (ie: transport network)

"nb_employees * mean_salary" can be used as a variable cost of the plant if you want to directly use other informations as variable cost.

# Contact
For questions and feedbacks related to the project, please send an email to r.andry.rasoanaivo@gmail.com or soloforahamefy@gmail.com or tokyandriaxel@gmail.com

# Note
This project is a work in progress so it can not yet used in production (Many changes are on their way). Feedbacks are welcome!

Here is a list of available optimizers:
'cGA', 'SplitOptimizer', 'RecombiningPortfolioOptimisticNoisyDiscreteOnePlusOne', 'RecES', 'RealSpacePSO', 'RandomSearchPlusMiddlePoint', 'QrDE', 'QORandomSearch', 'OptimisticNoisyOnePlusOne', 'OptimisticDiscreteOnePlusOne', 'ORandomSearch', 'NoisyOnePlusOne', 'NoisyDiscreteOnePlusOne', 'NoisyDE', 'NoisyBandit', 'NelderMead', 'NaiveTBPSA', 'NaiveIsoEMNA', 'LhsDE', 'FCMA', 'ES', 'DoubleFastGADiscreteOnePlusOne', 'DiscreteOnePlusOne', 'CauchyOnePlusOne', 'CM', 'AlmostRotationInvariantDE', 'TwoPointsDE', 'RandomSearch', 'OnePlusOne', 'DE', 'CMA', 'PSO', 'TBPSA'
