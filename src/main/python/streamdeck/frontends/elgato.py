#!/usr/bin/python3
"""
Frontend using the python-elgato-streamdeck library, see
https://github.com/abcminiuser/python-elgato-streamdeck
"""
import time
import logging
from PIL import Image
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper
from frontends import Frontend

logger = logging.getLogger("streamdeck.frontends.elgato")
# TODO: Implement automatic reconnect


class ElgatoFrontend(Frontend):
    """
    Frontend using the python-elgato-streamdeck library, see
    https://github.com/abcminiuser/python-elgato-streamdeck
    """

    _deck = None

    def __init__(self, rows, columns, callback):
        decks = DeviceManager().enumerate()
        if len(decks) != 1:
            raise RuntimeError("Found no or multiple streamdecks")
        self._deck = decks[0]
        self._deck.open()
        self._deck.reset()
        logger.info(
            "Opened device %s with serial number %s",
            self._deck.deck_type(),
            self._deck.get_serial_number(),
        )

        # Register callback:
        self._deck.set_key_callback(self._keypress)
        self._callback = callback

        # Check if layout matches:
        if self._deck.key_layout() != (rows, columns):
            raise RuntimeError(
                f"Streamdeck layout {self._deck.key_layout()} doesn't match expected ({rows},{columns})"
            )

        # Set image size:
        self.image_size = self._deck.key_image_format()["size"]

        # Create list of blank images:
        self._images = [None] * rows * columns

    def __del__(self):
        if self._deck is not None:
            self._deck.close()
            self._deck = None

    def clear(self):
        # pylint: disable=missing-function-docstring
        for i, _ in enumerate(self._images):
            self._images[i] = None

    def draw(self):
        # pylint: disable=missing-function-docstring
        with self._deck:
            for i, image in enumerate(self._images):
                if image is None:
                    native_img = self._deck.BLANK_KEY_IMAGE
                else:
                    native_img = PILHelper.to_native_format(self._deck, image)

                self._deck.set_key_image(i, native_img)

    def run(self):
        # pylint: disable=missing-function-docstring
        while self._deck.is_open():
            time.sleep(1)

    def set_key(self, key_index: int, image: Image):
        # pylint: disable=missing-function-docstring
        self._images[key_index] = image

    def _keypress(self, _, key_index, state):
        """
        Callback function for key presses.
        """
        if state:
            self._callback(key_index)
