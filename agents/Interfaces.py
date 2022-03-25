from typing import List

class Observable:
    def __init__(self):
        self.__observers = []
        self.__id = None

    def get_id(self) -> str:
        return self.__id

    def set_id(self, id) -> None:
        self.__id = id

    def get_observers(self) -> List :
        return self.__observers

    def register_observer(self, observers: List) -> None:
        for observer in observers:
            if observer not in self.__observers:
                self.__observers.append(observer)

    def __notify_observers(self, *args, **kwargs) -> None:
        pass



class Observer:
  
    def update(self, observable, *args, **kwargs):
        pass