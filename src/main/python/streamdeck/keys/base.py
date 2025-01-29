#!/usr/bin/python
"""
Contains an abstract base class for key classes.
"""
import enum
from abc import ABC, abstractmethod
from typing import Tuple


class KeyPressResult(enum.Enum):
    """
    Result of a key press.

    MENU_ENTER: Enter the submenu given as `details`
    MENU_BACK: Return from submenu, `details` is None
    REDRAW: Redraw the display, `details` is None
    """

    MENU_ENTER = 1
    MENU_BACK = 2
    REDRAW = 3


class KeyBase(ABC):
    """
    Abstract base class for key classes.
    """

    def __init__(self, values, backend):
        self._values = values
        self._backend = backend

        if "icon" in self._values:
            self._icon = self._values["icon"]
        elif not hasattr(self, "_icon"):
            self._icon = "help"

        if "icon_color" in self._values:
            self._icon_color = self._values["icon_color"]
        elif not hasattr(self, "_icon_color"):
            self._icon_color = "black"

        if "title" in self._values:
            self._title = self._values["title"]
        elif not hasattr(self, "_title"):
            self._title = self.__class__.__name__

    @property
    def appearance(self):
        """
        Returns the appearance of the key.
        """
        return {
            "title": self._title,
            "icon": self._icon,
            "icon_color": self._icon_color,
        }

    @abstractmethod
    def pressed(self) -> Tuple[KeyPressResult, dict]:
        """
        This method is called when the key is pressed.

        :return: a tuple (result, details)
        """

    def _trigger_redraw(self):
        """
        Triggers a redraw of all keys.
        """
        # TODO: Implement!
