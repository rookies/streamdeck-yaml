#!/usr/bin/python3
"""
Abstract base class for all frontends.
"""

import time
import logging
from abc import ABC, abstractmethod
from PIL import Image

REQUIRED_PARAMETERS = ["rows", "columns"]
logger = logging.getLogger("streamdeck.frontends.frontend")


class Frontend(ABC):
    """
    Abstract base class for all frontends.
    """

    _enabled = True

    def __init__(self, callback, **kwargs):
        # Store callback function:
        self._callback = callback

        # Check required parameters:
        missing = []
        for param in REQUIRED_PARAMETERS:
            if param not in kwargs:
                missing.append(param)
        if len(missing) > 0:
            raise ValueError("Missing frontend parameters: {', '.join(missing)}")

        # Store layout and timeout:
        self._layout = (kwargs["rows"], kwargs["columns"])
        self._timeout = kwargs.get("timeout")

        # Store last action:
        self._last_action = time.monotonic()

    @abstractmethod
    def clear(self):
        """
        Clears all keys without actually updating them.
        """

    @abstractmethod
    def draw(self):
        """
        Updates the keys with the current configuration set via clear() and
        set_key().
        """

    @abstractmethod
    def run(self):
        """
        Implements the frontend main loop.
        """

    @abstractmethod
    def set_key(self, key_index: int, image: Image):
        """
        Sets the image for the key with the given index.
        """

    def disable(self):
        """
        Disables the display of the frontend. Has to set self._enabled
        to False.
        """
        self._enabled = False

    def enable(self):
        """
        Enables the display of the frontend. Has to set self._enabled
        to True.
        """
        self._enabled = True

    @property
    def enabled(self) -> bool:
        """
        Whether the display of the frontend is enabled or not.
        """
        return self._enabled

    def _timer_callback(self) -> bool:
        """
        Callback function that has to be called by the implementing
        class at least once a second.

        :return: always True
        """
        if (
            self._enabled
            and self._timeout is not None
            and time.monotonic() >= self._last_action + self._timeout
        ):
            self.disable()
            logger.info("Disabled frontend after %d seconds", self._timeout)

        return True

    def _update_last_action(self):
        """
        Updates the time of the last action to reset the timeout. Has to
        be called by the implementing class at each keypress.
        """
        self._last_action = time.monotonic()
