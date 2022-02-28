#!/usr/bin/python3
"""
Main application entrypoint.
"""
import sys
import enum
import logging
import threading
import yaml
import typer
import frontends
import backends
import keys
from image import ImageRenderer

logger = logging.getLogger("streamdeck.main")
app = typer.Typer()


class LogLevel(str, enum.Enum):
    """
    Log level, used to check the corresponding command line parameter.
    """

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Main:
    """
    Main application entrypoint.
    """

    def __init__(self, layout_file: str, loglevel: str):
        logging.basicConfig(level=getattr(logging, loglevel))

        with open(layout_file, encoding="utf8") as file_handle:
            self.layout = yaml.safe_load(file_handle)

        self._submenu_stack = [self.layout["keys"]]
        self._keys = []

        # Load frontend:
        logger.info("Available frontends: %s", ", ".join(frontends.AVAILABLE))
        frontend_kind = self.layout["frontend"]["kind"]
        if frontend_kind not in frontends.AVAILABLE:
            logger.error("Unknown frontend: %s", frontend_kind)
            sys.exit(1)
        self._frontend = getattr(frontends, frontend_kind)(
            self.layout["frontend"]["rows"],
            self.layout["frontend"]["columns"],
            self._callback,
        )
        logger.info("Loaded frontend %s", frontend_kind)

        # Load backends:
        logger.info("Available backends: %s", ", ".join(backends.AVAILABLE))
        self._backends = {}
        for key, backend in self.layout["backends"].items():
            backend_kind = backend["kind"]
            if backend_kind not in backends.AVAILABLE:
                logger.error("Unknown backend: %s", backend_kind)
                sys.exit(1)
            self._backends[key] = getattr(backends, backend_kind)(**backend["values"])
            logger.info("Loaded backend %s as %s", backend_kind, key)

        # Print available keys:
        logger.info("Available keys: %s", ", ".join(keys.AVAILABLE))

        # Create image renderer:
        self._renderer = ImageRenderer(self._frontend.image_size, self.layout["style"])

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
        self._keys = []
        for row in range(self.layout["frontend"]["rows"]):
            for col in range(self.layout["frontend"]["columns"]):
                key_index = row * self.layout["frontend"]["columns"] + col

                if key_index >= len(self.submenu_layout):
                    break
                key_config = self.submenu_layout[key_index]
                if key_config is None:
                    self._keys.append(None)
                    continue

                # Create key object:
                key_kind = key_config["kind"]
                if key_kind not in keys.AVAILABLE:
                    logger.error("Unknown key: %s", key_kind)
                    sys.exit(1)
                key = getattr(keys, key_kind)(
                    key_config.get("values", {}),
                    self._backends.get(key_config.get("backend")),
                )
                logger.info("Loaded key %s at position (%d,%d)", key_kind, row, col)
                self._keys.append(key)

    def _draw(self):
        """
        Updates the layout at the frontend.
        """
        self._frontend.clear()
        for key_index, key in enumerate(self._keys):
            if key is not None:
                self._frontend.set_key(key_index, self._renderer.render(key))
        self._frontend.draw()

    def _callback(self, key_index):
        """
        This method is called by the frontend when a key is pressed.

        :param key_index: index of the key that was pressed
        """
        if key_index >= len(self.submenu_layout):
            logger.info("Key #%d pressed, but it has no mapping", key_index)
            return
        key_config = self.submenu_layout[key_index]
        if key_config is None:
            logger.info("Key #%d pressed, but its mapping is null", key_index)
            return

        key = self._keys[key_index]
        logger.info("Key #%d (%s) pressed, calling handler", key_index, type(key))
        result, details = key.pressed()
        logger.debug(
            "Keypress handler for key #%d (%s) returned %s",
            key_index,
            key_config,
            result,
        )
        if result == keys.KeyPressResult.MENU_ENTER:
            self._submenu_stack.append(details)
            logger.info("Entering submenu at level %d", len(self._submenu_stack) - 1)
            self._create_keys()
            self._draw()
        elif result == keys.KeyPressResult.MENU_BACK:
            if len(self._submenu_stack) == 1:
                logger.warning("Sorry, there's no way back from here")
                return

            self._submenu_stack.pop()
            logger.info(
                "Going back to submenu at level %d", len(self._submenu_stack) - 1
            )
            self._create_keys()
            self._draw()
        elif result == keys.KeyPressResult.REDRAW:
            logger.info("Redrawing frontend")
            self._draw()

    @property
    def submenu_layout(self):
        """
        Returns the layout of the currently selected submenu.
        """
        return self._submenu_stack[-1]


@app.command()
def main(
    layout: str = typer.Argument(..., help="path to the layout YAML file"),
    loglevel: LogLevel = typer.Option("INFO", help="loglevel to use"),
):
    """
    Wrapper around the main class, used for typer.
    """
    instance = Main(layout, loglevel)
    instance.run()


if __name__ == "__main__":
    app()
