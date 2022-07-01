#!/usr/bin/python3
"""
Keys for integration with HomeAssistant.
"""
import logging
from keys.generic import Key, KeyPressResult

logger = logging.getLogger("streamdeck.keys.home_assistant")


class HomeAssistantToggle(Key):
    """
    A key that represents the state of a HomeAssistant entity that can be toggled.
    Currently, lights and switches are supported.
    """

    _icon_by_domain_and_state = {
        "light": {
            "on": "lightbulb-on",
            "off": "lightbulb-off",
            "unknown": "lightbulb-question",
        },
        "switch": {
            "on": "toggle-switch",
            "off": "toggle-switch-off",
            "unknown": "toggle-switch",
        },
    }

    _icon_color_by_domain_and_state = {
        "light": {
            "on": "#fdd835",
            "off": "black",
            "unknown": "black",
        },
        "switch": {
            "on": "#44739e",
            "off": "black",
            "unknown": "black",
        },
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._handler_key = self._backend.register_state_change_handler(
            self._values["entity_id"], self._statechange
        )

        self._domain = self._values["entity_id"].split(".")[0]
        if "icon" in self._values:
            self._icon_by_state = {
                "on": self._values["icon"],
                "off": self._values["icon"],
                "unknown": self._values["icon"],
            }
        else:
            self._icon_by_state = self._icon_by_domain_and_state[self._domain]
        self._icon_color_by_state = self._icon_color_by_domain_and_state[self._domain]

        state = self._backend.get_entity_state(self._values["entity_id"])
        self._set_icon(state)

    def __del__(self):
        self._backend.unregister_state_change_handler(self._handler_key)

        super().__del__()

    def pressed(self):
        # pylint: disable=missing-function-docstring
        state = self._backend.get_entity_state(self._values["entity_id"])

        if state == "off":
            self._backend.call_service(
                self._domain, "turn_on", target={"entity_id": self._values["entity_id"]}
            )
            self._set_icon("on")
        elif state == "on":
            self._backend.call_service(
                self._domain,
                "turn_off",
                target={"entity_id": self._values["entity_id"]},
            )
            self._set_icon("off")
        else:
            logger.warning(
                "Entity %s is in unknown state: %s", self._values["entity_id"], state
            )
            self._set_icon("unknown")

        return KeyPressResult.REDRAW, None

    def _statechange(self, _, state):
        """
        Callback for entity state changes.
        """
        self._set_icon(state)

        self._trigger_redraw()

    def _set_icon(self, state):
        """
        Sets the icon according to the given state.
        """
        if state in self._icon_by_state:
            self._icon = self._icon_by_state[state]
            self._icon_color = self._icon_color_by_state[state]
        else:
            self._icon = self._icon_by_state["unknown"]
            self._icon_color = self._icon_color_by_state["unknown"]


class HomeAssistantScript(Key):
    # pylint: disable=too-few-public-methods
    """
    A key that can trigger a HomeAssistant script.
    """

    def pressed(self):
        # pylint: disable=missing-function-docstring
        self._backend.call_service(
            "script", "turn_on", target={"entity_id": self._values["entity_id"]}
        )

        return None, None
