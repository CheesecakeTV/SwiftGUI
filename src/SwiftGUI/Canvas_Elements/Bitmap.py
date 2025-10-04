from typing import Hashable

import SwiftGUI as sg
from SwiftGUI import Canvas_Elements
from SwiftGUI.Compat import Self


class Bitmap(Canvas_Elements.BaseCanvasElement):
    defaults = sg.GlobalOptions.Canvas_Bitmap

    _create_method = "create_bitmap"

    _transfer_keys = {
        "bitmap_active": "activebitmap",
        "bitmap_disabled": "disabledbitmap",

        "background_color": "background",
        "background_color_active": "activebackground",
        "background_color_disabled": "disabledbackground",

        "color": "foreground",
        "color_active": "activeforeground",
        "color_disabled": "disabledforeground",
    }

    def __init__(
            self,
            position: tuple[float, float],
            bitmap: sg.Literals.bitmap = None,
            /,
            key: Hashable = None,

            bitmap_active: sg.Literals.bitmap = None,
            bitmap_disabled: sg.Literals.bitmap = None,
            anchor: sg.Literals.anchor = None,

            background_color: sg.Color | str = None,
            background_color_active: sg.Color | str = None,
            background_color_disabled: sg.Color | str = None,

            color: sg.Color | str = None,
            color_active: sg.Color | str = None,
            color_disabled: sg.Color | str = None,

            state: sg.Literals.canv_elem_state = None,

            tk_kwargs: dict = None,
    ):
        super().__init__(key=key, tk_kwargs=tk_kwargs)

        self._update_initial(
            *position,
            bitmap = bitmap,
            bitmap_active = bitmap_active,
            bitmap_disabled = bitmap_disabled,
            anchor = anchor,
            background_color = background_color,
            background_color_active = background_color_active,
            background_color_disabled = background_color_disabled,
            color = color,
            color_active = color_active,
            color_disabled = color_disabled,
            state = state,
        )

    def update_coords(self, x: float, y: float) -> Self:
        super().update_coords((x, y))
        return self

