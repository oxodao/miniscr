# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 Oxodao

import requests

from config import UploadDestination as UploadDestinationConfig
from utils import UploadResult, get_picture_mimetype

from .destination import UploadDestination


class CatboxDestination(UploadDestination):
    @classmethod
    def is_current_destination(cls, config: UploadDestinationConfig) -> bool:
        return config.type == "catbox"

    def do_upload(self, picture: bytes) -> UploadResult:
        userhash = self.get_args_value('userhash')
        hide_user_agent = self.get_args_value('hide_user_agent')

        data = {
            'reqtype': 'fileupload',
        }

        if userhash:
            data['userhash'] = userhash

        headers = {}
        if hide_user_agent is not False:
            headers['User-Agent'] = 'MiniScr'

        response = requests.post(
            'https://catbox.moe/user/api.php',
            headers=headers,
            files={'fileToUpload': (self._get_filename(), picture, get_picture_mimetype(picture))},
            data=data,
            timeout=60,
        )

        response.raise_for_status()

        full_url = response.text.strip()
        if not full_url.startswith(('http://', 'https://')):
            raise RuntimeError(f'Catbox upload failed: {full_url}')

        return {
            'full_url': full_url,
            'thumb_url': None,
        }
