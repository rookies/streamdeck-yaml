#!/usr/bin/python3
"""
Abstract base class for all frontends.
"""
from abc import ABC, abstractmethod
from PIL import Image


class Frontend(ABC):
    """
    Abstract base class for all frontends.
    """

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
