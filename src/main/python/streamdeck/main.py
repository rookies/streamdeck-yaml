#!/usr/bin/python3
"""
Main application entrypoint.
"""
import sys
import os.path
import threading
import yaml
import frontends
import backends


class Main:
    """
    Main application entrypoint.
    """

    def __init__(self, argv):
        if len(argv) != 2:
            print(f"Usage: {argv[0]} layout.yml")
            sys.exit(1)

        with open(argv[1], encoding="utf8") as file_handle:
            self.layout = yaml.safe_load(file_handle)

        self._submenu = []
        self._icon_path = os.path.join(
            os.path.dirname(__file__), "../../resources/icons"
        )

        # Load frontend:
        print(f"Available frontends: {', '.join(frontends.AVAILABLE)}")
        frontend_kind = self.layout["frontend"]["kind"]
        if frontend_kind not in frontends.AVAILABLE:
            print(f"Unknown frontend {frontend_kind}")
            sys.exit(1)
        self._frontend = getattr(frontends, frontend_kind)(
            self.layout["frontend"]["rows"],
            self.layout["frontend"]["columns"],
            self._callback,
        )
        print(f"Loaded frontend {frontend_kind}")

        # Load backends:
        print(f"Available backends: {', '.join(backends.AVAILABLE)}")
        self._backends = {}
        for key, backend in self.layout["backends"].items():
            backend_kind = backend["kind"]
            if backend_kind not in backends.AVAILABLE:
                print(f"Unknown backend {backend_kind}")
                sys.exit(1)
            self._backends[key] = getattr(backends, backend_kind)(**backend["values"])
            print(f"Loaded backend {backend_kind} as {key}")

    def run(self):
        """
        Starts the application main loops.
        """
        # Start a thread for each backend:
        for key, backend in self._backends.items():
            threading.Thread(target=backend.run, name=key, daemon=True).start()

        # Update layout and run frontend main loop:
        self._update()
        self._frontend.run()

    def _update(self):
        """
        Updates the layout at the frontend.
        """
        submenu_layout = self.get_submenu_layout()

        self._frontend.clear()
        for row in range(self.layout["frontend"]["rows"]):
            for col in range(self.layout["frontend"]["columns"]):
                key_index = row * self.layout["frontend"]["columns"] + col

                if key_index >= len(submenu_layout):
                    break
                key_config = submenu_layout[key_index]
                if key_config is None:
                    continue

                self._frontend.set_key(
                    key_index,
                    key_config["title"],
                    os.path.join(self._icon_path, f"{key_config['icon']}.png"),
                )
        self._frontend.draw()

    def _callback(self, key_index):
        """
        This method is called by the frontend when a key is pressed.

        :param key_index: index of the key that was pressed
        """
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
        """
        Returns the layout of the currently selected submenu.
        """
        submenu_layout = self.layout["keys"]
        for i in self._submenu:
            submenu_layout = submenu_layout[i]["values"]["keys"]

        return submenu_layout


if __name__ == "__main__":
    Main(sys.argv).run()
