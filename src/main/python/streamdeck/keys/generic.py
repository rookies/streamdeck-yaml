#!/usr/bin/python
"""
Contains an abstract base class for key classes as well as some generic key classes.
"""
import enum
import os.path
from abc import ABC, abstractmethod

ICON_PATH = os.path.join(os.path.dirname(__file__), "../../../resources/icons")


class KeyPressResult(enum.Enum):
    """
    Result of a key press.

    MENU_ENTER: Enter the submenu
    MENU_BACK: Return from submenu
    REDRAW: Redraw the display
    """

    MENU_ENTER = 1
    MENU_BACK = 2
    REDRAW = 3


class Key(ABC):
    """
    Abstract base class for key classes.
    """

    def __init__(self, values, backend):
        self._values = values
        self._backend = backend

        if "icon" in self._values:
            self._icon = self._values["icon"]
        elif not hasattr(self, "_icon"):
            self._icon = "unknown"

        if "title" in self._values:
            self._title = self._values["title"]
        elif not hasattr(self, "_title"):
            self._title = self.__class__.__name__

    @property
    def title(self):
        """
        Returns the title for the key.
        """
        return self._title

    @property
    def icon_path(self):
        """
        Returns the path to the icon for the key.
        """
        return os.path.join(ICON_PATH, f"{self._icon}.png")

    @abstractmethod
    def pressed(self) -> KeyPressResult:
        """
        This method is called when the key is pressed.
        """
        ...

    def _trigger_redraw(self):
        """
        Triggers a redraw of all keys.
        """
        # TODO: Implement!


class SubMenu(Key):
    """
    A key that enters a submenu.
    """

    @staticmethod
    def pressed():
        # pylint: disable=missing-function-docstring
        return KeyPressResult.MENU_ENTER


class BackButton(Key):
    """
    A key that returns back from a submenu.
    """

    _title = "Back"
    _icon = "arrow-left"

    @staticmethod
    def pressed():
        # pylint: disable=missing-function-docstring
        return KeyPressResult.MENU_BACK
