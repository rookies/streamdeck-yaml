#!/usr/bin/python
"""
Class that renders the information about a key (icon, title, ...) as an image.
"""
import os.path
from PIL import Image, ImageFont, ImageDraw
from keys.generic import Key

ICON_PATH = os.path.join(os.path.dirname(__file__), "../../resources/icons")


class ImageRenderer:
    # pylint: disable=too-few-public-methods
    """
    Class that renders the information about a key (icon, title, ...) as an image.
    """

    def __init__(self, size, config):
        self._config = config
        self._size = size

    def render(self, key: Key) -> Image:
        """
        Renders an image for the given key and returns the Pillow image.
        """
        # Create blank image:
        result = Image.new("RGBA", self._size, (255, 255, 255))

        # Add icon:
        with Image.open(os.path.join(ICON_PATH, f"{key.icon}.png")).convert(
            "RGBA"
        ) as icon:
            result.alpha_composite(
                icon, ((result.size[0] - icon.size[0]) // 2, self._config["padding"])
            )

        # Add text:
        font = self._get_fitting_font(key.title)
        result_draw = ImageDraw.Draw(result)
        result_draw.text(
            (result.size[0] // 2, result.size[1] - self._config["padding"]),
            key.title,
            font=font,
            anchor="mb",
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

            if font.getsize(text)[0] > (self._size[0] - 2 * self._config["padding"]):
                return last_font
            last_font = font

        return font
