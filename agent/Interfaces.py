class Observable:
    def __init__(self):
        self._observers = []

    def register_observer(self, observer):
        self._observers.append(observer)

    def notify_observers(self, *args, **kwargs):
        for obs in self._observers:
            obs._notify(self, *args, **kwargs)


class Observer:

    def _notify(self, observable, *args, **kwargs):
        pass