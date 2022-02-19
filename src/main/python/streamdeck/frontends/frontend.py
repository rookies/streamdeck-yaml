#!/usr/bin/python3
"""
Abstract base class for all frontends.
"""
from abc import ABC, abstractmethod


class Frontend(ABC):
    """
    Abstract base class for all frontends.
    """

    @abstractmethod
    def clear(self):
        """
        Clears all keys without actually updating them.
        """
        ...

    @abstractmethod
    def draw(self):
        """
        Updates the keys with the current configuration set via clear() and
        set_key().
        """
        ...

    @abstractmethod
    def run(self):
        """
        Implements the frontend main loop.
        """
        ...

    @abstractmethod
    def set_key(self, key_index: int, title: str, image_path: str):
        """
        Sets the content of the key with the given index.
        """
        ...
