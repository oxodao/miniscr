# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 Oxodao

from utils import convert_picture_to_format, mimetypes, send_notification

from .destination import Destination


class CopyToClipboardDestination(Destination):
    def action(self, picture: bytes) -> bytes | None:
        picture_format = self._app_config.picture_format.lstrip('.').lower() or 'png'

        try:
            mime_type = mimetypes.get(picture_format, 'image/png')
            if not mime_type:
                raise Exception('Unkown file format')

            picture = convert_picture_to_format(picture, picture_format)
            self._wm.set_clipboard_image(picture, mime_type)

            send_notification(
                title='Screenshot copied',
                description='Image copied to clipboard.',
            )
        except Exception as e:
            send_notification(
                title='Screenshot copy failed',
                description=str(e),
            )

        return None