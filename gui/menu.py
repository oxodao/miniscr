# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 Oxodao

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
        self._window.add_css_class('menu')
        self._window.set_decorated(False)
        self._window.set_resizable(False)

        Gtk4LayerShell.init_for_window(self._window)
        Gtk4LayerShell.set_layer(self._window, Gtk4LayerShell.Layer.OVERLAY)
        Gtk4LayerShell.set_keyboard_mode(self._window, Gtk4LayerShell.KeyboardMode.EXCLUSIVE)
        Gtk4LayerShell.set_exclusive_zone(self._window, 0)

        self._install_css()
        self._build()

        key_controller = Gtk.EventControllerKey()
        key_controller.connect("key-pressed", self._on_key_pressed)
        self._window.add_controller(key_controller)

        self._window.connect('close-request', self._on_close)

    def _install_css(self):
        provider = Gtk.CssProvider()
        provider.load_from_data(CSS.encode())

        monitor = Gdk.Display.get_default()
        if not monitor:
            raise Exception('No monitor found!')

        Gtk.StyleContext.add_provider_for_display(
            display=monitor,
            provider=provider,
            priority=Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

    def _build(self):
        self.listbox = Gtk.ListBox()
        self.listbox.add_css_class("menu-list")
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.listbox.connect("row-activated", self._on_activate)

        self._window.set_child(self.listbox)
        self._show_main_menu()

    def _set_actions(self, actions: list[tuple[str, str]]):
        while row := self.listbox.get_first_child():
            self.listbox.remove(row)

        for label, action in actions:
            row = Gtk.ListBoxRow()
            row.set_name(action)
            row.set_child(Gtk.Label(label=label, xalign=0))
            self.listbox.append(row)

        self._window.queue_resize()

    def _show_main_menu(self):
        actions = [
            ("Copy to clipboard", "copy"),
            ("Save as file", "save"),
        ]

        destinations = self._app_config.upload_destination

        if destinations:
            actions.append(
                (f"Upload to {destinations[0].name}", "upload_0")
            )

        if len(destinations) > 1:
            actions.append(("Other uploads ›", "other_uploads"))

        actions.append(("Cancel", "cancel"))
        self._set_actions(actions)


    def _show_upload_menu(self):
        actions = [
            (f"Upload to {dest.name}", f"upload_{index}")
            for index, dest in enumerate(
                self._app_config.upload_destination[1:], start=1
            )
        ]

        actions.append(("‹ Back", "back"))
        self._set_actions(actions)

    def _on_activate(self, listbox, row):
        action = row.get_name()

        if action == "other_uploads":
            self._show_upload_menu()

            return

        if action == "back":
            self._show_main_menu()

            return

        self._action = action
        self._window.close()

    def _on_key_pressed(self, controller, keyval, keycode, state) -> bool:
        key = Gdk.keyval_name(keyval)
        if not key:
            return False

        actions = {
            "Escape": "cancel",
            "s": "save",
            "c": "copy",
            "u": "upload_0",
        }

        action = actions.get(key)

        if action is None:
            return False

        if action == "upload_0" and not self._app_config.upload_destination:
            return False

        self._action = action
        self._window.close()

        return True

    def _on_close(self, window):
        self._loop.quit()

        return False

    def run(self) -> str | None:
        self._window.present()
        self._loop.run()

        return self._action