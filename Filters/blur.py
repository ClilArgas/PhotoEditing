from .abstract_filter import AbstractFilter
import numpy as np


class Blur(AbstractFilter):
    def __init__(self, params):
        super().__init__(params)

    # checked this video: https://www.youtube.com/watch?v=yb2tPt0QVPY and in GeeksForGeeks
    def apply(self, image):
        # getting the box-blur size
        x = self.params['x']
        y = self.params['y']
        # getting the image_size
        num_rows, num_cols = image.shape[0], image.shape[1]
        # avoiding errors of index out of bounce
        if num_rows < x or num_cols < y:
            return image
        # checking whether the image is colorful or gray
        rgb = image.shape[2] == 3
        output_image = blur_row = np.array([])
        # init row column pointers
        rp = cp = 0
        # moving the box through the image
        while rp <= num_rows - x:
            while cp <= num_cols - y:
                # collecting all the values corresponding to the bo
                # adding the blur pixel to the blur row
                blur_row = np.append(blur_row, self.average_pixel_by_box(image[rp:rp+x, cp:cp+y], rgb))
                cp += 1
            # adding the blur row to the output image
            output_image = np.append(output_image, blur_row)
            rp += 1
            blur_row = np.array([])
            cp = 0

        return output_image.reshape(num_rows - x + 1, num_cols - y + 1, image.shape[2])

    def average_pixel_by_box(self, box, rgb):

        shape = 3 if rgb else 1
        return np.sum(box.reshape(-1, shape), axis=0) / (self.params['x'] * self.params['y'])








