from os import PathLike
from typing import Hashable, IO, Any
from PIL import Image as PIL_Image

import SwiftGUI as sg
from SwiftGUI import Canvas_Elements
from SwiftGUI.Compat import Self
from SwiftGUI.Utilities.Images import image_to_tk_image


class Image(Canvas_Elements.BaseCanvasElement):
    defaults = sg.GlobalOptions.Canvas_Image

    _create_method = "create_image"

    _transfer_keys = {
        "image_active": "activeimage",
        "image_disabled": "disabledimage",
    }

    def __init__(
            self,
            position: tuple[float, float],
            image: PathLike | str | PIL_Image.Image | IO[bytes] = None,
            /,
            key: Hashable = None,

            image_width: int = None,
            image_height: int = None,

            image_active: str | PathLike | PIL_Image.Image | IO[bytes] = None,
            image_disabled: str | PathLike | PIL_Image.Image | IO[bytes] = None,

            anchor: sg.Literals.anchor = None,

            state: sg.Literals.canv_elem_state = None,

            tk_kwargs: dict = None,
    ):
        super().__init__(key=key, tk_kwargs=tk_kwargs)

        self._image = image
        self._image_active = image_active
        self._image_disabled = image_disabled

        self._update_initial(
            *position,
            image_width = image_width,
            image_height = image_height,
            anchor = anchor,
            state = state,
        )

    def _update_special_key(self, key: str, new_val: Any) -> bool | None:
        match key:
            case "image":
                self._image = new_val
                self.add_flags(sg.ElementFlag.UPDATE_IMAGE)
            case "image_active":
                self._image_active = new_val
                self.add_flags(sg.ElementFlag.UPDATE_IMAGE)
            case "image_disabled":
                self._image_disabled = new_val
                self.add_flags(sg.ElementFlag.UPDATE_IMAGE)
            case "image_width":
                self._width = new_val
                self.add_flags(sg.ElementFlag.UPDATE_IMAGE)
            case "image_height":
                self._height = new_val
                self.add_flags(sg.ElementFlag.UPDATE_IMAGE)
            case _:  # Not a match
                return super()._update_special_key(key, new_val)

        return True

    @Canvas_Elements.BaseCanvasElement._run_after_window_creation
    def _update_image(self) -> Self:
        """
        Changes/sets/updates the image of the tk-element.

        :return:
        """
        image = image_to_tk_image(self._image, self._width, self._height)
        if image is not None:
            self._image_tk = image  # If the image doesn't get saved inside this element, it will be garbage-collected away...
            self.canvas.tk_widget.itemconfigure(self.canvas_id, image= image)

        image = image_to_tk_image(self._image_active, self._width, self._height)
        if image is not None:
            self._image_tk_active = image
            self.canvas.tk_widget.itemconfigure(self.canvas_id, activeimage= image)

        image = image_to_tk_image(self._image_disabled, self._width, self._height)
        if image is not None:
            self._image_tk_disabled = image
            self.canvas.tk_widget.itemconfigure(self.canvas_id, disabledimage= image)

        return self

    def _update_default_keys(self,kwargs: dict,transfer_keys: bool = True):
        super()._update_default_keys(kwargs, transfer_keys)

        if self.has_flag(sg.ElementFlag.UPDATE_IMAGE):
            self._update_image()
            self.remove_flags(sg.ElementFlag.UPDATE_IMAGE)
