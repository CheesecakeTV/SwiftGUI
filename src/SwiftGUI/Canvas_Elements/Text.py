from typing import Hashable, Any, Literal
from tkinter import font

import SwiftGUI as sg
from SwiftGUI import Canvas_Elements
from SwiftGUI.Compat import Self


class Text(Canvas_Elements.BaseCanvasElement):
    defaults = sg.GlobalOptions.Canvas_Text

    _create_method = "create_text"

    _transfer_keys = {
        "color": "fill",
        "stippleoffset": "offset",

        "color_disabled": "disabledfill",
        "dash_disabled": "disableddash",
        "stipple_disabled": "disabledstipple",

        "color_active": "activefill",
        "dash_active": "activedash",
        "stipple_active": "activestipple",
    }

    def __init__(
            self,
            position: tuple[float, float],
            text: str = None,
            *,
            key: Hashable = None,

            width: float = None,

            color: str | sg.Color = None,
            color_active: str | sg.Color = None,
            color_disabled: str | sg.Color = None,

            # Doesn't work and won't be used anyways...
            # If you do want to stipple your text, pass it via the tk_kwargs, or tell me how to fix it.

            # stipple: sg.Literals.bitmap = None,
            # stippleoffset: str | tuple[float, float] = None,
            # stipple_active: sg.Literals.bitmap = None,
            # stipple_disabled: sg.Literals.bitmap = None,

            state: sg.Literals.canv_elem_state = None,

            anchor: sg.Literals.anchor = None,
            justify: Literal["left", "right", "center"] = None,

            fonttype: str = None,
            fontsize: int = None,
            font_bold: bool = None,
            font_italic: bool = None,
            font_underline: bool = None,
            font_overstrike: bool = None,

            tk_kwargs: dict = None,
    ):
        super().__init__(key=key, tk_kwargs=tk_kwargs)

        self._update_initial(
            *position,
            text = text,
            width = width,
            color = color,
            color_active = color_active,
            color_disabled = color_disabled,
            # stipple = stipple,
            # stippleoffset = stippleoffset,
            # stipple_active = stipple_active,
            # stipple_disabled = stipple_disabled,
            state = state,
            anchor = anchor,
            justify = justify,
            fonttype = fonttype,
            fontsize = fontsize,
            font_bold = font_bold,
            font_italic = font_italic,
            font_underline = font_underline,
            font_overstrike = font_overstrike,
        )

    @sg.BaseElement._run_after_window_creation
    def _update_font(self):
        # self._tk_kwargs will be passed to tk_widget later
        new_font = font.Font(
            self.canvas.tk_widget,
            family=self._fonttype,
            size=self._fontsize,
            weight="bold" if self._bold else "normal",
            slant="italic" if self._italic else "roman",
            underline=bool(self._underline),
            overstrike=bool(self._overstrike),
        )
        self.canvas.tk_widget.itemconfigure(self.canvas_id, font= new_font)
        #self.update_after_window_creation(font= new_font)

    def _update_special_key(self, key: str, new_val: Any) -> bool | None:
        match key:
            case "fonttype":
                self._fonttype = self.defaults.single(key, new_val)
                self.add_flags(sg.ElementFlag.UPDATE_FONT)
            case "fontsize":
                self._fontsize = self.defaults.single(key, new_val)
                self.add_flags(sg.ElementFlag.UPDATE_FONT)
            case "font_bold":
                self._bold = self.defaults.single(key, new_val)
                self.add_flags(sg.ElementFlag.UPDATE_FONT)
            case "font_italic":
                self._italic = self.defaults.single(key, new_val)
                self.add_flags(sg.ElementFlag.UPDATE_FONT)
            case "font_underline":
                self._underline = self.defaults.single(key, new_val)
                self.add_flags(sg.ElementFlag.UPDATE_FONT)
            case "font_overstrike":
                self._overstrike = self.defaults.single(key, new_val)
                self.add_flags(sg.ElementFlag.UPDATE_FONT)
            # case "apply_parent_background_color":
            #     if new_val:
            #         self.add_flags(sg.ElementFlag.APPLY_PARENT_BACKGROUND_COLOR)
            #     else:
            #         self.remove_flags(sg.ElementFlag.APPLY_PARENT_BACKGROUND_COLOR)
            case _:  # Not a match
                return super()._update_special_key(key, new_val)

        return True

    def _update_default_keys(self,kwargs: dict,transfer_keys: bool = True):
        super()._update_default_keys(kwargs, transfer_keys)

        if self.has_flag(sg.ElementFlag.UPDATE_FONT):
            self._update_font()
            self.remove_flags(sg.ElementFlag.UPDATE_FONT)

    def _get_value(self) -> str:
        return self.get_option("text", "")

    def set_value(self, new_val: str) -> Self:
        self.update(text= new_val)
        return self
