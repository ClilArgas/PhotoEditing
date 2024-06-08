import numpy as np
from .abstract_filter import AbstractFilter
from .edge_detection import EdgeDetection


class Sharpen(AbstractFilter):
    def __init__(self, params):
        super().__init__(params)

    def apply(self, image):
        edge = EdgeDetection(params={})
        edge_detect = edge.apply(image)
        rows, cols = image.shape[0], image.shape[1]
        for i in range(rows):
            for j in range(cols):
                for k in range(image.shape[2]):
                    image[i][j][k] += self.params['alpha'] * edge_detect[i][j]

        # normalize image to range of 0-255
        image = (image / np.max(image)) * 255
        return image

