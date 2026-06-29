import tkinter as tk
import tkinter.font as font
from collections.abc import Iterable, Callable
from typing import Literal, Any, Hashable
from SwiftGUI.Compat import Self

from SwiftGUI import ElementFlag, BaseWidget, GlobalOptions, Literals, Color, \
    MixinElementWithValue


class Scale(MixinElementWithValue, BaseWidget):
    _tk_widget_class: type = tk.Scale  # Class of the connected widget
    tk_widget: tk.Scale
    defaults = GlobalOptions.Scale  # Default values (Will be applied to kw_args-dict and passed onto the tk_widget
    value: float | int

    _transfer_keys = {
        # "background_color_disabled": "disabledbackground",
        "background_color": "bg",
        "highlightbackground_color": "highlightbackground",
        # "selectbackground_color": "selectbackground",
        # "select_text_color": "selectforeground",
        "background_color_active": "activebackground",
        "text_color_active": "activeforeground",
        "text_color": "fg",
        "bitmap_position": "compound",
        "check_background_color": "selectcolor",

        "number_format": "format",
        "number_min": "from_",
        "number_max": "to",
    }

    def __init__(
            self,
            *,
            key: Hashable = None,
            key_function: Callable | Iterable[Callable] = None,
            default_event: bool = False,
            default_event_on_value_change: bool = None,    # Generate an event on EVERY value-change. Normally only on button-release

            default_value: int | float = None,
            number_min: float = None,
            number_max: float = None,
            resolution: float = None,
            showvalue: bool = None,
            tickinterval: float = None,

            width: int = None,
            length: int = None,
            sliderlength: int = None,
            sliderrelief: Literals.relief = None,
            background_color_active: str | Color = None,
            orient: Literal["horizontal", "vertical"] = None,

            disabled: bool = None,

            fonttype: str = None,
            fontsize: int = None,
            font_bold: bool = None,
            font_italic: bool = None,
            font_underline: bool = None,
            font_overstrike: bool = None,

            readonly: bool = None,
            borderwidth:int = None,

            label: str = None,
            text_color: str | Color = None,
            troughcolor: str | Color = None,

            digits: int = None,

            cursor: Literals.cursor = None,
            takefocus: bool = None,

            background_color: str | Color = None,
            apply_parent_background_color: bool = None,

            relief: Literals.relief = None,
            highlightbackground_color: str | Color = None,
            highlightcolor: str | Color = None,
            highlightthickness: int = None,

            repeatdelay: int = None,
            repeatinterval: int = None,

            expand: bool = None,
            expand_y: bool = None,
            tk_kwargs: dict = None,
    ):
        super().__init__(key, tk_kwargs=tk_kwargs, expand=expand,expand_y=expand_y, default_event=default_event, default_value=default_value)

        self._key_function = key_function
        self._default_event_on_value_change = self.defaults.single("default_event_on_value_change", default_event_on_value_change)

        if background_color and not apply_parent_background_color:
            apply_parent_background_color = False

        self._update_initial(
            default_value = default_value,
            number_min = number_min,
            number_max = number_max,
            resolution = resolution,
            showvalue = showvalue,
            tickinterval = tickinterval,
            width = width,
            length = length,
            sliderlength = sliderlength,
            sliderrelief = sliderrelief,
            orient = orient,
            disabled = disabled,
            fonttype = fonttype,
            fontsize = fontsize,
            font_bold = font_bold,
            font_italic = font_italic,
            font_underline = font_underline,
            font_overstrike = font_overstrike,
            readonly = readonly,
            borderwidth = borderwidth,
            label = label,
            text_color = text_color,
            troughcolor = troughcolor,
            digits = digits,
            cursor = cursor,
            takefocus = takefocus,
            apply_parent_background_color = apply_parent_background_color,
            relief = relief,
            highlightbackground_color = highlightbackground_color,
            highlightcolor = highlightcolor,
            highlightthickness = highlightthickness,
            repeatdelay = repeatdelay,
            repeatinterval = repeatinterval,
            background_color = background_color,
            background_color_active = background_color_active,
        )

    def set_value(self,val: float) -> Self:
        self._apply_value(val)
        super().set_value(val)
        return self

    def _get_value(self) -> float:
        return float(super()._get_value())

    def _personal_init_inherit(self):
        self._set_tk_target_variable(tk.StringVar, kwargs_key="variable", default_key= "default_value")

    def init_window_creation_done(self):
        super().init_window_creation_done()
        self._apply_value(self.value)

        if self._default_event_on_value_change:
            self.tk_widget.configure(command = self._event_callback)
        else:
            self.tk_widget.bind("<ButtonRelease>", self._event_callback)

    def _update_font(self):
        # self._tk_kwargs will be passed to tk_widget later
        self._tk_kwargs["font"] = font.Font(
            self.window.parent_tk_widget,
            family=self._fonttype,
            size=self._fontsize,
            weight="bold" if self._bold else "normal",
            slant="italic" if self._italic else "roman",
            underline=bool(self._underline),
            overstrike=bool(self._overstrike),
        )

    def _update_special_key(self, key: str, new_val: Any) -> bool | None:
        # Fish out all special keys to process them seperately
        match key:
            case "fonttype":
                self._fonttype = self.defaults.single(key, new_val)
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "fontsize":
                self._fontsize = self.defaults.single(key, new_val)
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "font_bold":
                self._bold = self.defaults.single(key, new_val)
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "font_italic":
                self._italic = self.defaults.single(key, new_val)
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "font_underline":
                self._underline = self.defaults.single(key, new_val)
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "font_overstrike":
                self._overstrike = self.defaults.single(key, new_val)
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "disabled":
                self._tk_kwargs["state"] = "disabled" if new_val else "normal"
            case "apply_parent_background_color":
                if new_val:
                    self.add_flags(ElementFlag.APPLY_PARENT_BACKGROUND_COLOR)
                else:
                    self.remove_flags(ElementFlag.APPLY_PARENT_BACKGROUND_COLOR)
            case _:  # Not a match
                return super()._update_special_key(key, new_val)

        return True

    def _apply_update(self):
        # If the font changed, apply them to self._tk_kwargs
        if self.has_flag(ElementFlag.UPDATE_FONT):
            self.remove_flags(ElementFlag.UPDATE_FONT)
            self._update_font()

        super()._apply_update()  # Actually apply the update

