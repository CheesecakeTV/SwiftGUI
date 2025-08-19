import base64
import io
from os import PathLike


def file_to_b64(file: PathLike | str) -> bytes:
    file = open(file, "rb")
    file = base64.b64encode(file.read())
    return file

def file_from_b64(b64_data: str | bytes) -> io.BytesIO:
    file = base64.b64decode(b64_data)
    file = io.BytesIO(file)
    return file
