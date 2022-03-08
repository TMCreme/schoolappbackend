import base64
from django.core.files.base import ContentFile



def base64_to_file(data, name=None):
    idx = data[:100].find(',')
    _format, file_str = data.split(";base64,")
    _name, ext = _format.split("/")
    if not name:
        name = _name.split(":")[-1]
    return ContentFile(base64.b64decode(file_str), name="{}.{}".format(name, ext))









