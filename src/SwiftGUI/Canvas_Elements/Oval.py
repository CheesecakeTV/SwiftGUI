from typing import Hashable

import SwiftGUI as sg
from SwiftGUI import Canvas_Elements


# Good explanation for this object: https://tkinter-docs.readthedocs.io/en/latest/widgets/canvas.html#Canvas.create_arc
class Oval(Canvas_Elements.BaseCanvasElement):
    defaults = sg.GlobalOptions.Canvas_Oval

    _create_method = "create_oval"

    _transfer_keys = {
        "infill_color": "fill",
        "infill_color_disabled": "disabledfill",
        "infill_color_active": "activefill",

        "stipple": "outlinestipple",
        "stippleoffset": "outlineoffset",

        "color": "outline",
        "color_disabled": "disabledoutline",
        "color_active": "activeoutline",

        "dash_disabled": "disableddash",
        "dash_active": "activedash",

        "infill_stipple": "stipple",
        "infill_stippleoffset": "offset",
        "infill_stipple_disabled": "disabledstipple",
        "infill_stipple_active": "activestipple",

        "stipple_disabled": "disabledoutlinestipple",
        "stipple_active": "activeoutlinestipple",

        "width_disabled": "disabledwidth",
        "width_active": "activewidth",

        "start_angle": "start",
        "extent_angle": "extent",
    }

    def __init__(
            self,
            upper_left: tuple[float, float],
            lower_right: tuple[float, float],
            *,
            key: Hashable = None,

            width: float = None,
            width_active: float = None,
            width_disabled: float = None,

            infill_color: str | sg.Color = None,
            infill_color_active: str | sg.Color = None,
            infill_color_disabled: str | sg.Color = None,

            color: str | sg.Color = None,
            color_active: str | sg.Color = None,
            color_disabled: str | sg.Color = None,

            dash: sg.Literals.canv_dash = None,
            dashoffset: int = None,
            dash_active: sg.Literals.canv_dash = None,
            dash_disabled: sg.Literals.canv_dash = None,

            stipple: sg.Literals.bitmap = None,
            stippleoffset: str | tuple[float, float] = None,
            stipple_active: sg.Literals.bitmap = None,
            stipple_disabled: sg.Literals.bitmap = None,

            infill_stipple: sg.Literals.bitmap = None,
            infill_stippleoffset: str | tuple[float, float] = None,
            infill_stipple_active: sg.Literals.bitmap = None,
            infill_stipple_disabled: sg.Literals.bitmap = None,

            state: sg.Literals.canv_elem_state = None,

            tk_kwargs: dict = None,
    ):
        super().__init__(key=key, tk_kwargs=tk_kwargs)

        self._update_initial(
            *upper_left,
            *lower_right,
            width = width,
            width_active = width_active,
            width_disabled = width_disabled,
            infill_color = infill_color,
            infill_color_active = infill_color_active,
            infill_color_disabled = infill_color_disabled,
            color = color,
            color_active = color_active,
            color_disabled = color_disabled,
            dash = dash,
            dashoffset = dashoffset,
            dash_active = dash_active,
            dash_disabled = dash_disabled,
            stipple = stipple,
            stippleoffset = stippleoffset,
            stipple_active = stipple_active,
            stipple_disabled = stipple_disabled,
            infill_stipple = infill_stipple,
            infill_stippleoffset = infill_stippleoffset,
            infill_stipple_active = infill_stipple_active,
            infill_stipple_disabled = infill_stipple_disabled,
            state = state,
        )


