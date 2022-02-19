#!/usr/bin/python3
"""
Keys for integration with HomeAssistant.
"""
from keys.generic import Key


class HomeAssistantLight(Key):
    # pylint: disable=too-few-public-methods
    """
    A key that represents the state of a HomeAssistant light entity
    and can control it.
    """

    @staticmethod
    def pressed():
        # pylint: disable=missing-function-docstring
        # TODO
        ...


class HomeAssistantScript(Key):
    # pylint: disable=too-few-public-methods
    """
    A key that can trigger a HomeAssistant script.
    """

    @staticmethod
    def pressed():
        # pylint: disable=missing-function-docstring
        # TODO
        ...
