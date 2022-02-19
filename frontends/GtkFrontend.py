#!/usr/bin/python3
import gi
from frontends import Frontend

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class GtkFrontend(Frontend):
    def __init__(self, rows, columns, callback):
        self._layout = (rows, columns)
        self._callback = callback

        self._window = Gtk.Window()
        self._window.connect("destroy", Gtk.main_quit)

        self._grid = Gtk.Grid()
        self._grid.set_row_homogeneous(True)
        self._grid.set_column_homogeneous(True)
        self._window.add(self._grid)

        self._buttons = []
        for row in range(rows):
            for col in range(columns):
                button = Gtk.Button()

                key_index = row * self._layout[1] + col
                button.connect("clicked", self._keypress, key_index)

                self._buttons.append(button)
                self._grid.attach(button, col, row, 1, 1)

    def clear(self):
        for button in self._buttons:
            button.set_label("")
            button.set_image(None)

    def draw(self):
        self._window.show_all()

    def run(self):
        Gtk.main()

    def set_key(self, key_index, title, image_path):
        image = Gtk.Image.new_from_file(image_path)
        self._buttons[key_index].set_label(title)
        self._buttons[key_index].set_always_show_image(True)
        self._buttons[key_index].set_image_position(Gtk.PositionType.TOP)
        self._buttons[key_index].set_image(image)

    def _keypress(self, button, key_index):
        self._callback(key_index)
