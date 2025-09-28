import tkinter as tk
import tkinter.font as font
from collections.abc import Iterable, Callable
from typing import Literal, Any

import SwiftGUI as sg
from SwiftGUI.Compat import Self

from SwiftGUI import ElementFlag, BaseWidget, GlobalOptions, Literals, Color

class Canvas(BaseWidget):
    _tk_widget_class: type = tk.Canvas  # Class of the connected widget
    tk_widget: tk.Canvas
    defaults = GlobalOptions.Canvas  # Default values (Will be applied to kw_args-dict and passed onto the tk_widget
    value: None

    _transfer_keys = {
        # "background_color_disabled": "disabledbackground",
        "background_color": "bg",
        "text_color_disabled": "disabledforeground",
        "highlightbackground_color": "highlightbackground",
        "selectbackground_color": "selectbackground",
        "select_text_color": "selectforeground",
        "background_color_active": "activebackground",
        "text_color_active": "activeforeground",
        "text_color": "fg",
        "bitmap_position": "compound",
        "check_background_color": "selectcolor",
    }

    def __init__(
            self,
            /,
            key: Any = None,
            default_event: bool = False,
            key_function: Callable | Iterable[Callable] = None,

            width: int = None,
            height: int = None,

            select_text_color: str | Color = None,
            selectbackground_color: str | Color = None,
            selectborderwidth: int = None,

            borderwidth:int = None,

            cursor: Literals.cursor = None,
            takefocus: bool = None,

            background_color: str | Color = None,
            apply_parent_background_color: bool = None,

            highlightbackground_color: str | Color = None,
            highlightcolor: str | Color = None,
            highlightthickness: int = None,

            confine: bool = None,
            scrollregion: tuple[int, int, int, int] = None,

            closeenough: int = None,

            relief: Literals.relief = None,

            expand: bool = None,
            expand_y: bool = None,
            tk_kwargs: dict = None,
    ):
        super().__init__(key, tk_kwargs=tk_kwargs, expand=expand,expand_y=expand_y)

        self._key_function = key_function

        if background_color and not apply_parent_background_color:
            apply_parent_background_color = False

        self._default_event = default_event

        self._update_initial(
            width = width,
            height = height,
            select_text_color = select_text_color,
            selectbackground_color = selectbackground_color,
            selectborderwidth = selectborderwidth,
            borderwidth = borderwidth,
            cursor = cursor,
            takefocus = takefocus,
            background_color = background_color,
            apply_parent_background_color = apply_parent_background_color,
            highlightbackground_color = highlightbackground_color,
            highlightcolor = highlightcolor,
            highlightthickness = highlightthickness,
            confine = confine,
            scrollregion = scrollregion,
            closeenough = closeenough,
            relief = relief,
        )

    def set_value(self, val: None):
        raise AttributeError("A canvas-object does not have a 'value'.")

    def _get_value(self) -> None:
        return None

    def _personal_init_inherit(self):
        super()._personal_init_inherit()

    def init_window_creation_done(self):
        if self._default_event:
            self.bind_event("<Button-1>", key=self.key, key_function=self._key_function)

    def _update_special_key(self, key: str, new_val: Any) -> bool | None:
        # Fish out all special keys to process them seperately
        match key:
            case "apply_parent_background_color":
                if new_val:
                    self.add_flags(ElementFlag.APPLY_PARENT_BACKGROUND_COLOR)
                else:
                    self.remove_flags(ElementFlag.APPLY_PARENT_BACKGROUND_COLOR)
            case _:  # Not a match
                return super()._update_special_key(key, new_val)

        return True

