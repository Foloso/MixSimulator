# MixSimulator 
MixSimulator is an application with an optimization model for calculating and simulating the least cost of an energy mix under certain constraints. The optimizers used are based on the Nevergrad Python 3.6+ library.

The primary objective of the simulator is to study the relevance of an energy mix connected to each Inter-connected Grid through the coefficient of usage of each unit in the production cost.

## Version 0.4
The current version is a multi-agent system (MAS) approach but keeps the previous classic optimization approach available. Check `test_mas.py` for more details. (Available events are : powerplant shutdown and powerplant power_on).

An experiment on evaluating both method is available in `Experiments/Scenario_type.py` or [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1IzjJlNg3fCp14GICB2GGYYwmSIEK9yQf?usp=sharing)

#### Note
This project is a work in progress so it can not yet used in production (Many changes are on their way). Feedbacks are welcome!

### Specifications :
- Generic simulator, compatible with data from Madagascar and those from abroad (but may require data pre-processing beforehand);
- Optimization of duty cycle (or usage coefficient) under constraints ;
- Get the production cost and various performance indicators (CO2 emission, unsatisfied demand);
- Estimate of the costs of a mix or a power plant over the long term ;
- Comparison of the performance indicators on different optimizers. (see `EvaluationBudget` method)

### Perspectives :
- Add other constraints ;
- Long-term Optimization ;
- Pair with a transmission and distribution power grid simulator (MixSimulator can provide input data).

Suggestions are welcome!

## How to install
It can be installed with : 
```python
pip install mixsimulator
```
MixSimulator is written in Python 3.6 and requires the following Python packages : nevergrad, prophet, typing, numpy, pandas and matplotlib.

## How to run
As MixSimulator is a python package, it can be called and used as we can see in `test_classic.py` and `test_mas.py`.

Official documentation will accompany the first release version.

## Datasets

### Power plants dataset
The dataset "dataset_RI_Toamasina_v2.csv" is for the test and it comes from the Inter-connected energy mix of Toamasina Madagascar (2017) and Some information from the dataset is estimated.

Dataset features needed:
- `tuneable` (boolean): is the control unit controllable or not?
- `green` (boolean): is it a renewable energy plant?
- `hydro` (boolean): is it a hydro power plant?
- `fuel` (boolean): is it a thermal power plant?
- `centrals` : identification
- `fuel_consumption` (g/MWh): fuel consumption (in the case of a fossil fuel power plant)
- `availability` (%): plant availability
- `fuel_cost` ($/g): price of fuel used
- `init_value` ($): initial investment in setting up the plant
- `lifetime` (years): plant lifetime
- `carbon_production` (g/MWh): emission rate of CO2 from the power plant
- `raw_power` (MW): nominal power of the plant
- `nb_employees`: number of employees at the central level
- `mean_salary` ($): average salary of plant employees
- `demand` (MWh): electricity demand
- `lost` (MWh): electrical loss at another level (ie: transport network)

Hydro specification :
- `height` (meter): height of the stream ;
- `flow` : flow of the stream ;
- `stock_available` : water reservoir ;
- `capacity` : max water reservoir.

`nb_employees * mean_salary` **can be used as a variable cost of the plant if you want to directly use other informations as variable cost.**

### Demand and Variation datas
There is also "DIR-TOAMASINA_concat.csv" about Consumption data (in kwh, more details in `demand/`) and "dataset_RI_Toamasina_variation_template.csv" about limits in variation of power plants load following (WIP). 

**If you have datasets of any region in the world that can be used to evaluate our model, please contact us.**

## Contact
For questions and feedbacks related to the project, please send an email to r.andry.rasoanaivo@gmail.com or soloforahamefy@gmail.com or tokyandriaxel@gmail.com
