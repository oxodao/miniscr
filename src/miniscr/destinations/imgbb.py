# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 Oxodao

import requests

from ..config import UploadDestination as UploadDestinationConfig
from ..utils import UploadResult, get_picture_mimetype
from .destination import UploadDestination


class ImgbbDestination(UploadDestination):
    @classmethod
    def is_current_destination(cls, config: UploadDestinationConfig) -> bool:
        return config.type == "imgbb"

    def _get_expiration(self) -> int | None:
        expiration = self.get_args_value('expiration')
        if expiration is None or expiration == '':
            return None

        try:
            expiration = int(expiration)
        except (TypeError, ValueError):
            raise ValueError(
                f'Invalid expiration, expected a number of seconds, got: {expiration}'
            ) from None

        if not 60 <= expiration <= 15552000:
            raise ValueError('Invalid expiration, must be between 60 and 15552000')

        return expiration

    def do_upload(self, picture: bytes) -> UploadResult:
        api_key = self.get_args_value('api_key')
        hide_user_agent = self.get_args_value('hide_user_agent')

        data = {
            'key': api_key,
            'name': self._get_filename(),
        }

        expiration = self._get_expiration()
        if expiration is not None:
            data['expiration'] = f'{expiration}'

        headers = {}
        if hide_user_agent is not False:
            headers['User-Agent'] = 'MiniScr'

        response = requests.post(
            'https://api.imgbb.com/1/upload',
            headers=headers,
            files={'image': (self._get_filename(), picture, get_picture_mimetype(picture))},
            data=data,
            timeout=60,
        )

        response.raise_for_status()

        resp = response.json()
        if not resp.get('success') or 'data' not in resp:
            error = resp.get('error', {}).get('message') or 'Unknown imgbb error'

            raise RuntimeError(f'Imgbb upload failed: {error}')

        uploaded = resp.get('data')

        return {
            'full_url': uploaded.get('url'),
            'thumb_url': uploaded.get('thumb', {}).get('url'),
        }
