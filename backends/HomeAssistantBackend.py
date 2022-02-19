#!/usr/bin/python3
import ssl
import json
import websocket


class HomeAssistantBackend:
    def __init__(self, url, token, insecure=False):
        self._ws = websocket.WebSocketApp(url,
            on_open=self._on_open, on_message=self._on_message, on_error=self._on_error, on_close=self._on_close)
        self._access_token = token
        self._insecure = insecure

    def run(self):
        if self._insecure:
            self._ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        else:
            self._ws.run_forever()

    def _on_message(self, ws, message):
        print("+++ MESSAGE +++")
        print(message)

        data = json.loads(message)
        msg_type = data.get("type", "")

        if msg_type == "auth_required":
            self._send({"type": "auth", "access_token": self._access_token})
        elif msg_type == "auth_ok":
            self._send({"id": 1, "type": "subscribe_events"})

    def _on_error(self, ws, error):
        print("+++ ERROR +++")
        print(error)

    def _on_close(self, ws, status_code, msg):
        print("+++ CLOSE +++")
        print(status_code, msg)

    def _on_open(self, ws):
        print("+++ OPEN +++")

    def _send(self, data):
        self._ws.send(json.dumps(data))
