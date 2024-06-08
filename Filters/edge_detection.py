from .abstract_filter import AbstractFilter
import numpy as np


class EdgeDetection(AbstractFilter):
    def __init__(self, params):
        super().__init__(params)

    # Watched ComputerPhil video in YouTube about edge detection filter
    def apply(self, image):
        # gray_scaling the image
        gray_image = self.rgb2gray(rgb=image)

        # created edge detection matrices for X axis and Y axis
        G_x = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
        G_y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])

        rows, cols = gray_image.shape
        output_image = np.zeros(shape=(rows, cols))
        for i in range(rows-2):
            for j in range(cols-2):
                g_x = np.sum(np.multiply(G_x, gray_image[i:i + 3, j:j + 3]))
                g_y = np.sum(np.multiply(G_y, gray_image[i:i + 3, j:j + 3]))
                pixel = np.sqrt(g_x ** 2 + g_y ** 2)
                output_image[i+1][j+1] = pixel

        # normalize the image to 0-255
        output_image = (output_image / np.max(output_image)) * 255

        return output_image

    # checked in StackOverFlow how to convert an Image to grayscale
    @staticmethod
    def rgb2gray(rgb):
        r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
        gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

        return gray
