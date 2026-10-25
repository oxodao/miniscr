from abc import ABC, abstractmethod
from datetime import datetime
from typing import ClassVar

from config import Config
from config import UploadDestination as UploadDestinationConfig
from utils import UploadResult, send_notification
from wm import WM


class Destination(ABC):
    _app_config: Config
    _wm: WM

    def __init__(self, app_config: Config, wm: WM):
        self._app_config = app_config
        self._wm = wm

    def _get_picture_format(self) -> str:
        return self._app_config.picture_format.lstrip('.').lower() or 'png'
    
    def _get_filename(self):
        return datetime.now().strftime(self._app_config.filename_format) + f'.{self._get_picture_format()}'

    def action(self, picture: bytes) -> bytes | None:
        """
        Do the action required.
        If the action is a final step (most of the time), this should return None
        If the action should re-open the menu with the modified picture it should return the new picture
        This is useful for the picture editor for example
        """
        raise NotImplementedError


class UploadDestination(Destination):
    _name: str = "base"
    _args: ClassVar[dict[str, str]] = {}

    def __init__(self, app_config: Config, wm: WM, config: UploadDestinationConfig):
        super().__init__(app_config, wm)

        self._name = config.name
        self._args = config.args

    def get_args_value(self, key: str) -> str:
        return self._app_config.get_secret(self._args, key) or ''
    
    @classmethod
    @abstractmethod
    def is_current_destination(cls, config: UploadDestinationConfig) -> bool:
        raise NotImplementedError

    @abstractmethod
    def do_upload(self, picture: bytes) -> UploadResult:
        """ Do the upload and return the URL """
        raise NotImplementedError

    def action(self, picture) -> bytes|None:
        try:
            result = self.do_upload(picture)

            self._wm.set_clipboard_text(result.get('full_url'))

            send_notification(
                title=f'Screenshot uploaded to {self._name}',
                description=f'Link copied to the clipboard: {result.get('full_url')}'
            )
        except Exception as e:
            send_notification('Screenshot upload failure', f'{e}')

        return None
