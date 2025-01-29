#!/usr/bin/python
"""
Contains some generic key classes.
"""
from keys.base import KeyBase, KeyPressResult


class SubMenuKey(KeyBase):
    # pylint: disable=too-few-public-methods
    """
    A key that enters a submenu.
    """

    def pressed(self):
        # pylint: disable=missing-function-docstring
        return KeyPressResult.MENU_ENTER, self._values["keys"]


class BackKey(KeyBase):
    # pylint: disable=too-few-public-methods
    """
    A key that returns back from a submenu.
    """

    _title = "Back"
    _icon = "arrow-left"

    def pressed(self):
        # pylint: disable=missing-function-docstring
        return KeyPressResult.MENU_BACK, None
