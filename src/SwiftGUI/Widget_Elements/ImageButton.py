import io
import tkinter as tk
from os import PathLike
from typing import Callable, Iterable, Any
from PIL import Image as PIL_Image

from SwiftGUI import GlobalOptions, Image, Button, Literals, Color
from SwiftGUI.Compat import Self


class ImageButton(Button, Image):
    _tk_widget_class = tk.Button
    tk_widget: tk.Button

    defaults = GlobalOptions.ImageButton

    def __init__(
            self,
            image: str | PathLike | PIL_Image.Image | io.BytesIO = None,
            /,
            key: Any = None,
            key_function: Callable | Iterable[Callable] = None,

            text: str = None,
            compound: Literals.compound = None,

            borderwidth: int = None,

            disabled: bool = None,
            text_color_disabled: str | Color = None,
            background_color_active: str | Color = None,

            image_width: int = None,
            image_height: int = None,
            
            width: int = None,
            height: int = None,

            cursor: Literals.cursor = None,
            takefocus: bool = None,

            background_color: str | Color = None,

            relief: Literals.relief = None,
            overrelief: Literals.relief = None,

            repeatdelay: int = None,
            repeatinterval: int = None,

            expand: bool = None,
            expand_y: bool = None,
            tk_kwargs: dict[str:Any] = None
    ):
        super().__init__(
            text,
            key= key,
            key_function= key_function,
            expand= expand,
            expand_y= expand_y,
            cursor = cursor,
            takefocus = takefocus,
            background_color = background_color,
            relief = relief,
            overrelief = overrelief,
            repeatdelay = repeatdelay,
            repeatinterval = repeatinterval,
            borderwidth = borderwidth,
            disabled = disabled,
            text_color_disabled = text_color_disabled,
            background_color_active = background_color_active,
            width=width,
            height=height,
            tk_kwargs=tk_kwargs,
        )

        self._height = None
        self._width = None

        self._update_initial(image=image, image_height=image_height, image_width=image_width, compound=compound)

    def _get_value(self) -> Any:
        return self._tk_target_value.get()

    def set_value(self,val: Any) -> Self:
        self._tk_target_value.set(val)
        return self

