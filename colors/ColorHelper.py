import colorsys
from typing import Tuple


def hex_to_rgb(h) -> Tuple[int]:
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

def change_hsv(hex, dh, ds, dv):
    rgb = hex_to_rgb(hex)
    h, s, v = colorsys.rgb_to_hsv(*rgb)

    # print("h", h)
    # print("s", s)
    # print("v", v)

    h += dh
    s += ds
    v /= 255
    v += dv
    
    """
    0 < h < 1
    0 < s < 1
    0 < v < 255
    """

    h = max(0, min(h, 1))
    s = max(0, min(s, 1))
    v = max(0, min(v, 1))

    v = int(v*255)

    # print("h", h)
    # print("s", s)
    # print("v", v)

    r, g, b = colorsys.hsv_to_rgb(h, s, v)

    r = int(r)
    g = int(g)
    b = int(b)

    return rgb_to_hex((r, g, b))
