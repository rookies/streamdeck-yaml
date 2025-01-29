#!/usr/bin/python3
"""
This module contains all available key implementations.
"""
import pkgutil
import inspect
import importlib
from keys.base import KeyBase, KeyPressResult

AVAILABLE = []
for _, module_name, _ in pkgutil.iter_modules(__path__):
    module = importlib.import_module(f"{__name__}.{module_name}")
    for class_name, class_obj in inspect.getmembers(module, inspect.isclass):
        if class_name.endswith("Key"):
            AVAILABLE.append(class_name)
            locals()[class_name] = class_obj
