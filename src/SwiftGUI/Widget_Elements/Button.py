import tkinter as tk
import tkinter.font as font
from collections.abc import Iterable, Callable
from typing import Literal

from SwiftGUI import ElementFlag, BaseWidget, GlobalOptions, Literals, Color


class Button(BaseWidget):
    tk_widget:tk.Button
    _tk_widget_class:type = tk.Button # Class of the connected widget
    defaults = GlobalOptions.Button

    _transfer_keys = {
        "background_color_disabled":"disabledbackground",
        "background_color":"background",
        "text_color_disabled": "disabledforeground",
        "highlightbackground_color": "highlightbackground",
        # "selectbackground_color": "selectbackground",
        # "select_text_color": "selectforeground",
        # "pass_char":"show",
        "background_color_active" : "activebackground",
        "text_color_active" : "activeforeground",
        "text_color":"fg",
        "bitmap_position": "compound",
    }

    def __init__(
            # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/button.html

            self,
            # Add here
            text:str = "",
            /,
            key:any = None,
            key_function:Callable|Iterable[Callable] = None,
            default_event = True,

            borderwidth:int = None,

            bitmap:Literals.bitmap = None,
            bitmap_position: Literals.compound = None,
            disabled:bool = None,
            text_color_disabled: str | Color = None,
            background_color_active: str | Color = None,
            text_color_active: str | Color = None,
            highlightcolor: str | Color = None,

            width: int = None,
            height: int = None,
            padx:int = None,
            pady:int = None,

            cursor: Literals.cursor = None,
            takefocus: bool = None,

            underline: int = None,
            anchor: Literals.anchor = None,
            justify: Literal["left", "right", "center"] = None,
            background_color: str | Color = None,
            text_color: str | Color = None,

            relief: Literals.relief = None,
            overrelief: Literals.relief = None,

            repeatdelay:int = None,
            repeatinterval:int = None,

            fonttype: str = None,
            fontsize: int = None,
            font_bold: bool = None,
            font_italic: bool = None,
            font_underline: bool = None,
            font_overstrike: bool = None,

            expand: bool = None,
            expand_y: bool = None,
            tk_kwargs: dict[str:any] = None
    ):
        """
        A button that throws an event every time it is pushed

        :param text: Text the button displays
        :param key: (See docs for more details)
        :param key_function: (See docs for more details)
        :param borderwidth: Border-Thickness in pixels. Default is 2
        :param bitmap: The are a couple of icons builtin. If you are using PyCharm, they should be suggested when pressing "ctrl+space"
        :param disabled: True, if this button should not be pressable
        :param text_color_disabled: Text color, if disabled = True
        :param background_color_active: Background color shown only when the button is held down
        :param text_color_active: Text color only shown when the button is held down
        :param width: Button-size in x-direction in text-characters
        :param height: Button-height in text-rows
        :param padx: Adds space to both sides not filled with text. Should not be combined with "width". The value is given in characters
        :param pady: Adds space to the top and bottom not filled with text. Should not be combined with "height". The value is given in rows
        :param cursor: How the cursor should look when hovering over this element.
        :param takefocus: True, if this element should be able to get focus (e.g. by pressing tab)
        :param underline: Underlines the single character at this index
        :param anchor: Specifies, where the text in this element should be placed (See docs for more details)
        :param justify: When the text is multiple rows long, this will specify where the new rows begin.
        :param background_color: Background-color for the non-pressed state
        :param overrelief: Relief when the mouse hovers over the element
        :param text_color: Text-color in non-pressed state
        :param relief: Relief in non-pressed state
        :param repeatdelay: How long to hold the button until repeation starts (doesn't work without "repeatinterval")
        :param repeatinterval: How long to wait between repetitions (doesn't work without "repeatdelay")
        :param fonttype: Use sg.font_windows. ... to select some fancy font. Personally, I like sg.font_windows.Small_Fonts
        :param fontsize: Size (height) of the font in pixels
        :param font_bold: True, if thicc text
        :param font_italic: True, if italic text
        :param font_underline: True, if the text should be underlined
        :param font_overstrike: True, if the text should be overstruck
        :param tk_kwargs: (Only if you know tkinter) Pass more kwargs directly to the tk-widget
        """
        super().__init__(key=key,tk_kwargs=tk_kwargs,expand=expand,expand_y=expand_y)

        if tk_kwargs is None:
            tk_kwargs = dict()

        self._update_initial(
            **tk_kwargs,
            text = text,
            cursor = cursor,
            underline = underline,
            justify = justify,
            background_color = background_color,
            #"highlightbackground_color":"cyan",
            highlightthickness = 0,
            highlightcolor = highlightcolor,
            relief = relief,
            text_color = text_color,
            width = width,
            fonttype = fonttype,
            fontsize = fontsize,
            font_bold = font_bold,
            font_italic = font_italic,
            font_underline = font_underline,
            font_overstrike = font_overstrike,
            anchor = anchor,
            bitmap = bitmap,
            borderwidth = borderwidth,
            disabled = disabled,
            overrelief = overrelief,
            takefocus = takefocus,
            text_color_disabled = text_color_disabled,
            background_color_active = background_color_active,
            text_color_active = text_color_active,
            repeatdelay = repeatdelay,
            repeatinterval = repeatinterval,
            height = height,
            padx = padx,
            pady = pady,
            bitmap_position = bitmap_position,
        )

        self._default_event = default_event
        self._key_function = key_function

    _disabled_at_start = False
    def _update_special_key(self,key:str,new_val:any) -> bool|None:
        match key:

            case "disabled":
                if not self.has_flag(ElementFlag.IS_CREATED):
                    self._disabled_at_start = new_val
                    return True

                self._tk_kwargs["state"] = "disabled" if new_val else "normal"
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
            case _:
                return super()._update_special_key(key, new_val)

        return True

    def _apply_update(self):
        # If the font changed, apply them to self._tk_kwargs
        if self.has_flag(ElementFlag.UPDATE_FONT):
            self.remove_flags(ElementFlag.UPDATE_FONT)
            self._update_font()

        super()._apply_update() # Actually apply the update

    def _personal_init(self):
        if self._default_event:
            self._tk_kwargs.update({
                "command": self.window.get_event_function(self, self.key, self._key_function)
            })

        super()._personal_init()

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

    def _personal_init_inherit(self):
        self._set_tk_target_variable(default_key="text")


    def flash(self):
        """
        Flash the button visually
        :return:
        """
        if self._window_is_dead():
            return

        self.tk_widget.flash()

    def push_once(self):
        """
        "Push" the button virtually
        :return:
        """
        if self._window_is_dead():
            return

        self.tk_widget.invoke()

    def init_window_creation_done(self):
        super().init_window_creation_done()
        if self._disabled_at_start:
            self._update_initial(disabled=True)
