from config import Config, UploadDestination as UploadDestinationConfig
from .destination import UploadDestination
from .save import SaveDestination
from .copy_to_clipboard import CopyToClipboardDestination
from .slink import SlinkDestination
from .imgbb import ImgbbDestination

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
    'upload_destinations',
    'UploadDestination',
    'SaveDestination',
    'CopyToClipboardDestination',
    'get_upload_destination',
]