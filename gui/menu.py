from gi.repository import Gdk, GLib, Gtk, Gtk4LayerShell

from config import Config
from wm import WM

CSS = """
window.menu {
    background: transparent;
}

list.menu-list {
    background: #1d2028;
    border: 1px solid #404655;
    border-radius: 6px;
    padding: 4px;
}

list.menu-list row {
    background: transparent;
    border-radius: 4px;
    padding: 7px 12px;
    min-width: 150px;
}

list.menu-list row:hover,
list.menu-list row:selected {
    background: #394253;
}

list.menu-list label {
    color: #e7eaf0;
    font-size: 13px;
}
"""


class Menu:
    _app_config: Config
    _wm: WM

    _loop: GLib.MainLoop
    _window: Gtk.Window
    _action: str|None

    def __init__(self, config: Config, wm: WM):
        self._app_config = config
        self._wm = wm

        self._action = None

        self._loop = GLib.MainLoop()
        self._window = Gtk.Window(title="MiniScr")
        self._window.set_default_size(200, 150)
        self._window.add_css_class('menu')
        self._window.set_decorated(False)
        self._window.set_resizable(False)

        Gtk4LayerShell.init_for_window(self._window)
        Gtk4LayerShell.set_layer(self._window, Gtk4LayerShell.Layer.OVERLAY)
        Gtk4LayerShell.set_keyboard_mode(self._window, Gtk4LayerShell.KeyboardMode.EXCLUSIVE)
        Gtk4LayerShell.set_exclusive_zone(self._window, 0)

        self._install_css()
        self._build()

        self._window.connect('close-request', self._on_close)

    def _install_css(self):
        provider = Gtk.CssProvider()
        provider.load_from_data(CSS.encode())

        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

    def _build(self):
        self.listbox = Gtk.ListBox()
        self.listbox.add_css_class("menu-list")
        self.listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)

        for label, action in (
            ("Copy to clipboard", "copy"),
            ("Save as file", "save"),
            # ("Upload", "upload"),
            ("Cancel", "cancel"),
        ):
            row = Gtk.ListBoxRow()
            row.set_name(action)

            text = Gtk.Label(label=label, xalign=0)
            row.set_child(text)

            self.listbox.append(row)

        self.listbox.connect("row-activated", self._on_activate)
        self._window.set_child(self.listbox)

    def _on_activate(self, listbox, row):
        self._action = row.get_name()
        self._window.close()

    def _on_close(self, window):
        self._loop.quit()

        return False

    def run(self) -> str | None:
        self._window.present()
        self._loop.run()

        return self._action