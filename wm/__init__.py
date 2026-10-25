from .wm import WM, Wayland
from .hyprland import Hyprland
from .sway import Sway

supported_wms: list[type[WM]] = [
    Hyprland,
    Sway,
]

def get_current_wm() -> WM:
    for wm_class in supported_wms:
        if wm_class.is_current_wm():
            return wm_class()
    
    raise RuntimeError("No supported window manager detected.")

__all__ = [
    'supported_wms',
    "WM",
    'Wayland',
    # 'X11',
    'get_current_wm',
]