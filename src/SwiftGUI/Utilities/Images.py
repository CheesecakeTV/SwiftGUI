import base64
import io
from os import PathLike
from typing import IO

from PIL import Image as PIL_Image

from PIL import ImageTk


def file_to_b64(file: PathLike | str) -> bytes:
    file = open(file, "rb")
    file = base64.b64encode(file.read())
    return file

def file_from_b64(b64_data: str | bytes) -> io.BytesIO:
    file = base64.b64decode(b64_data)
    file = io.BytesIO(file)
    return file

def image_to_tk_image(
        image: str | PathLike | PIL_Image.Image | IO[bytes],
        width: int = None,
        height: int = None,
) -> ImageTk.PhotoImage | None:
    if image is None:
        return

    # if isinstance(image, str) or isinstance(image, PathLike) or isinstance(image, IO) or isinstance(image, bytes):

    if not isinstance(image, PIL_Image.Image):
        image = PIL_Image.open(image)
    #self._image = image

    if width is not None and height is not None:
        image = image.resize((width, height))
    elif width is not None:
        factor = width / image.size[0]
        height = int(image.size[1] * factor)
        image = image.resize((width, height))
    elif height is not None:
        factor = height / image.size[1]
        width = int(image.size[0] * factor)
        image = image.resize((width, height))

    if isinstance(image, PIL_Image.Image):
        image = ImageTk.PhotoImage(image)

    assert isinstance(image, ImageTk.PhotoImage), "An image you supplied has a non-supported type."
    return image
