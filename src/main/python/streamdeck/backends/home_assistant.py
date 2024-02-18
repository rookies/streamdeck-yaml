#!/usr/bin/python3
"""
HomeAssistant backend
"""
import ssl
import time
import json
import logging
from typing import Optional
import websocket

logger = logging.getLogger("streamdeck.backends.home_assistant")


class HomeAssistantBackend:
    # pylint: disable=too-many-instance-attributes
    """
    HomeAssistant backend
    """

    def __init__(self, url, token, insecure=False):
        self._url = url
        self._access_token = token
        self._insecure = insecure
        self._id = 1
        self._get_states_id = -1
        self._entity_states = {}
        self._handlers = {}

        self._connect()

    def _connect(self):
        self._ws = websocket.WebSocketApp(
            self._url,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
        )

    def run(self):
        """
        Implements the backend main loop.
        """
        while True:
            if self._insecure:
                self._ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
            else:
                self._ws.run_forever()

            time.sleep(1)

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

    def register_state_change_handler(self, entity_id, callback):
        """
        Registers a handler that is called when the state of the entity with
        the given changes.
        """
        if entity_id not in self._handlers:
            self._handlers[entity_id] = []

        self._handlers[entity_id].append(callback)

        return (entity_id, len(self._handlers[entity_id]) - 1)

    def unregister_state_change_handler(self, key):
        """
        Unregisters the handler with the given key, which was returned when
        creating the handler.
        """
        self._handlers[key[0]].pop(key[1])

    def _on_message(self, _, message):
        """
        Handler for received WebSocket messages.
        """
        logger.debug("Received message: %s", message)

        data = json.loads(message)
        msg_type = data.get("type", "")

        if msg_type == "auth_required":
            # Authentication required, send access token:
            self._send({"type": "auth", "access_token": self._access_token})
        elif msg_type == "auth_ok":
            # Authentication succeeded, subscribe to events and get initial states:
            self._send_with_id({"type": "subscribe_events"})
            self._get_states_id = self._send_with_id({"type": "get_states"})
        elif msg_type == "result":
            # TODO: What if data["success"] is False?
            if data["id"] == self._get_states_id:
                # Initial states received, store them:
                for entity in data["result"]:
                    self._entity_states[entity["entity_id"]] = entity["state"]
                    self._call_handlers(entity["entity_id"])
        elif msg_type == "event":
            if data["event"]["event_type"] == "state_changed":
                # State change received, update entity states:
                self._entity_states[data["event"]["data"]["entity_id"]] = data["event"][
                    "data"
                ]["new_state"]["state"]
                self._call_handlers(data["event"]["data"]["entity_id"])
        else:
            logger.warning("Unknown message: %s", message)

    def _call_handlers(self, entity_id):
        """
        Calls all registered state change handlers for the entity with
        the given ID.
        """
        for handler in self._handlers.get(entity_id, []):
            handler(entity_id, self._entity_states[entity_id])

    @staticmethod
    def _on_error(_, error):
        """
        Handler for WebSocket errors.
        """
        logger.error("WebSocket error: %s", error)

    def _on_close(self, _, status_code, msg):
        """
        Handler that is called when the WebSocket connection is closed.
        """
        logger.info("WebSocket connection closed: %s %s", status_code, msg)
        self._connect()

    @staticmethod
    def _on_open(_):
        """
        Handler that is called when the WebSocket connection is opened.
        """
        logger.info("Websocket connection opened")

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
