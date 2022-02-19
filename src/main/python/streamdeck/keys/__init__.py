#!/usr/bin/python3
"""
This module contains all available key implementations.
"""
from keys.home_assistant import HomeAssistantToggle, HomeAssistantScript
from keys.generic import KeyPressResult, SubMenu, BackButton

AVAILABLE = ["SubMenu", "BackButton", "HomeAssistantToggle", "HomeAssistantScript"]
