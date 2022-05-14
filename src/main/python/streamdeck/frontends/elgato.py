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


class ElgatoFrontend(Frontend):
    """
    Frontend using the python-elgato-streamdeck library, see
    https://github.com/abcminiuser/python-elgato-streamdeck
    """

    _deck = None
    _deck_serial_number = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Try to connect to device:
        if not self._connect():
            raise RuntimeError("No streamdeck found")

        # Check if layout matches:
        if self._deck.key_layout() != self._layout:
            raise RuntimeError(
                f"Streamdeck layout {self._deck.key_layout()} doesn't match expected ({self._layout})"
            )

        # Set image size:
        self.image_size = self._deck.key_image_format()["size"]

        # Create list of blank images:
        self._images = [None] * self._layout[0] * self._layout[1]

    def __del__(self):
        self._disconnect()

    def _connect(self):
        decks = DeviceManager().enumerate()
        for deck in decks:
            try:
                deck.open()
                deck_serial_number = deck.get_serial_number()
            finally:
                deck.close()

            if (
                self._deck_serial_number is None
                or self._deck_serial_number == deck_serial_number
            ):
                self._deck = deck
                self._deck_serial_number = deck_serial_number

                self._deck.open()
                self._deck.reset()
                logger.info(
                    "Opened device %s with serial number %s",
                    self._deck.deck_type(),
                    self._deck_serial_number,
                )
                self._deck.set_key_callback(self._keypress)
                return True

        logger.warning("Failed to reconnect")
        return False

    def _disconnect(self):
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
        while True:  # TODO: Add stop signal?
            if self._deck is None:
                if self._connect():
                    self.draw()
            elif not self._deck.connected():
                self._disconnect()

            self._timer_callback()
            time.sleep(1)

    def set_key(self, key_index: int, image: Image):
        # pylint: disable=missing-function-docstring
        self._images[key_index] = image

    def disable(self):
        # pylint: disable=missing-function-docstring
        self._deck.set_brightness(0)
        super().disable()

    def enable(self):
        # pylint: disable=missing-function-docstring
        self._deck.set_brightness(100)
        super().enable()

    def _keypress(self, _, key_index, state):
        """
        Callback function for key presses.
        """
        self._update_last_action()
        if state:
            self._callback(key_index)
