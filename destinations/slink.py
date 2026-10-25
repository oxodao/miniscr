import requests

from config import UploadDestination as UploadDestinationConfig
from utils import UploadResult, get_picture_mimetype

from .destination import UploadDestination


class SlinkDestination(UploadDestination):
    @classmethod
    def is_current_destination(cls, config: UploadDestinationConfig) -> bool:
        return config.type == "slink"

    def do_upload(self, picture: bytes) -> UploadResult:
        base_url = self.get_args_value('base_url').rstrip('/')
        token = self.get_args_value('api_key')
        collection_id = self.get_args_value('collection_id')
        
        hide_user_agent = self.get_args_value('hide_user_agent')

        data = {}
        if len(collection_id) > 0:
            data["collectionIds[]"] = collection_id

        headers = {
            'Authorization': f'Bearer {token}',
            'Origin': base_url,
        }

        if hide_user_agent is not False:
            headers['User-Agent'] = 'MiniScr'
        
        response = requests.post(
            f"{base_url}/api/external/upload",
            headers=headers,
            files={'image': (self._get_filename(), picture, get_picture_mimetype(picture))},
            data=data,
            timeout=60,
        )

        response.raise_for_status()

        return {
            'full_url': f'{base_url}/{response.json()["url"]}',
            'thumb_url': None,
        }