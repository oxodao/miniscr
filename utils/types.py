# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 Oxodao

from typing import TypedDict


class Point(TypedDict):
    x: int
    y: int


class Region(TypedDict):
    x: int
    y: int
    width: int
    height: int


class UploadResult(TypedDict):
    full_url: str
    thumb_url: str | None


class Insets(TypedDict):
    left: int
    top: int
    right: int
    bottom: int

def empty_insets() -> Insets:
    return {
        'left': 0,
        'top': 0,
        'right': 0,
        'bottom': 0,
    }