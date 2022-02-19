#!/usr/bin/python3
"""
Main application entrypoint.
"""
import sys
import threading
import yaml
import frontends
import backends
import keys


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
        self._keys = []

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

        # Print available keys:
        print(f"Available keys: {', '.join(keys.AVAILABLE)}")

    def run(self):
        """
        Starts the application main loops.
        """
        # Start a thread for each backend:
        for key, backend in self._backends.items():
            threading.Thread(target=backend.run, name=key, daemon=True).start()

        # Create key objects, update layout and run frontend main loop:
        self._create_keys()
        self._draw()
        self._frontend.run()

    def _create_keys(self):
        """
        Creates the key objects.
        """
        submenu_layout = self.get_submenu_layout()

        self._keys = []
        for row in range(self.layout["frontend"]["rows"]):
            for col in range(self.layout["frontend"]["columns"]):
                key_index = row * self.layout["frontend"]["columns"] + col

                if key_index >= len(submenu_layout):
                    break
                key_config = submenu_layout[key_index]
                if key_config is None:
                    self._keys.append(None)
                    continue

                # Create key object:
                key_kind = key_config["kind"]
                if key_kind not in keys.AVAILABLE:
                    print(f"Unknown key {key_kind}")
                    sys.exit(1)
                key = getattr(keys, key_kind)(
                    key_config.get("values", {}),
                    self._backends.get(key_config.get("backend")),
                )
                print(f"Loaded key {key_kind} at position ({row},{col})")
                self._keys.append(key)

    def _draw(self):
        """
        Updates the layout at the frontend.
        """
        self._frontend.clear()
        for key_index, key in enumerate(self._keys):
            if key is not None:
                self._frontend.set_key(key_index, key.title, key.icon_path)
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

        key = self._keys[key_index]
        result = key.pressed()
        print(key_index, key_config, result)
        if result == keys.KeyPressResult.MENU_ENTER:
            self._submenu.append(key_index)
            self._create_keys()
            self._draw()
        elif result == keys.KeyPressResult.MENU_BACK:
            self._submenu.pop()
            self._create_keys()
            self._draw()
        elif result == keys.KeyPressResult.REDRAW:
            self._draw()

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
