#!/usr/bin/python3
"""
Keys for integration with HomeAssistant.
"""
import logging
from keys.generic import Key, KeyPressResult

logger = logging.getLogger("streamdeck.keys.home_assistant")


class HomeAssistantLight(Key):
    # pylint: disable=too-few-public-methods
    """
    A key that represents the state of a HomeAssistant light entity
    and can control it.
    """

    _icon_by_state = {
        "on": "lightbulb-on",
        "off": "lightbulb-off",
        "unknown": "lightbulb-question",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._handler_key = self._backend.register_state_change_handler(
            self._values["entity_id"], self._statechange
        )

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
                "light", "turn_on", target={"entity_id": self._values["entity_id"]}
            )
            self._set_icon("on")
        elif state == "on":
            self._backend.call_service(
                "light", "turn_off", target={"entity_id": self._values["entity_id"]}
            )
            self._set_icon("off")
        else:
            logger.warning(
                "Entity %s is in unknown state: %s", self._values["entity_id"], state
            )
            self._set_icon("unknown")

        return KeyPressResult.REDRAW

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
        else:
            self._icon = self._icon_by_state["unknown"]


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
