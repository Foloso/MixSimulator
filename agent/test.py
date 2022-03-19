from Plant import Plant
from Moderator import Moderator


mod = Moderator()

plants = []
for i in range(5):
    tmp = Plant()
    tmp.set_id("plant_"+str(i))
    tmp.register_observer([mod])
    plants.append(tmp)

# plants[0].notify_is_up()
# subject = Observable()
# observer = Observer(subject)
# subject.notify_observers("test", kw="python")