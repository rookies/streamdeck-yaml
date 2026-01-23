#!/usr/bin/python3
"""
This module contains all available frontend implementations. A frontend displays the
keys and informs the main application when a key is pressed.
"""

from frontends.frontend import Frontend
from frontends.gtk import GtkFrontend
from frontends.elgato import ElgatoFrontend

AVAILABLE = ["GtkFrontend", "ElgatoFrontend"]
