# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 Oxodao

from pathlib import Path

from ..utils import convert_picture_to_format, send_notification
from .destination import Destination


class SaveDestination(Destination):
    def action(self, picture: bytes) -> bytes | None:
        save_directory = Path(self._app_config.save_directory).expanduser()
        save_directory.mkdir(parents=True, exist_ok=True)

        try:
            picture = convert_picture_to_format(
                picture,
                self._get_picture_format(),
            )

            filename = self._get_filename()
            file_path = save_directory / filename

            if file_path.exists():
                raise Exception(f'This filename already exists: {filename}')

            file_path.write_bytes(picture)

            send_notification(
                title="Screenshot saved",
                description=f"Screenshot was saved in {file_path}",
            )
        except Exception as e:
            send_notification(
                title='Screenshot failure',
                description=f'{e}',
            )


        return None