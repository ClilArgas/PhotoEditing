import numpy as np

from .abstract_adjustment import AbstractAdjustment


class Contrast(AbstractAdjustment):

    def __init__(self, level):
        super().__init__(level)

    def apply(self, image):
        # ChatGpt prompt: what is the formula for contrast image
        image = image.astype(np.float32)
        image = 128 + self.level * (image - 128)
        image = np.clip(image, 0, 255)
        return image
