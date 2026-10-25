from io import BytesIO

from PIL import Image

formats_mapping = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
    "webp": "WEBP",
}

mimetypes = {
    'png': 'image/png',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'webp': 'image/webp',
}

def convert_picture_to_format(picture: bytes, target_format: str) -> bytes:
    if target_format not in formats_mapping:
        raise RuntimeError('The selected format is invalid.')

    # We check if the input format is the correct one, otherwise we convert it
    image = Image.open(BytesIO(picture))
    if image.format is None or image.format.upper() != formats_mapping[target_format.lower()]:
        buffer = BytesIO()
        image.save(buffer, quality=95, format=formats_mapping[target_format.lower()])
        picture = buffer.getvalue()

    return picture

def get_picture_mimetype(picture: bytes) -> str:
    image = Image.open(BytesIO(picture))
    if image.format is None:
        raise Exception('No format for this picture')

    if image.format.lower() not in mimetypes:
        raise Exception(f'Unknown mimetype for format {image.format.lower()}')

    return mimetypes[image.format.lower()]