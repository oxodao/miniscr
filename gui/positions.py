from utils import Insets, empty_insets

def clamp_position(x: int, y: int, width: int, height: int, screen_width: int, screen_height: int, reserved: Insets | None = None) -> tuple[int, int]:
    reserved = reserved if reserved is not None else empty_insets()

    min_x = reserved["left"]
    min_y = reserved["top"]

    max_x = max(min_x, screen_width - reserved["right"] - width)
    max_y = max(min_y, screen_height - reserved["bottom"] - height)

    return (
        max(min_x, min(x, max_x)),
        max(min_y, min(y, max_y)),
    )