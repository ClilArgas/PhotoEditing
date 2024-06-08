from .abstract_adjustment import AbstractAdjustment
import numpy as np

class Brightness(AbstractAdjustment):

    def __init__(self, level):
        super().__init__(level)

    def apply(self, image):
        # add constant to all the array
        image = image.astype(np.float32)
        image += self.level
        image = np.clip(image, 0, 255)
        return image


