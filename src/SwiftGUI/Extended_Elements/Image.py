import tkinter as tk
from os import PathLike
from typing import Any, IO, Hashable
from SwiftGUI.Compat import Self
from PIL import Image as PIL_Image
from PIL import ImageTk

from SwiftGUI import GlobalOptions, BaseWidget, ElementFlag, Color, image_to_tk_image


class Image(BaseWidget):
    _tk_widget_class = tk.Label
    tk_widget: tk.Label

    _grab_anywhere_on_this = True

    defaults = GlobalOptions.Image

    _transfer_keys = {
        "background_color": "bg"
    }

    def __init__(
            self,
            image: str | PathLike | PIL_Image.Image | IO[bytes] = None,
            *,
            key: Hashable = None,
            image_height: int = None,
            image_width: int = None,
            background_color: str | Color = None,
            apply_parent_background_color:bool = None,
            tk_kwargs: dict = None,
            expand: bool = None,
            expand_y: bool = None,
    ):
        super().__init__(key= key, tk_kwargs= tk_kwargs, expand = expand, expand_y= expand_y)

        self._height = None
        self._width = None

        if background_color and not apply_parent_background_color:
            apply_parent_background_color = False

        self._update_initial(image=image, image_height=image_height, image_width=image_width,
                             apply_parent_background_color=apply_parent_background_color,
                             background_color=background_color)

    def _update_special_key(self,key:str,new_val:Any) -> bool|None:
        match key:
            case "image":
                self._image = new_val
                self.add_flags(ElementFlag.UPDATE_IMAGE)
            case "image_height":
                self._height = new_val
                self.add_flags(ElementFlag.UPDATE_IMAGE)
            case "image_width":
                self._width = new_val
                self.add_flags(ElementFlag.UPDATE_IMAGE)
            case "apply_parent_background_color":
                if new_val:
                    self.add_flags(ElementFlag.APPLY_PARENT_BACKGROUND_COLOR)
                else:
                    self.remove_flags(ElementFlag.APPLY_PARENT_BACKGROUND_COLOR)
            case _:
                return super()._update_special_key(key, new_val)

        return True

    _image: Any | PIL_Image.Image = None
    _photo_image: ImageTk.PhotoImage = None

    @BaseWidget._run_after_window_creation
    def _set_image(self, image: str | PathLike | PIL_Image.Image | IO[bytes]) -> Self:
        """
        Changes/sets/updates the image of the tk-element.

        :param image:
        :return:
        """
        temp = image_to_tk_image(image, self._width, self._height)
        if temp is not None:
            self._photo_image: Any | str = temp
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
        raise TypeError("sg.Image doesn't allow changing of its 'value'. Use .update(image= ...) instead.")

