import io
import tkinter as tk
from os import PathLike
from typing import Any, Self, IO
from PIL import Image as PIL_Image
from PIL import ImageTk

from SwiftGUI import GlobalOptions, BaseWidget, ElementFlag


class Image(BaseWidget):
    _tk_widget_class = tk.Label
    tk_widget: tk.Label

    defaults = GlobalOptions.Image

    def __init__(
            self,
            image: str | PathLike | PIL_Image.Image | io.BytesIO = None,
            /,
            key: Any = None,
            height: int = None,
            width: int = None,
            tk_kwargs: dict = None,
    ):
        super().__init__(key= key, tk_kwargs= tk_kwargs)

        self._height = None
        self._width = None

        self.update(
            image = image,
            height = height,
            width = width,
        )

    def _update_special_key(self,key:str,new_val:any) -> bool|None:
        match key:
            case "image":
                self._image = new_val
                self.add_flags(ElementFlag.UPDATE_IMAGE)
            case "height":
                self._height = new_val
                self.add_flags(ElementFlag.UPDATE_IMAGE)
            case "width":
                self._width = new_val
                self.add_flags(ElementFlag.UPDATE_IMAGE)
            case _:
                return False

        return True

    _image: Any | PIL_Image.Image = None
    _photo_image: ImageTk.PhotoImage = None

    @BaseWidget._run_after_window_creation
    def _set_image(self, image: str | PathLike | PIL_Image.Image | io.BytesIO) -> Self:
        """
        Changes/sets/updates the image of the tk-element.

        :param image:
        :return:
        """
        if image is None:
            return self

        #if isinstance(image, str) or isinstance(image, PathLike) or isinstance(image, IO) or isinstance(image, bytes):

        if not isinstance(image, PIL_Image.Image):
            image = PIL_Image.open(image)
        self._image = image

        if self._width is not None and self._height is not None:
            image = image.resize((self._width, self._height))
        elif self._width is not None:
            factor = self._width / image.size[0]
            height = int(image.size[1] * factor)
            image = image.resize((self._width, height))
        elif self._height is not None:
            factor = self._height / image.size[1]
            width = int(image.size[0] * factor)
            image = image.resize((width, self._height))

        if isinstance(image, PIL_Image.Image):
            image = ImageTk.PhotoImage(image)

        assert isinstance(image, ImageTk.PhotoImage), "Whatever you supplied to .update(image= ...) of the sg.Image can't be used (Wrong type)."
        self._photo_image = image
        self.tk_widget.configure(image = self._photo_image)

        return self

    def _apply_update(self):
        super()._apply_update()

        if self.has_flag(ElementFlag.UPDATE_IMAGE):
            self.remove_flags(ElementFlag.UPDATE_IMAGE)
            self._set_image(self._image)

    def _get_value(self) -> Any:
        return None

    def set_value(self,val: Any):
        raise TypeError("sg.Image doesn't allow changing of its 'value'")

