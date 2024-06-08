from abc import ABC, abstractmethod


class AbstractAdjustment(ABC):

    def __init__(self,level):
        self.level = level

    @abstractmethod
    def apply(self, image):
        pass
