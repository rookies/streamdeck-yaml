#!/usr/bin/python
"""
Class that renders the information about a key (icon, title, ...) as an image.
"""
import os.path
import numpy
from PIL import Image, ImageFont, ImageDraw, ImageColor
from keys import KeyBase

ICON_PATH = os.path.join(os.path.dirname(__file__), "../../resources/icons")


class ImageRenderer:
    # pylint: disable=too-few-public-methods
    """
    Class that renders the information about a key (icon, title, ...) as an image.
    """

    def __init__(self, size, config):
        self._config = config
        self._size = size

    def render(self, key: KeyBase) -> Image:
        """
        Renders an image for the given key and returns the Pillow image.
        """
        # Get the key's appearance:
        appearance = key.appearance

        # Create blank, black image:
        result = Image.new("RGBA", self._size, (0, 0, 0))
        result_draw = ImageDraw.Draw(result)

        # Add white, rounded rectangle as background:
        result_draw.rounded_rectangle(
            [(0, 0), self._size],
            15,
            fill=(255, 255, 255),
        )
        # ^- TODO: Don't hardcode corner radius?

        # Add icon:
        with Image.open(os.path.join(ICON_PATH, f"{appearance['icon']}.png")).convert(
            "RGBA"
        ) as icon:
            icon_color = self._colorize_image(icon, appearance["icon_color"])
            result.alpha_composite(
                icon_color,
                ((result.size[0] - icon.size[0]) // 2, self._config["padding"]),
            )

        # Add text:
        font = self._get_fitting_font(appearance["title"])
        result_draw.text(
            (result.size[0] // 2, result.size[1] - self._config["padding"]),
            appearance["title"],
            font=font,
            anchor="ms",
            fill=(0, 0, 0),
        )

        return result.convert("RGB")

    def _get_fitting_font(self, text: str):
        """
        Returns the largest font that fits on the image with the given text, capped
        by the configured maximum fontsize.
        """
        last_font = None
        for size in range(1, self._config["max_fontsize"] + 1):
            font = ImageFont.truetype(self._config["font"], size)

            if font.getlength(text) > (self._size[0] - 2 * self._config["padding"]):
                return last_font
            last_font = font

        return font

    @staticmethod
    def _colorize_image(image: Image, color: str) -> Image:
        """
        Replaces all non-white pixels in the given image with the given color.
        """
        # Convert image into numpy array and prepare result array:
        array = numpy.array(image)
        result = numpy.zeros_like(array)

        # Find all pixels that are not [0,0,0,0]:
        mask = numpy.logical_or.reduce(numpy.not_equal(array, 0), axis=-1)

        # Colorize those pixels:
        color = ImageColor.getrgb(color)
        result[mask == True] = numpy.array(  # pylint: disable=singleton-comparison
            [color[0], color[1], color[2], 255]
        )
        # ^- TODO: Keep original alpha values?

        return Image.fromarray(result)
