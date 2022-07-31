import math

DELTA = 35


class ColorPalette:

    def __init__(self, img_arr_list):
        self.data = img_arr_list
        self.smooth_data = self.round_color(self.data)
        self.rgb_arr = self.rgb_statistics(self.smooth_data)

    def round_color(self, img_arr_list):
        for i in range(len(img_arr_list)):
            for j in range(len(img_arr_list[i])):
                r = self.rounding(img_arr_list[i][j][0])
                g = self.rounding(img_arr_list[i][j][1])
                b = self.rounding(img_arr_list[i][j][2])
                img_arr_list[i][j] = (r, g, b)
        return img_arr_list

    def rounding(self, num):
        half_delta = DELTA / 2 - 1
        rounded = math.floor((num + half_delta) / DELTA) * DELTA
        if rounded >= 256:
            return 255
        else:
            return rounded

    def rgb_statistics(self, img_arr_list):
        dict_holder = dict()
        for i in range(len(img_arr_list)):
            for j in range(len(img_arr_list[i])):
                obj = tuple(img_arr_list[i][j])
                dict_holder[obj] = dict_holder.get(obj, 0) + 1
        return dict_holder

    def get_major_color(self):
        order_sorted = sorted(self.rgb_arr.items(), key=lambda x: x[1], reverse=True)
        major_color_rgb = [item[0] for item in order_sorted[:10]]
        major_color_hex = ['#%02x%02x%02x' % item for item in major_color_rgb]
        return major_color_rgb, major_color_hex
