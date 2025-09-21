from tempfile import TemporaryFile
from colorthief import ColorThief
from PIL import Image
import math
import colorsys

def is_vibrant(rgb, min_saturation = 0.3, min_brightness = 0.3):
    r, g, b = [x/255.0 for x in rgb]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return s >= min_saturation and v >= min_brightness

def get_file(file_path):
    """Get a PIL acceptable input file reference.

    Allows us to mock patch during testing to make BytesIO stream.
    """
    return file_path


def get_cropped_image(file_handler, crop_area):
    im = Image.open(file_handler)
    if crop_area['active']:
        im_width, im_height = im.size
        im = im.crop((
            math.floor(im_width / 100 * crop_area['x']),
            math.floor(im_height / 100 * crop_area['y']),
            math.floor(im_width / 100 * (crop_area['x'] + crop_area['w'])),
            math.floor(im_width / 100 * (crop_area['y'] + crop_area['h'])),
        ))
    return im


def get_color_from_image(im, color_count = 10, accuracy = 10, min_saturation = 0.3, min_brightness = 0.3) -> tuple:
    file_handler = TemporaryFile()
    im.save(file_handler, "PNG")
    return get_color_from_file(file_handler, color_count, accuracy, min_saturation, min_brightness)


def get_color_from_file(file_handler, color_count = 10, accuracy = 10, min_saturation = 0.3, min_brightness = 0.3) -> tuple:
    """Given an image file, extract the predominant color from it."""
    color_thief = ColorThief(file_handler)
    palette = color_thief.get_palette(color_count=color_count, quality=accuracy)
    vibrant_colors = [color for color in palette if is_vibrant(color, min_saturation, min_brightness)]
    return vibrant_colors[0] or (0, 0 ,0)
