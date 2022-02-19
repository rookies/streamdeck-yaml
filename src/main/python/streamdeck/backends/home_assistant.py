#!/usr/bin/python3
"""
HomeAssistant backend
"""
import ssl
import json
from typing import Optional
import websocket


class HomeAssistantBackend:
    """
    HomeAssistant backend
    """

    def __init__(self, url, token, insecure=False):
        self._ws = websocket.WebSocketApp(
            url,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
        )
        self._access_token = token
        self._insecure = insecure
        self._id = 1
        self._get_states_id = -1
        self._entity_states = {}
        # TODO: Implement reconnect

    def run(self):
        """
        Implements the backend main loop.
        """
        if self._insecure:
            self._ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        else:
            self._ws.run_forever()

    def call_service(
        self,
        domain: str,
        service: str,
        data: Optional[dict] = None,
        target: Optional[dict] = None,
    ):
        """
        Calls a HomeAssistant service.

        :param domain: domain of the service to call
        :param service: name of the service to call
        :param data: data for the service
        :param target: target for the service
        """
        if data is None:
            data = {}
        if target is None:
            target = {}

        self._send_with_id(
            {
                "type": "call_service",
                "domain": domain,
                "service": service,
                "service_data": data,
                "target": target,
            }
        )

    def get_entity_state(self, entity_id):
        """
        Returns the state of the entity with the given ID or None if unknown.
        """
        return self._entity_states.get(entity_id)

    def _on_message(self, _, message):
        """
        Handler for received WebSocket messages.
        """
        print("+++ MESSAGE +++")
        print(message)

        data = json.loads(message)
        msg_type = data.get("type", "")

        if msg_type == "auth_required":
            # Authentication required, send access token:
            self._send({"type": "auth", "access_token": self._access_token})
        elif msg_type == "auth_ok":
            # Authentication succeeded, subscribe to events and get initial states:
            self._send_with_id({"type": "subscribe_events"})
            self._get_states_id = self._send_with_id({"type": "get_states"})
        elif msg_type == "result" and data["id"] == self._get_states_id:
            # Initial states received, store them:
            # TODO: What if data["success"] is False?
            for entity in data["result"]:
                self._entity_states[entity["entity_id"]] = entity["state"]
        elif msg_type == "event" and data["event"]["event_type"] == "state_changed":
            # State change received, update entity states:
            self._entity_states[data["event"]["data"]["entity_id"]] = data["event"][
                "data"
            ]["new_state"]["state"]

    @staticmethod
    def _on_error(_, error):
        """
        Handler for WebSocket errors.
        """
        print("+++ ERROR +++")
        print(error)

    @staticmethod
    def _on_close(_, status_code, msg):
        """
        Handler that is called when the WebSocket connection is closed.
        """
        print("+++ CLOSE +++")
        print(status_code, msg)

    @staticmethod
    def _on_open(_):
        """
        Handler that is called when the WebSocket connection is opened.
        """
        print("+++ OPEN +++")

    def _send(self, data):
        """
        Sends a given object as JSON via WebSocket.
        """
        self._ws.send(json.dumps(data))

    def _send_with_id(self, data):
        """
        Sends a given object as JSON via WebSocket, adding an incrementing ID.
        """
        data["id"] = self._id
        self._send(data)
        self._id += 1

        return self._id - 1
