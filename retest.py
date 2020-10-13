from MixSimulator.MixSimulator import MixSimulator

mix = MixSimulator()
mix.set_data_csv("MixSimulator/data/RIToamasina/dataset_RI_Toamasina.csv")
print(mix.optimizeMix(999999999999999999999, step = 10,
                    time_index = 2))