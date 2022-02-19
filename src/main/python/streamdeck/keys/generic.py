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
    """

    MENU_ENTER = 1
    MENU_BACK = 2


class Key(ABC):
    """
    Abstract base class for key classes.
    """

    def __init__(self, key_config):
        self._config = key_config

    @property
    def title(self):
        """
        Returns the title for the key.
        """
        return self._config["title"]

    @property
    def icon_path(self):
        """
        Returns the path to the icon for the key.
        """
        return os.path.join(ICON_PATH, f"{self._config['icon']}.png")

    @abstractmethod
    def pressed(self) -> KeyPressResult:
        """
        This method is called when the key is pressed.
        """
        ...


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

    @staticmethod
    def pressed():
        # pylint: disable=missing-function-docstring
        return KeyPressResult.MENU_BACK
