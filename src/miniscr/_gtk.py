# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 Oxodao

from ctypes import CDLL

import gi

CDLL("libgtk4-layer-shell.so.0")

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Gtk4LayerShell", "1.0")
