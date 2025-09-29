from typing import Hashable

import SwiftGUI as sg
from SwiftGUI import Canvas_Elements


class Line(Canvas_Elements.BaseCanvasElement):
    defaults = sg.GlobalOptions.Canvas_Line

    _create_method = "create_line"

    _transfer_keys = {
        "color": "fill",
        "stippleoffset": "offset",

        "color_disabled": "disabledfill",
        "dash_disabled": "disableddash",
        "stipple_disabled": "disabledstipple",
        "width_disabled": "disabledwidth",

        "color_active": "activefill",
        "dash_active": "activedash",
        "stipple_active": "activestipple",
        "width_active": "activewidth",
    }

    def __init__(
            self,
            *points: tuple[float, float],

            key: Hashable = None,

            width: float = None,
            width_active: float = None,
            width_disabled: float = None,

            smooth: bool = None,
            splinesteps: int = None,

            color: str | sg.Color = None,
            color_active: str | sg.Color = None,
            color_disabled: str | sg.Color = None,

            dash: tuple[int, ...] = None,
            dashoffset: int = None,
            dash_active: tuple[int, ...] = None,
            dash_disabled: tuple[int, ...] = None,

            stipple: sg.Literals.bitmap = None,
            stippleoffset: str | tuple[float, float] = None, # Todo: correct typehinting: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/stipple-offset.html
            stipple_active: sg.Literals.bitmap = None,
            stipple_disabled: sg.Literals.bitmap = None,

            arrow: sg.Literals.arrow = None,
            arrowshape: tuple[float, float, float] = None,

            capstyle: sg.Literals.capstyle = None,
            joinstyle: sg.Literals.joinstyle = None,

            state: sg.Literals.canv_elem_state = None,

            tk_kwargs: dict = None,
    ):
        super().__init__(key=key, tk_kwargs=tk_kwargs)

        points = self._flatten(points)

        self._update_initial(
            *points,
            width = width,
            width_active = width_active,
            width_disabled = width_disabled,
            smooth = smooth,
            splinesteps = splinesteps,
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
            arrow = arrow,
            arrowshape = arrowshape,
            capstyle = capstyle,
            joinstyle = joinstyle,
            state = state,
        )


