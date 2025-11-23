import tkinter as tk
import tkinter.font as font
from collections.abc import Iterable, Callable
from typing import Literal, Any

from SwiftGUI import ElementFlag, BaseWidget, GlobalOptions, Literals, Color


class Checkbox(BaseWidget):
    _tk_widget_class: type = tk.Checkbutton  # Class of the connected widget
    tk_widget: tk.Checkbutton
    defaults = GlobalOptions.Checkbox  # Default values (Will be applied to kw_args-dict and passed onto the tk_widget
    value: bool

    _grab_anywhere_on_this = True

    _transfer_keys = {
        # "background_color_disabled": "disabledbackground",
        "background_color": "background",
        "text_color_disabled": "disabledforeground",
        "highlightbackground_color": "highlightbackground",
        # "selectbackground_color": "selectbackground",
        # "select_text_color": "selectforeground",
        # "pass_char":"show",
        "background_color_active": "activebackground",
        "text_color_active": "activeforeground",
        "text_color": "fg",
        "bitmap_position": "compound",
        "check_background_color": "selectcolor",
    }

    def __init__(
            self,
            text: str = None,
            /,
            key: Any = None,
            default_event: bool = False,
            key_function: Callable | Iterable[Callable] = None,
            default_value: bool = False,
            fonttype: str = None,
            fontsize: int = None,
            font_bold: bool = None,
            font_italic: bool = None,
            font_underline: bool = None,
            font_overstrike: bool = None,
            disabled: bool = None,
            borderwidth:int = None,
            #
            bitmap: Literals.bitmap = None,
            text_color_disabled: str | Color = None,
            check_background_color: str | Color = None,
            bitmap_position: Literals.compound = None,
            background_color_active: str | Color = None,
            text_color_active: str | Color = None,
            check_type: Literals.indicatoron = None,
            #
            width: int = None,
            height: int = None,
            padx: int = None,
            pady: int = None,
            #
            cursor: Literals.cursor = None,
            takefocus: bool = None,
            #
            underline: int = None,
            anchor: Literals.anchor = None,
            justify: Literal["left", "right", "center"] = None,
            background_color: str | Color = None,
            apply_parent_background_color: bool = None,
            overrelief: Literals.relief = None,
            offrelief: Literals.relief = None,
            text_color: str | Color = None,
            relief: Literals.relief = None,
            # hilightbackground_color: str | Color = None,
            # highlightcolor: str | Color = None,
            highlightcolor: str | Color = None,
            expand: bool = None,
            expand_y: bool = None,
            tk_kwargs: dict = None,
    ):
        super().__init__(key, tk_kwargs=tk_kwargs, expand=expand,expand_y=expand_y)

        self._key_function = key_function

        if tk_kwargs is None:
            tk_kwargs = dict()

        if self.defaults.single("background_color", background_color) and not apply_parent_background_color:
            apply_parent_background_color = False

        if check_type == "button":
            self._grab_anywhere_on_this = False

        self._update_initial(
            default_value = default_value,
            font_bold = font_bold,
            font_italic = font_italic,
            font_overstrike = font_overstrike,
            font_underline = font_underline,
            fontsize = fontsize,
            fonttype = fonttype,
            disabled = disabled,
            bitmap_position = bitmap_position,
            bitmap = bitmap,
            check_background_color = check_background_color,
            borderwidth = borderwidth,
            check_type = check_type,
            cursor = cursor,
            underline = underline,
            justify = justify,
            background_color = background_color,
            apply_parent_background_color = apply_parent_background_color,
            highlightthickness = 0,
            highlightcolor = highlightcolor,
            relief = relief,
            text_color = text_color,
            width = width,
            anchor = anchor,
            overrelief = overrelief,
            offrelief = offrelief,
            takefocus = takefocus,
            text_color_disabled = text_color_disabled,
            background_color_active = background_color_active,
            text_color_active = text_color_active,
            height = height,
            padx = padx,
            pady = pady,
            text = text,
            **tk_kwargs,
        )

        self._default_event = default_event

        # self.bind_event("<KeyRelease>",key=self.key,key_function=self._key_function)

    def _personal_init_inherit(self):
        self._set_tk_target_variable(tk.IntVar, kwargs_key="variable", default_key="default_value")

        if self._default_event:
            self._tk_kwargs["command"] = self.window.get_event_function(self, key=self.key,
                                                                        key_function=self._key_function, )

    def _get_value(self) -> bool:
        return bool(super()._get_value())

    def set_value(self, val: bool):
        super().set_value(int(val))

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
            case "check_type":
                self._tk_kwargs["indicatoron"] = int(new_val == "check")
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
            self._update_font()
            self.remove_flags(ElementFlag.UPDATE_FONT)

        super()._apply_update()  # Actually apply the update

    def toggle(self):
        """
        Toggle the button WITHOUT throwing an event.
        :return:
        """
        self.tk_widget.toggle()

    def flash(self):
        """
        Flash the Element a couple of times
        :return:
        """
        self.tk_widget.flash()

