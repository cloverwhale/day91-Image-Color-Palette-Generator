import math
import numpy as np
from PIL import Image

PREVIEW_SIZE = 150


class ImageFile:

    def __init__(self, file):
        self.file = file
        self.img = Image.open(self.file)

    def img_arr(self):
        return np.array(self.img)

    def resized_img_arr(self):
        x = len(self.img_arr()[0])
        y = len(self.img_arr())

        scale = min(PREVIEW_SIZE / x, PREVIEW_SIZE / y)
        if scale < 1:
            x = math.floor(scale * x)
            y = math.floor(scale * y)

        resized_img = self.img.resize(size=(x, y))
        return np.array(resized_img)

    def img_arr_list(self):
        return self.img_arr().tolist()

    def resized_img_arr_list(self):
        return self.resized_img_arr().tolist()
