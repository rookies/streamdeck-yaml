#!/usr/bin/python3
import sys
import os.path
import threading
import yaml
from GtkFrontend import GtkFrontend
from HomeAssistant import HomeAssistant


class Main:
    def __init__(self, argv):
        if len(argv) != 2:
            print(f"Usage: {argv[0]} layout.yml")
            sys.exit(1)

        with open(argv[1]) as f:
            self.layout = yaml.safe_load(f)

        self._submenu = []
        self._icon_path = os.path.join(os.path.dirname(__file__), "icons")
        # TODO: Don't hardcode frontend kind
        self._frontend = GtkFrontend(self.layout["rows"], self.layout["columns"], self._callback)

        self._backends = {}
        for key, backend in self.layout["backends"].items():
            # TODO: Don't hardcode backend kind
            self._backends[key] = HomeAssistant(**backend["values"])

    def run(self):
        # Start a thread for each backend:
        for key, backend in self._backends.items():
            threading.Thread(target=backend.run, name=key, daemon=True).start()

        # Update layout and run frontend main loop:
        self._update()
        self._frontend.run()

    def _update(self):
        submenu_layout = self.get_submenu_layout()

        self._frontend.clear()
        for row in range(self.layout["rows"]):
            for col in range(self.layout["columns"]):
                key_index = row * self.layout["columns"] + col

                if key_index >= len(submenu_layout):
                    break
                key_config = submenu_layout[key_index]
                if key_config is None:
                    continue

                self._frontend.set_key(key_index, key_config["title"], os.path.join(self._icon_path, f"{key_config['icon']}.png"))
        self._frontend.draw()

    def _callback(self, key_index):
        submenu_layout = self.get_submenu_layout()

        if key_index >= len(submenu_layout):
            return
        key_config = submenu_layout[key_index]
        if key_config is None:
            return

        if key_config["kind"] == "SubMenu":
            self._submenu.append(key_index)
            self._update()
        elif key_config["kind"] == "BackButton":
            self._submenu.pop()
            self._update()
        else:
            # TODO
            print(key_index, key_config)

    def get_submenu_layout(self):
        submenu_layout = self.layout["keys"]
        for i in self._submenu:
            submenu_layout = submenu_layout[i]["values"]["keys"]

        return submenu_layout


if __name__ == '__main__':
    Main(sys.argv).run()
