# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 Oxodao

import os

from utils import Insets, Point, Region, exec_command_json, exec_region_command

from .wm import Wayland


class Sway(Wayland):
    @staticmethod
    def is_current_wm() -> bool:
        env_var = os.environ.get("SWAYSOCK")

        return env_var is not None

    # Requires https://github.com/wlrfx/swayfx/pull/619
    def get_cursor_position(self) -> Point | None:
        """Get the current cursor position."""
        seats = exec_command_json("swaymsg -t get_seats -r")
        if not seats:
            return None

        for seat in seats:
            position = seat.get("cursor_position")
            if position is not None:
                return {"x": position["x"], "y": position["y"]}

        return None

    def get_reserved_area(self, monitor_name: str) -> Insets | None:
        outputs = exec_command_json("swaymsg -t get_outputs -r")
        workspaces = exec_command_json("swaymsg -t get_workspaces -r")

        if not isinstance(outputs, list) or not isinstance(workspaces, list):
            return None

        output = next(
            (o for o in outputs if o.get("name") == monitor_name),
            None,
        )

        workspace = next(
            (w for w in workspaces
            if w.get("output") == monitor_name and w.get("visible")),
            None,
        )

        if output is None or workspace is None:
            return None

        screen = output.get("rect")
        usable = workspace.get("rect")

        if screen is None or usable is None:
            return None

        return {
            "left": usable["x"] - screen["x"],
            "top": usable["y"] - screen["y"],
            "right": screen["x"] + screen["width"] - usable["x"] - usable["width"],
            "bottom": screen["y"] + screen["height"] - usable["y"] - usable["height"],
        }

    def _get_windows(self, node: dict):
        if node.get("pid") is not None and node.get("visible"):
            yield node

        for child in node.get("nodes", []) + node.get("floating_nodes", []):
            yield from self._get_windows(child)

    def wait_for_window(self) -> Region | None:
        tree = exec_command_json("swaymsg -t get_tree")
        if not tree:
            return None

        regions = []
        for window in self._get_windows(tree):
            rect = window["rect"]
            content = window["window_rect"]

            x = rect["x"] + content["x"]
            y = rect["y"] + content["y"]
            w = content["width"]
            h = content["height"]

            if w > 0 and h > 0:
                regions.append(f"{x},{y} {w}x{h}")

        if not regions:
            return None

        return exec_region_command(
            'slurp -r -f \'{"x":%x,"y":%y,"width":%w,"height":%h}\'',
            "\n".join(regions),
        )