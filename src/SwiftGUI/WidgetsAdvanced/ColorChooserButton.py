import tkinter as tk
from tkinter import colorchooser
from collections.abc import Iterable, Callable
from typing import Literal

from SwiftGUI import GlobalOptions, Literals, Color
from SwiftGUI.Widgets.Button import Button


class ColorChooserButton(Button):
    """
    Small Element to create a button that lets you chose a color
    """
    tk_widget:tk.Button
    _tk_widget_class:type = tk.Button # Class of the connected widget
    defaults = GlobalOptions.ColorChooserButton

    def __init__(
            # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/button.html

            self,
            # Add here
            text:str = "",
            /,
            key:any = None,
            key_function:Callable|Iterable[Callable] = None,

            initial_color: str | Color = None,
            color_chooser_title: str = None,

            borderwidth:int = None,

            bitmap:Literals.bitmap = None,
            disabled:bool = None,
            text_color_disabled: str | Color = None,
            background_color_active: str | Color = None,
            text_color_active: str | Color = None,

            width: int = None,
            height: int = None,
            padx:int = None,
            pady:int = None,

            cursor: Literals.cursor = None,
            takefocus: bool = None,

            underline: int = None,
            anchor: Literals.anchor = None,
            justify: Literal["left", "right", "center"] = None,
            #background_color: str | Color = None,
            overrelief: Literals.relief = None,
            text_color: str | Color = None,
            relief: Literals.relief = None,

            repeatdelay:int = None,
            repeatinterval:int = None,

            # # Mixed options
            fonttype: str = None,
            fontsize: int = None,
            font_bold: bool = None,
            font_italic: bool = None,
            font_underline: bool = None,
            font_overstrike: bool = None,

            expand: bool = None,
            tk_kwargs: dict[str:any] = None
    ):
        """
        A button that throws an event every time it is pushed

        :param text: Text the button displays
        :param key: (See docs for more details)
        :param key_function: (See docs for more details)

        :param initial_color: Color that should be displayed in the beginning


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
        if callable(key_function):
            key_function = (self._button_callback,key_function)
        elif key_function:
            key_function = (self._button_callback,*tuple(key_function))
        else:
            key_function = self._button_callback

        super().__init__(
            text,
            key=key,
            key_function=key_function,
            borderwidth=borderwidth,
            bitmap=bitmap,
            disabled=disabled,
            text_color_disabled=text_color_disabled,
            background_color_active=background_color_active,
            text_color_active=text_color_active,
            width=width,
            height=height,
            padx=padx,
            pady=pady,
            cursor=cursor,
            takefocus=takefocus,
            underline=underline,
            anchor=anchor,
            justify=justify,
            #background_color=background_color,
            overrelief=overrelief,
            text_color=text_color,
            relief=relief,
            repeatdelay=repeatdelay,
            repeatinterval=repeatinterval,
            fonttype=fonttype,
            fontsize=fontsize,
            font_bold=font_bold,
            font_italic=font_italic,
            font_underline=font_underline,
            font_overstrike=font_overstrike,
            expand=expand,
            tk_kwargs=tk_kwargs,
        )

        self._file_function_kwargs = dict()

        self.update(
            initial_color = initial_color,
            color_chooser_title = color_chooser_title,
        )

    _prev_val:str = None
    def _button_callback(self):
        # Call the file-dialogue
        _,temp = colorchooser.askcolor(initialcolor=self._prev_val,title=self._title)

        if temp is None:
            return

        self.value = str(temp)

        return True # Refresh values for coming key_functions

    def _get_value(self) -> any:
        return self._prev_val

    def set_value(self,val:any):
        self._prev_val = val
        self.update(background_color = val)

    _title:str = None
    def _update_special_key(self,key:str,new_val:any) -> bool|None:
        if super()._update_special_key(key,new_val):
            return True

        match key:
            case "initial_color":
                self.value = new_val
            case "color_chooser_title":
                self._title = new_val
            case _:
                return False

        return True

    def _personal_init_inherit(self):
        pass    # Avoid creating a target variable for this button, so the text can be changed with .update(text="...")

