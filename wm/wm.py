import subprocess
from abc import ABC, abstractmethod

from utils import Point, Region, exec_region_command


class WM(ABC):
    @abstractmethod
    def get_cursor_position(self) -> Point | None:
        """Get the current cursor position."""
        raise NotImplementedError

    @abstractmethod
    def wait_for_region(self) -> Region | None:
        """Ask the user to select a region and return its geometry"""
        raise NotImplementedError

    @abstractmethod
    def wait_for_window(self) -> Region | None:
        """Wait for a window to be selected and return its geometry"""
        raise NotImplementedError

    @abstractmethod
    def wait_for_monitor(self) -> Region | None:
        """Wait for a monitor to be selected and return its geometry"""
        raise NotImplementedError

    @abstractmethod
    def take_screenshot(self, region: Region | None = None) -> bytes | None:
        """Take a screenshot of the specified region or the entire screen if no region is provided."""
        raise NotImplementedError

    @abstractmethod
    def set_clipboard_image(self, image: bytes, mime_type: str) -> None:
        """ Set the clipboard to the taken image """
        raise NotImplementedError

    @abstractmethod
    def set_clipboard_text(self, text: str) -> None:
        """ Set the clipboard to the url of the uploaded image """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def is_current_wm() -> bool:
        raise NotImplementedError


class Wayland(WM):
    def wait_for_region(self) -> Region | None:
        """Ask the user to select a region and return its geometry"""
        result: Region | None = exec_region_command('slurp -f \'{"x":%x,"y":%y,"width":%w,"height":%h}\'')
        if not result:
            return None

        return result

    @abstractmethod
    def wait_for_window(self) -> Region | None:
        """Wait for a window to be selected and return its geometry"""
        raise NotImplementedError

    def wait_for_monitor(self) -> Region | None:
        return exec_region_command(
            'slurp -o -r -f \'{"x":%x,"y":%y,"width":%w,"height":%h}\''
        )

    def take_screenshot(self, region: Region | None = None) -> bytes | None:
        cmd = ['grim']

        if region:
            cmd.extend([
                '-g',
                f'{region["x"]},{region["y"]} {region["width"]}x{region["height"]}',
            ])

        cmd.append('-')

        result = subprocess.run(
            cmd,
            capture_output=True,
            check=True,
        )

        return result.stdout

    def set_clipboard_image(self, image: bytes, mime_type: str) -> None:
        subprocess.run(
            ['wl-copy', '--type', mime_type],
            input=image,
            check=True,
        )

    def set_clipboard_text(self, text: str) -> None:
        subprocess.run(
            ['wl-copy', '--type', 'text/plain;charset=utf-8'],
            input=text.encode('utf-8'),
            check=True,
        )