import tkinter as tk
import tkinter.font as font
from collections.abc import Iterable, Callable
from typing import Literal, Any, Hashable

from SwiftGUI import ElementFlag, BaseWidget, GlobalOptions, Literals, Color
from SwiftGUI.Compat import Self


class Input(BaseWidget):
    """
    Copy this class ot create your own Widget

    The following methods are to be overwritten if needed:
    _get_value  (determines the value returned by this widget)
    _init_widget_for_inherrit   (Initializes the widget)
    """
    _tk_widget_class:type = tk.Entry # Class of the connected widget
    defaults = GlobalOptions.Input   # Default values (Will be applied to kw_args-dict and passed onto the tk_widget

    _transfer_keys = {
        "background_color_readonly":"readonlybackground",
        "background_color":"background",
        "text_color":"foreground",
        #"text_color_disabled": "disabledforeground",
        "highlightbackground_color": "highlightbackground",
        "selectbackground_color": "selectbackground",
        "select_text_color": "selectforeground",
        "pass_char":"show",
        "insertbackground_color":"insertbackground",
    }

    def __init__(
            self,
            # Add here
            text: str = None,
            *,
            key: Hashable = None,
            key_function: Callable|Iterable[Callable] = None,
            default_event: bool = False,

            width: int = None,
            #
            cursor: Literals.cursor = None,
            takefocus: bool = None,
            #
            justify: Literal["left","right","center"] = None,
            background_color: str|Color = None,
            background_color_readonly: str|Color = None,
            text_color: str|Color = None,
            #text_color_disabled: str|Color = None,
            highlightbackground_color: str|Color = None,
            selectbackground_color: str|Color = None,
            select_text_color: str|Color = None,
            insertbackground_color: str | Color = None,
            selectborderwidth: int = None,
            highlightcolor: str|Color = None,
            highlightthickness: int = None,
            pass_char: str = None,
            readonly: bool = None,   # Set state to tk.Normal, or 'readonly'
            relief: Literals.relief = None,
            exportselection: bool = None,
            validate: Literals.validate = None,
            validatecommand: Callable = None,
            #
            fonttype: str = None,
            fontsize: int = None,
            font_bold: bool = None,
            font_italic: bool = None,
            font_underline: bool = None,
            font_overstrike: bool = None,
            #
            expand: bool = None,
            expand_y: bool = None,
            tk_kwargs: dict[str:Any]=None
    ):
        """

        :param text: Text initially shown in the input-field
        :param key:
        :param key_function:
        :param default_event: True, if changing the text should cause an event
        :param width: Width in number of letters. If you make the font bigger, the input will be bigger too.
        :param cursor: How the cursor looks while over the element
        :param takefocus: True, if this element can be selected by pressing tab
        :param justify: Where the text is relative to the input
        :param background_color:
        :param background_color_readonly:
        :param text_color:
        :param highlightbackground_color: (Doesn't work on windows) Color of the border around the element while not in focus
        :param selectbackground_color:
        :param select_text_color:
        :param insertbackground_color:
        :param selectborderwidth:
        :param highlightcolor: (Doesn't work on windows) Color of the border around the element while in focus
        :param highlightthickness: (Doesn't work on windows) Thickness of the border around the element
        :param pass_char: Pass a char to show every character as it. Set it to "*" to make it look like a passwort-input-field
        :param readonly: True, if the user shouldn't be able to change text
        :param relief: Relief-Style of the element. Just play around with this or check the documentation.
        :param exportselection: Haven't found out what it does yet... Just ignore it for now...
        :param validate: This is complicated. Check the documentation for details.
        :param validatecommand: This is complicated. Check the documentation for details.
        :param fonttype: Text-font
        :param fontsize: Size of the text (font)
        :param font_bold: Bold
        :param font_italic: Italic
        :param font_underline: Underline
        :param font_overstrike: Overstrike
        :param expand: Span the input-element over the whole row
        :param expand_y:
        :param tk_kwargs: Other arguments passed directly to the tkinter widget
        """
        # Not used:
        # :param underline: Which character to underline for alt+character selection of this element

        super().__init__(key=key,tk_kwargs=tk_kwargs,expand=expand,expand_y=expand_y)
        self._key_function = key_function

        if tk_kwargs is None:
            tk_kwargs = dict()

        self._default_event = default_event
        self._value_change_callback: Callable | None = None
        # if default_event:
        #     self.bind_event("<KeyRelease>",key=self.key,key_function=self._key_function)

        self._update_initial(
            takefocus = takefocus,
            background_color = background_color,
            background_color_readonly = background_color_readonly,
            cursor = cursor,
            readonly = readonly,
            exportselection = exportselection,
            font_bold = font_bold,
            font_italic = font_italic,
            font_overstrike = font_overstrike,
            font_underline = font_underline,
            fontsize = fontsize,
            fonttype = fonttype,
            highlightbackground_color = highlightbackground_color,
            highlightcolor = highlightcolor,
            highlightthickness = highlightthickness,
            justify = justify,
            pass_char = pass_char,
            relief = relief,
            select_text_color = select_text_color,
            selectbackground_color = selectbackground_color,
            selectborderwidth = selectborderwidth,
            text = text,
            text_color = text_color,
            #text_color_disabled = text_color_disabled,
            validate = validate,
            validatecommand = validatecommand,
            width = width,
            insertbackground_color = insertbackground_color,
            **tk_kwargs,
        )

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

    def _update_special_key(self, key: str, new_val: Any) -> bool|None:
        # Fish out all special keys to process them seperately
        match key:
            case "default_event":
                self._default_event = new_val
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
            case "readonly":
                self._tk_kwargs["state"] = "readonly" if new_val else "normal"
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
        self._set_tk_target_variable(default_key="text")

    def init_window_creation_done(self):
        super().init_window_creation_done()
        self._value_change_callback = self.window.get_event_function(self, key= self.key, key_function= self._key_function)
        self._tk_target_value.trace_add("write", self._event_callback)

    def set_value(self, val:str) -> Self:
        self._prev_value = val  # Avoid event trigger
        super().set_value(val)
        return self

    _prev_value: str = None
    def _event_callback(self, *_):
        value = self.value
        if self._prev_value == value:
            return

        self._prev_value = value
        if self._default_event:
            self._value_change_callback()

