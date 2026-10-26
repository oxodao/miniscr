from ctypes import CDLL

import gi

CDLL("libgtk4-layer-shell.so.0")

gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
gi.require_version('Gtk4LayerShell', '1.0')

if __name__ == "__main__":
    from app import main

    main()