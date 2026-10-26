# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 Oxodao

import os

from ..utils import Insets, Point, Region, exec_command_json, exec_region_command
from .wm import Wayland


class Hyprland(Wayland):
    @staticmethod
    def is_current_wm() -> bool:
        env_var = os.environ.get("HYPRLAND_INSTANCE_SIGNATURE")

        return env_var is not None

    def get_cursor_position(self) -> Point | None:
        """Get the current cursor position."""
        output = exec_region_command('hyprctl -j cursorpos')

        if not output:
            return None

        return {"x": output["x"], "y": output["y"]}

    def get_reserved_area(self, monitor_name: str) -> Insets | None:
        monitors = exec_command_json("hyprctl -j monitors")
        if not isinstance(monitors, list):
            return None

        for monitor in monitors:
            if monitor.get("name") != monitor_name:
                continue

            reserved = monitor.get("reserved")
            if not isinstance(reserved, list) or len(reserved) != 4:
                return None

            return {
                "left": int(reserved[0]),
                "top": int(reserved[1]),
                "right": int(reserved[2]),
                "bottom": int(reserved[3]),
            }

        return None

    def wait_for_window(self) -> Region | None:
        """Ask the user to select a window and return its geometry"""
        clients = exec_command_json("hyprctl -j clients")
        if not clients:
            return None

        regions = [
            f"{x},{y} {w}x{h}"
            for client in clients
            if client.get("mapped") and not client.get("hidden")
            for (x, y), (w, h) in [(client["at"], client["size"])]
            if w > 0 and h > 0
        ]

        return exec_region_command(
            'slurp -r -f \'{"x":%x,"y":%y,"width":%w,"height":%h}\'',
            "\n".join(regions),
        )