#!/usr/bin/python3
"""
Gtk frontend, useful for development purposes
"""
import gi
from PIL import Image
from frontends import Frontend

gi.require_version("Gtk", "3.0")
gi.require_version("GdkPixbuf", "2.0")
from gi.repository import Gtk, GdkPixbuf, GLib  # pylint: disable=wrong-import-position


class GtkFrontend(Frontend):
    """
    Gtk frontend, useful for development purposes
    """

    image_size = (80, 80)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initialize window:
        self._window = Gtk.Window()
        self._window.connect("destroy", Gtk.main_quit)

        # Initialize grid:
        self._grid = Gtk.Grid()
        self._grid.set_row_homogeneous(True)
        self._grid.set_column_homogeneous(True)
        self._window.add(self._grid)

        # Initialize buttons:
        self._buttons = []
        for row in range(self._layout[0]):
            for col in range(self._layout[1]):
                button = Gtk.Button()

                key_index = row * self._layout[1] + col
                button.connect("clicked", self._keypress, key_index)

                self._buttons.append(button)
                self._grid.attach(button, col, row, 1, 1)

        # Initialize regular timer:
        GLib.timeout_add(1000, self._timer_callback)

    def clear(self):
        # pylint: disable=missing-function-docstring
        for button in self._buttons:
            button.set_label("")
            button.set_image(None)

    def draw(self):
        # pylint: disable=missing-function-docstring
        self._window.show_all()

    @staticmethod
    def run():
        # pylint: disable=missing-function-docstring
        Gtk.main()

    def set_key(self, key_index: int, image: Image):
        # pylint: disable=missing-function-docstring
        # See https://gist.github.com/mozbugbox/10cd35b2872628246140
        pixbuf = GdkPixbuf.Pixbuf.new_from_bytes(
            GLib.Bytes.new(image.tobytes()),
            GdkPixbuf.Colorspace.RGB,
            False,
            8,
            image.size[0],
            image.size[1],
            image.size[0] * 3,
        ).copy()
        gtk_image = Gtk.Image.new_from_pixbuf(pixbuf)
        self._buttons[key_index].set_image(gtk_image)
        self._buttons[key_index].set_always_show_image(True)

    def disable(self):
        # pylint: disable=missing-function-docstring
        self.clear()
        super().disable()

    def _keypress(self, _, key_index):
        """
        Callback function for key presses.
        """
        self._update_last_action()
        self._callback(key_index)
