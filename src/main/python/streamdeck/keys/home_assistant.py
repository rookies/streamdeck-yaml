#!/usr/bin/python3
"""
Keys for integration with HomeAssistant.
"""
from keys.generic import Key, KeyPressResult


class HomeAssistantLight(Key):
    # pylint: disable=too-few-public-methods
    """
    A key that represents the state of a HomeAssistant light entity
    and can control it.
    """

    _icon = "lightbulb-question"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._handler_key = self._backend.register_state_change_handler(
            self._values["entity_id"], self._statechange
        )

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
            self._icon = "lightbulb-on"
        elif state == "on":
            self._backend.call_service(
                "light", "turn_off", target={"entity_id": self._values["entity_id"]}
            )
            self._icon = "lightbulb-off"
        else:
            print(f"Entity {self._values['entity_id']} is in unknown state")
            self._icon = "lightbulb-question"

        return KeyPressResult.REDRAW

    def _statechange(self, _, state):
        """
        Callback for entity state changes.
        """
        if state == "off":
            self._icon = "lightbulb-on"
        elif state == "on":
            self._icon = "lightbulb-off"
        else:
            self._icon = "lightbulb-question"

        self._trigger_redraw()


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
