from config import Config
from config import UploadDestination as UploadDestinationConfig

from .copy_to_clipboard import CopyToClipboardDestination
from .destination import UploadDestination
from .imgbb import ImgbbDestination
from .save import SaveDestination
from .slink import SlinkDestination

upload_destinations = [SlinkDestination, ImgbbDestination]

def get_upload_destination(
    app_config: Config,
    wm,
    config: UploadDestinationConfig,
) -> UploadDestination:
    for destination_cls in upload_destinations:
        if destination_cls.is_current_destination(config):
            return destination_cls(app_config, wm, config)

    raise RuntimeError(f"No matching upload destination found for config: {config}")

__all__ = [
    'CopyToClipboardDestination',
    'SaveDestination',
    'UploadDestination',
    'get_upload_destination',
    'upload_destinations',
]