#!/usr/bin/python3
"""
HomeAssistant backend
"""
import ssl
import json
import websocket


class HomeAssistantBackend:
    # pylint: disable=too-few-public-methods
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
        # TODO: Implement reconnect

    def run(self):
        """
        Implements the backend main loop.
        """
        if self._insecure:
            self._ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        else:
            self._ws.run_forever()

    def _on_message(self, _, message):
        """
        Handler for received WebSocket messages.
        """
        print("+++ MESSAGE +++")
        print(message)

        data = json.loads(message)
        msg_type = data.get("type", "")

        if msg_type == "auth_required":
            self._send({"type": "auth", "access_token": self._access_token})
        elif msg_type == "auth_ok":
            self._send({"id": 1, "type": "subscribe_events"})

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
