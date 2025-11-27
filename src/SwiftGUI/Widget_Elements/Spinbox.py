import tkinter as tk
import tkinter.font as font
from collections.abc import Iterable, Callable
from typing import Literal, Any

from SwiftGUI import ElementFlag, BaseWidget, GlobalOptions, Literals, Color
from SwiftGUI.Compat import Self


class Spinbox(BaseWidget):
    _tk_widget_class: type = tk.Spinbox # Class of the connected widget
    tk_widget: tk.Spinbox
    defaults = GlobalOptions.Spinbox   # Default values (Will be applied to kw_args-dict and passed onto the tk_widget

    _transfer_keys = {
        "background_color_disabled": "disabledbackground",
        "background_color_readonly": "readonlybackground",
        "background_color": "background",
        "background_color_active" : "activebackground",

        "text_color": "foreground",
        "text_color_disabled": "disabledforeground",
        "text_color_active": "activeforeground",
        "insertbackground_color": "insertbackground",

        "highlightbackground_color": "highlightbackground",
        "selectbackground_color": "selectbackground",
        "select_text_color": "selectforeground",
        "pass_char": "show",
        "background_color_button": "buttonbackground",
        "cursor_button": "buttoncursor",
        "relief_button_down": "buttondownrelief",
        "relief_button_up": "buttonup",

        "number_format": "format",
        "number_min": "from_",
        "number_max": "to",
    }

    def __init__(
            self,
            # Add here
            values: Iterable[Any] = None,
            /,
            key:Any=None,
            key_function:Callable|Iterable[Callable] = None,
            default_event:bool = False,

            default_value: Any = None,
            value_type: type = None,

            cursor: Literals.cursor = None,
            cursor_button: Literals.cursor = None,
            takefocus: bool = None,
            justify: Literal["left","right","center"] = None,

            background_color: str|Color = None,
            background_color_active: str | Color = None,
            background_color_disabled: str|Color = None,
            background_color_readonly: str|Color = None,
            text_color: str|Color = None,
            text_color_disabled: str|Color = None,

            background_color_button: Color | str = None,

            highlightbackground_color: str|Color = None,
            selectbackground_color: str|Color = None,
            select_text_color: str|Color = None,

            borderwidth: int = None,
            selectborderwidth: int = None,

            highlightcolor: str|Color = None,
            highlightthickness: int = None,

            relief: Literals.relief = None,
            relief_button_down: Literals.relief = None,
            relief_button_up: Literals.relief = None,
            insertbackground_color: str | Color = None,

            fonttype: str = None,
            fontsize: int = None,
            font_bold: bool = None,
            font_italic: bool = None,
            font_underline: bool = None,
            font_overstrike: bool = None,

            wrap: bool = None,
            number_format: str = None,
            number_min: float = None,
            number_max: float = None,
            increment: float = None,

            width: int=None,

            repeatdelay: int = None,
            repeatinterval: int = None,

            state: Literals.Spinbox_State = None,

            expand: bool = None,
            expand_y: bool = None,
            tk_kwargs: dict[str:Any]= None,
    ):



        if tk_kwargs is None:
            tk_kwargs = dict()

        super().__init__(key=key,tk_kwargs=tk_kwargs,expand=expand,expand_y=expand_y)
        self._key_function = key_function

        self._default_val = default_value
        self._value_type = self.defaults.single("value_type", default= float)

        self._update_initial(cursor=cursor, cursor_button=cursor_button,
                             takefocus=takefocus, justify=justify, background_color=background_color,
                             background_color_active=background_color_active,
                             background_color_disabled=background_color_disabled,
                             background_color_readonly=background_color_readonly, text_color=text_color,
                             text_color_disabled=text_color_disabled, background_color_button=background_color_button,
                             highlightbackground_color=highlightbackground_color,
                             selectbackground_color=selectbackground_color, select_text_color=select_text_color,
                             borderwidth=borderwidth, selectborderwidth=selectborderwidth,
                             highlightcolor=highlightcolor, highlightthickness=highlightthickness, relief=relief,
                             relief_button_down=relief_button_down, relief_button_up=relief_button_up,
                             fonttype=fonttype, fontsize=fontsize, font_bold=font_bold, font_italic=font_italic,
                             font_underline=font_underline, font_overstrike=font_overstrike,
                             values=tuple(values) if values else None, wrap=wrap, number_format=number_format,
                             number_min=number_min, number_max=number_max, increment=increment, width=width,
                             repeatdelay=repeatdelay, repeatinterval=repeatinterval, state=state,
                             insertbackground_color=insertbackground_color,
                             # validate = "key",  # This restricts the user to one type of value
                             # validatecommand = (self.parent.register(self._validate), "%P"),  # This too
                             **tk_kwargs)

        self._default_event = default_event

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

    def _update_special_key(self,key:str,new_val:Any) -> bool|None:
        # Fish out all special keys to process them seperately
        match key:
            case "fonttype":
                self._fonttype = self.defaults.single(key,new_val)
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "fontsize":
                self._fontsize = self.defaults.single(key,new_val)
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "font_bold":
                self._bold = self.defaults.single(key,new_val)
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "font_italic":
                self._italic = self.defaults.single(key,new_val)
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "font_underline":
                self._underline = self.defaults.single(key,new_val)
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "font_overstrike":
                self._overstrike = self.defaults.single(key,new_val)
                self.add_flags(ElementFlag.UPDATE_FONT)
            case _: # Not a match
                return super()._update_special_key(key, new_val)

        return True

    def _apply_update(self):
        # If the font changed, apply them to self._tk_kwargs
        if self.has_flag(ElementFlag.UPDATE_FONT):
            self._update_font()
            self.remove_flags(ElementFlag.UPDATE_FONT)

        super()._apply_update() # Actually apply the update

    def _personal_init_inherit(self):
        self._set_tk_target_variable(kwargs_key="textvariable")

        if self._default_event:
            self._window_event_function = self.window.get_event_function(
                me = self,
                key = self.key,
                key_function= self._key_function,
            )

            #self._last_event_value = self.value()
            self._tk_target_value.trace_add("write", self._value_change_callback)

    _last_viable_value: Any = None
    def _get_value(self) -> Any:
        try:
            self._last_viable_value = self._tk_target_value.get()
        except tk.TclError:  # _tk_target_value isn't used
            pass

        return self._value_type(self._last_viable_value)

    def _validate(self, val: Any) -> bool:
        print("validate", val)
        try:
            self._value_type(val)
            return True
        except (ValueError, TypeError):
            return False

    def set_value(self,val:Any) -> Self:
        try:
            self._last_event_value = self._value_type(val)
        except (ValueError, TypeError) as ex:
            raise ex.__class__(f"You tried to write a {val.__class__.__name__} to a spin-box that only allows {self._value_type.__name__}.")

        return super().set_value(val)

    _window_event_function: Callable = None
    _last_event_value: Any = None
    def _value_change_callback(self, *_):   # Only throws an event on value-changes
        if not self.window.exists:
            return

        if self._last_event_value != self.value:
            self._last_event_value = self.value
            self._window_event_function()   # Call the actual event

    def init_window_creation_done(self):
        super().init_window_creation_done()

        self._update_initial(
            validate= "key",
            validatecommand = (self.parent_tk_widget.register(self._validate), "%P")
        )

        if self._default_val is not None:   # No idea why the usual way doesn't work in this case...
            self._last_event_value = self._value_type(self._default_val)
            self._tk_target_value.set(self._default_val)
