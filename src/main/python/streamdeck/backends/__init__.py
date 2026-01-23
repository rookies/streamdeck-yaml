#!/usr/bin/python3
"""
This module contains all available backend implementations. A backend communicates
with the actual objects that are displayed on and controlled with the Streamdeck,
e.g. HomeAssistant entitities.
"""

from backends.home_assistant import HomeAssistantBackend

AVAILABLE = ["HomeAssistantBackend"]
