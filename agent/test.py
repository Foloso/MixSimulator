from Powerplant import Powerplant
from Moderator import Moderator


mod = Moderator()

plants = []
for i in range(5):
    tmp = Powerplant("plant_"+str(i))
    tmp.register_to_moderator([mod])
    plants.append(tmp)

# plants[0].notify_is_up()
# subject = Observable()
# observer = Observer(subject)
# subject.notify_observers("test", kw="python")