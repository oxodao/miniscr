from typing import TypedDict


class Point(TypedDict):
    x: float
    y: float


class Region(TypedDict):
    x: float
    y: float
    width: float
    height: float

class UploadResult(TypedDict):
    full_url: str
    thumb_url: str | None