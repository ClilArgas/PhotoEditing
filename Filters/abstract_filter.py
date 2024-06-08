from abc import ABC, abstractmethod


class AbstractFilter(ABC):
    def __init__(self, params):
        self.params = params

    @abstractmethod
    def apply(self, image):
        pass
