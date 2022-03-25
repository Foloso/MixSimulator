from Moderator import Moderator
from ..power_plants.mas.PowerPlant import PowerPlant as Plant

mod = Moderator()

plants = []
for i in range(5):
    tmp = Plant()
    tmp.set_id("plant_"+str(i))
    tmp.register_observer([mod])
    plants.append(tmp)