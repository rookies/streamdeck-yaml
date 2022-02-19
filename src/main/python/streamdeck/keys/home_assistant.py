#!/usr/bin/python3
"""
Keys for integration with HomeAssistant.
"""
from keys.generic import Key


class HomeAssistantLight(Key):
    # pylint: disable=too-few-public-methods
    """
    A key that represents the state of a HomeAssistant light entity
    and can control it.
    """

    def pressed(self):
        # pylint: disable=missing-function-docstring
        state = self._backend.get_entity_state(self._values["entity_id"])

        if state == "off":
            self._backend.call_service(
                "light", "turn_on", target={"entity_id": self._values["entity_id"]}
            )
        elif state == "on":
            self._backend.call_service(
                "light", "turn_off", target={"entity_id": self._values["entity_id"]}
            )
        else:
            print(f"Entity {self._values['entity_id']} is in unknown state")


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
