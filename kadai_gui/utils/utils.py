import re
import kadai
import string
import random
from kadai.themer import Themer
from kadai.config_handler import ConfigHandler
from PIL import Image, ImageDraw

configHandler = ConfigHandler()
configHandler.save()
kadai_config = configHandler.get()


def getRandomString(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def resizeString(string, length):
    if len(string) > length:
        pre_string = string[: int((length / 2))]
        post_string = string[-int((length / 2)) :]

        string = "{}...{}".format(pre_string, post_string)

    return string


def getScaledDimensions(dimensions, new_width):
    ratio = dimensions[0] / new_width
    scaled_width = int(dimensions[0] / ratio)
    scaled_height = int(dimensions[1] / ratio)

    return (scaled_width, scaled_height)


def getPallete(image_path, engine):
    pallete = None
    themer = Themer(image_path, kadai_config["data_directory"], config=kadai_config)
    try:
        pallete = themer.getColorPallete()
    except kadai.utils.FileUtils.noPreGenThemeError:
        themer.setEngine(engine)
        themer.generate()
        pallete = themer.getColorPallete()

    return pallete


def getColorsFromPallete(pallete):
    pallete = [pallete[i] for i in sorted(pallete, key=natural_keys)]
    return [kadai.utils.ColorUtils.hex_to_rgb(color) for color in pallete]


def generatePalleteImage(image_path, engine=kadai_config["engine"]):
    pallete_segment_width = int((700 * 0.9) / 8)
    pallete_segment_height = 30

    pallete = getPallete(image_path, engine)
    colors = getColorsFromPallete(pallete)

    pallete_image = Image.new(
        "RGB", (8 * pallete_segment_width, 2 * pallete_segment_height), (0, 0, 0)
    )
    draw_pallete = ImageDraw.Draw(pallete_image)

    for i in range(8):
        for j in range(2):
            color = colors[i + (8 * j)]
            draw_pallete.rectangle(
                (
                    (pallete_segment_width * i, pallete_segment_height * j),
                    (
                        (pallete_segment_width * i) + pallete_segment_width,
                        (pallete_segment_height * j) + pallete_segment_height,
                    ),
                ),
                fill=color,
            )

    return pallete_image


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split(r"(\d+)", text)]
