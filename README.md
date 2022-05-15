streamdeck-yaml
===============

[![lint](https://github.com/rookies/streamdeck-yaml/actions/workflows/lint.yml/badge.svg)](https://github.com/rookies/streamdeck-yaml/actions/workflows/lint.yml)

Cross-platform compatible UI for devices like the Elgato Stream Decks. With HomeAssistant
integration and configured using a YAML file.

![Example menu](https://raw.githubusercontent.com/rookies/mywebsite-blogposts/master/2022-05-14_streamdeck-yaml/05.jpg)

## Dependencies
* base requirements: numpy, Pillow, libusb-hidapi, [requirements.txt](requirements.txt)
* for the GTK frontend: PyGObject 3, Gtk 3, GdkPixbuf 2, GLib

## Icons
The icons used by the application and included in `src/main/resources/icons` are from the
[Material Design Icons](https://github.com/Templarian/MaterialDesign), see
[their license](https://github.com/Templarian/MaterialDesign/blob/master/LICENSE) for details.

## Alternatives
* [streamdeck-ui by timothycrosley](https://github.com/timothycrosley/streamdeck-ui/) — if you
  want to use a graphical interface to configure your deck
* [python-elgato-streamdeck by abcminiuser](https://github.com/abcminiuser/python-elgato-streamdeck)
  — if you want to code your own custom UI in Python, streamdeck-yaml also uses this library
