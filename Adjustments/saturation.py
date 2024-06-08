from . abstract_adjustment import AbstractAdjustment
import numpy as np


class Saturation(AbstractAdjustment):
    def __init__(self, level):
        super().__init__(level)

    # checked with ChatGpt prompt: show me the mathematical equation for image saturation
    def apply(self, image):
        # built this code but it ran slow: so i gave it to chatgpt and told him implmement the same logic with numpy
        #     if image.shape[2] == 1:
        #         return image
        #     num_rows, num_cols, num_features = image.shape
        #     for i in range(num_rows):
        #         for j in range(num_cols):
        #             norm_colors = image[i][j] / 255
        #             V = max(norm_colors)
        #             delta = V - min(norm_colors)
        #             S = 0 if V == 0 else delta / V
        #             H = 0 if delta == 0 else 60 * (((norm_colors[1] - norm_colors[2])/delta) % 6) if V == norm_colors[0] \
        #                 else 60 * (((norm_colors[2] - norm_colors[0])/delta) + 2) if V == norm_colors[1] \
        #                 else 60 * (((norm_colors[0] - norm_colors[1])/delta) + 2)
        #             H %= 360
        #             S_tag = np.clip(S * self.level, 0, 1)
        #             C = V * S_tag
        #             X = C * (1 - abs(((H/60) % 2) - 1))
        #             m = V - C
        #             r_tag = g_tag = b_tag = 0
        #             lower, upper = 0, 60
        #             rgb_based_on_h = {
        #                 0: (C, X, 0),
        #                 1: (X, C, 0),
        #                 2: (0, C, X),
        #                 3: (0, X, C),
        #                 4: (X, 0, C),
        #                 5: (C, 0, X)
        #             }
        #
        #             for k in range(6):
        #                 if lower + k * 60 <= H < upper + k * 60:
        #                     r_tag, g_tag, b_tag = rgb_based_on_h[k]
        #
        #             modified_rgb = [(r_tag + m)*255, (g_tag + m)*255, (b_tag + m)*255]
        #             image[i][j] = modified_rgb

        if len(image.shape) < 3 or image.shape[2] == 1:  # If the image is grayscale
            return image

        # Normalize the image to [0, 1]
        norm_image = image / 255.0

        # Convert RGB to HSV
        max_vals = np.max(norm_image, axis=2)
        min_vals = np.min(norm_image, axis=2)
        delta_vals = max_vals - min_vals

        # Value (V) channel
        V = max_vals

        # Saturation (S) channel
        S = np.zeros_like(max_vals)
        mask = V != 0
        S[mask] = delta_vals[mask] / V[mask]

        # Hue (H) channel calculation
        H = np.zeros_like(max_vals)
        mask_r = (max_vals == norm_image[..., 0])
        mask_g = (max_vals == norm_image[..., 1])
        mask_b = (max_vals == norm_image[..., 2])

        H[mask_r] = 60 * ((norm_image[..., 1] - norm_image[..., 2]) / delta_vals % 6)[mask_r]
        H[mask_g] = 60 * (((norm_image[..., 2] - norm_image[..., 0]) / delta_vals) + 2)[mask_g]
        H[mask_b] = 60 * (((norm_image[..., 0] - norm_image[..., 1]) / delta_vals) + 4)[mask_b]

        H = H % 360

        # Adjust the Saturation by the given level
        S *= self.level
        S = np.clip(S, 0, 1)

        # Convert HSV back to RGB
        C = V * S
        X = C * (1 - np.abs((H / 60) % 2 - 1))
        m = V - C

        Z = np.zeros_like(C)

        h_0 = (0 <= H) & (H < 60)
        h_1 = (60 <= H) & (H < 120)
        h_2 = (120 <= H) & (H < 180)
        h_3 = (180 <= H) & (H < 240)
        h_4 = (240 <= H) & (H < 300)
        h_5 = (300 <= H) & (H < 360)

        r = np.where(h_0 | h_5, C, np.where(h_1 | h_4, X, Z)) + m
        g = np.where(h_0 | h_3, X, np.where(h_2 | h_5, C, Z)) + m
        b = np.where(h_0 | h_1, Z, np.where(h_2 | h_3, X, C)) + m

        # Stack and convert back to 255 scale
        image = (np.stack([r, g, b], axis=-1) * 255)
        return image
