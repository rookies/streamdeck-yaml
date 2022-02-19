#!/usr/bin/python3
from abc import ABC, abstractmethod


class Frontend(ABC):
    @abstractmethod
    def clear(self):
        ...

    @abstractmethod
    def draw(self):
        ...

    @abstractmethod
    def run(self):
        ...

    @abstractmethod
    def set_key(self, key_index: int, title: str, image_path: str):
        ...
