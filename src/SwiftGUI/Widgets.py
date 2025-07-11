import tkinter as tk
import tkinter.font as font
import tkinter.ttk as ttk
from collections.abc import Iterable, Callable
from typing import Literal

from SwiftGUI import BaseElement, ElementFlag, BaseWidget, BaseWidgetContainer, GlobalOptions, Literals, Color


# Todo: Add docstrings to __init__ methods
class Example(BaseWidget):
    _tk_widget_class = ttk.Label  # Class of your tk-widget
    defaults = GlobalOptions.DEFAULT_OPTIONS_CLASS      # Default options to be applied

    def _personal_init_inherit(self):
        self._set_tk_target_variable(tk.StringVar,"textvariable", default_key="text")


class Text(BaseWidget):
    """
    Copy this class ot create your own Widget
    """
    _tk_widget_class:type = ttk.Label # Class of the connected widget
    defaults = GlobalOptions.Text   # Default values (Will be applied to kw_args-dict and passed onto the tk_widget

    def __init__(
            self,
            # Add here
            text:str = None,
            key:any=None,
            width:int=None,

            # Standard-Tkinter options
            cursor:Literals.cursor = None,
            takefocus:bool = None,

            # Special Tkinter-options
            underline:int = None,
            anchor:Literals.anchor = None,
            justify:Literal["left","right","center"] = None,
            background_color:str|Color = None,
            text_color:str|Color = None,
            relief:Literals.relief = None,
            padding:Literals.padding = None,

            # Mixed options
            fonttype:str = None,
            fontsize:int = None,
            font_bold:bool = None,
            font_italic:bool = None,
            font_underline:bool = None,
            font_overstrike:bool = None,

            tk_kwargs:dict[str:any]=None
    ):
        """

        :param text: Default text to be displayed
        :param key: Element-Key. Can be used to change the text later
        :param cursor: Cursor-Type. Changes how the cursor looks when hovering over this element
        :param takefocus: True, if you want this element to be able to be focused when pressing tab. Most likely False for texts.
        :param tk_kwargs: Additional kwargs to pass to the ttk-widget
        :param background_color: Background-Color
        """
        # Not used:
        # :param underline: Which character to underline for alt+character selection of this element

        super().__init__(key=key,tk_kwargs=tk_kwargs)

        if tk_kwargs is None:
            tk_kwargs = dict()

        _tk_kwargs = {
            **tk_kwargs,
            "cursor":cursor,
            "takefocus":takefocus,
            "underline":underline,
            "justify":justify,
            "background_color":background_color,
            #"borderwidth":borderwidth,
            "relief":relief,
            "text_color":text_color,
            "padding":padding,
            "width":width,
            # "wraplength":"1c" # Todo: integrate wraplength in a smart way
            "fonttype":fonttype,
            "fontsize":fontsize,
            "font_bold":font_bold,
            "font_italic":font_italic,
            "font_underline":font_underline,
            "font_overstrike":font_overstrike,
            "anchor":anchor,
        }
        self.update(**_tk_kwargs)

        self._text = text

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

    def _update_special_key(self,key:str,new_val:any) -> bool|None:
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
            case "background_color":
                self._tk_kwargs["background"] = self.defaults.single(key,new_val)
            case "text_color":
                self._tk_kwargs["foreground"] = self.defaults.single(key,new_val)
            case _: # Not a match
                return False

        return True

    def _apply_update(self):
        # If the font changed, apply them to self._tk_kwargs
        if self.has_flag(ElementFlag.UPDATE_FONT):
            self._update_font()

        super()._apply_update() # Actually apply the update

    def _personal_init_inherit(self):
        self._set_tk_target_variable(default_value=self._text)


class Frame(BaseWidgetContainer):
    """
    Copy this class ot create your own Widget
    """
    _tk_widget_class:type[ttk.Frame] = tk.Frame # Class of the connected widget
    defaults = GlobalOptions.Frame

    def __init__(
            self,
            layout:Iterable[Iterable[BaseElement]],
            alignment:Literals.alignment = None,
            expand:bool = False,
            # Add here
            tk_kwargs:dict[str:any]=None,
    ):
        super().__init__(tk_kwargs=tk_kwargs)

        self._contains = layout

        if tk_kwargs is None:
            tk_kwargs = dict()
        self._tk_kwargs.update({
            **tk_kwargs,
            # Insert named arguments for the widget here
        })

        self._insert_kwargs["expand"] = self.defaults.single("expand",expand)

        self._insert_kwargs_rows.update({
            "side":self.defaults.single("alignment",alignment),
        })

    def window_entry_point(self,root:tk.Tk|tk.Widget,window:BaseElement):
        """
        Starting point for the whole window, or part of the layout.
        Don't use this unless you overwrite the sg.Window class
        :param window: Window Element
        :param root: Window to put every element
        :return:
        """
        self.window = window
        self.window.add_flags(ElementFlag.IS_CREATED)
        self.add_flags(ElementFlag.IS_CONTAINER)
        self._init_widget(root)

class Spacer(BaseWidget):
    """
    Spacer with a certain width in pixels
    """
    _tk_widget_class = tk.Frame

    def __init__(
            self,
            width:int = None,
            height:int = None,
    ):
        super().__init__()

        self._tk_kwargs = {
            "width":width,
            "height":height,
        }

# Aliases

class Button(BaseWidget):
    """
    Copy this class ot create your own Widget

    The following methods are to be overwritten if needed:
    _get_value  (determines the value returned by this widget)
    _init_widget_for_inherrit   (Initializes the widget)
    """
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

    }

    def __init__(
            # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/button.html

            self,
            # Add here
            text:str = "",
            key:any = None,
            key_function:Callable|Iterable[Callable] = None,

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
            background_color: str | Color = None,
            overrelief: Literals.relief = None,
            text_color: str | Color = None,
            # Todo: image
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

            tk_kwargs: dict[str:any] = None
    ):
        super().__init__(key=key,tk_kwargs=tk_kwargs)

        if tk_kwargs is None:
            tk_kwargs = dict()

        _tk_kwargs = {
            **tk_kwargs,
            "text":text,
            "cursor":cursor,
            "underline":underline,
            "justify":justify,
            "background_color":background_color,
            "highlightbackground_color":"red",
            "highlightthickness":5,
            "highlightcolor":"purple",
            "relief":relief,
            "text_color":text_color,
            "width":width,
            "fonttype":fonttype,
            "fontsize":fontsize,
            "font_bold":font_bold,
            "font_italic":font_italic,
            "font_underline":font_underline,
            "font_overstrike":font_overstrike,
            "anchor":anchor,
            "bitmap":bitmap,
            "borderwidth":borderwidth,
            "disabled":disabled,
            "overrelief":overrelief,
            "takefocus":takefocus,
            #"background_color_disabled": background_color_disabled,    # Todo: Add this manually since tk.Button has no option for it
            "text_color_disabled": text_color_disabled,
            "background_color_active": background_color_active,
            "text_color_active": text_color_active,
            "repeatdelay":repeatdelay,
            "repeatinterval":repeatinterval,

            "height": height,
            "padx": padx,
            "pady": pady,
        }
        self.update(**_tk_kwargs)

        self._key_function = key_function

    def _update_special_key(self,key:str,new_val:any) -> bool|None:
        match key:

            case "disabled":
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
                return False

        return True

    def _apply_update(self):
        # If the font changed, apply them to self._tk_kwargs
        if self.has_flag(ElementFlag.UPDATE_FONT):
            self._update_font()

        super()._apply_update() # Actually apply the update

    def _personal_init(self):
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
        "background_color_disabled":"disabledbackground",
        "background_color_readonly":"readonlybackground",
        "background_color":"background",
        "text_color":"foreground",
        "text_color_disabled": "disabledforeground",
        "highlightbackground_color": "highlightbackground",
        "selectbackground_color": "selectbackground",
        "select_text_color": "selectforeground",
        "pass_char":"show",
    }

    def __init__(
            self,   # Todo: Test all options
            # Add here
            text:str = None,
            key:any=None,
            key_function:Callable|Iterable[Callable] = None,
            width:int=None,
            default_event:bool = False,
            #
            # Standard-Tkinter options
            cursor:Literals.cursor = None,
            takefocus:bool = None,
            #
            # Special Tkinter-options
            justify:Literal["left","right","center"] = None,
            background_color:str|Color = None,
            background_color_disabled:str|Color = None,
            background_color_readonly:str|Color = None,
            text_color:str|Color = None,
            text_color_disabled:str|Color = None,
            highlightbackground_color:str|Color = None,
            selectbackground_color:str|Color = None,
            select_text_color:str|Color = None,
            selectborderwidth:int = None,
            highlightcolor:str|Color = None,
            highlightthickness:int = None,
            pass_char:str = None,
            readonly:bool = None,   # Set state to tk.Normal, or 'readonly'
            relief:Literals.relief = None,
            exportselection:bool = None,
            validate:Literals.validate = None,
            validatecommand:callable = None,
            #
            # Mixed options
            fonttype:str = None,
            fontsize:int = None,
            font_bold:bool = None,
            font_italic:bool = None,
            font_underline:bool = None,
            font_overstrike:bool = None,
            #
            tk_kwargs:dict[str:any]=None
    ):
        """

        :param text: Default text to be displayed
        :param key: Element-Key. Can be used to change the text later
        :param cursor: Cursor-Type. Changes how the cursor looks when hovering over this element
        :param takefocus: True, if you want this element to be able to be focused when pressing tab. Most likely False for texts.
        :param tk_kwargs: Additional kwargs to pass to the ttk-widget
        :param background_color: Background-Color
        """
        # Not used:
        # :param underline: Which character to underline for alt+character selection of this element

        super().__init__(key=key,tk_kwargs=tk_kwargs)
        self._key_function = key_function

        if tk_kwargs is None:
            tk_kwargs = dict()

        if default_event:   # Todo: Exclude shift+ctrl+alt from default event-calls
            self.bind_event("<KeyRelease>",key=self.key,key_function=self._key_function)

        _tk_kwargs = {
            **tk_kwargs,
            "takefocus":takefocus,
            "background_color":background_color,
            "background_color_disabled": background_color_disabled,
            "background_color_readonly": background_color_readonly,
            "cursor": cursor,
            "readonly": readonly,
            "exportselection": exportselection,
            "font_bold": font_bold,
            "font_italic": font_italic,
            "font_overstrike": font_overstrike,
            "font_underline": font_underline,
            "fontsize": fontsize,
            "fonttype": fonttype,
            "highlightbackground_color": highlightbackground_color,
            "highlightcolor": highlightcolor,
            "highlightthickness": highlightthickness,
            "justify": justify,
            "pass_char": pass_char,
            "relief": relief,
            "select_text_color": select_text_color,
            "selectbackground_color": selectbackground_color,
            "selectborderwidth": selectborderwidth,
            "text": text,
            "text_color": text_color,
            "text_color_disabled": text_color_disabled,
            "validate": validate,
            "validatecommand": validatecommand,
            "width": width,
        }
        self.update(**_tk_kwargs)

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

    def _update_special_key(self,key:str,new_val:any) -> bool|None:
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
            case "readonly":
                self._tk_kwargs["state"] = "readonly" if new_val else "normal"
            case _: # Not a match
                return False

        return True

    def _apply_update(self):
        # If the font changed, apply them to self._tk_kwargs
        if self.has_flag(ElementFlag.UPDATE_FONT):
            self._update_font()

        super()._apply_update() # Actually apply the update

    def _personal_init_inherit(self):
        self._set_tk_target_variable(default_key="text")


class Separator(BaseWidget):
    _tk_widget_class = ttk.Separator

    def __init__(self,orient:Literal["vertical","horizontal"]):
        super().__init__(key=None,tk_kwargs={"orient":orient})

class VerticalSeparator(Separator):
    def __init__(self):
        super().__init__(orient="vertical")

    def _personal_init_inherit(self):
        self._insert_kwargs["fill"] = "y"

class HorizontalSeparator(Separator):
    def __init__(self):
        super().__init__(orient="horizontal")

    def _personal_init_inherit(self):
        self._insert_kwargs["fill"] = "x"
        self._insert_kwargs["expand"] = True

        self.add_flags(ElementFlag.EXPAND_ROW)

class Checkbox(BaseWidget):

    _tk_widget_class:type = tk.Checkbutton # Class of the connected widget
    defaults = GlobalOptions.Checkbox   # Default values (Will be applied to kw_args-dict and passed onto the tk_widget
    value:bool

    _transfer_keys = {

    }

    def __init__(
            self,
            text:str = None,
            key:any=None,
            default_event:bool = False,
            key_function:Callable|Iterable[Callable] = None,
            default_value:bool = False,
            fonttype:str = None,
            fontsize:int = None,
            font_bold:bool = None,
            font_italic:bool = None,
            font_underline:bool = None,
            font_overstrike:bool = None,
            readonly:bool = None,
            tk_kwargs:dict = None,
    ):
        super().__init__(key,tk_kwargs=tk_kwargs)

        self._key_function = key_function

        if tk_kwargs is None:
            tk_kwargs = dict()


        _tk_kwargs = {
            **tk_kwargs,
            "default_value":default_value,
            "font_bold": font_bold,
            "font_italic": font_italic,
            "font_overstrike": font_overstrike,
            "font_underline": font_underline,
            "fontsize": fontsize,
            "fonttype": fonttype,
            "readonly": readonly,
            # "takefocus":takefocus,
            # "background_color":background_color,
            # "background_color_disabled": background_color_disabled,
            # "background_color_readonly": background_color_readonly,
            # "cursor": cursor,
            # "readonly": readonly,
            # "exportselection": exportselection,
            # "font_bold": font_bold,
            # "font_italic": font_italic,
            # "font_overstrike": font_overstrike,
            # "font_underline": font_underline,
            # "fontsize": fontsize,
            # "fonttype": fonttype,
            # "highlightbackground_color": highlightbackground_color,
            # "highlightcolor": highlightcolor,
            # "highlightthickness": highlightthickness,
            # "justify": justify,
            # "pass_char": pass_char,
            # "relief": relief,
            # "select_text_color": select_text_color,
            # "selectbackground_color": selectbackground_color,
            # "selectborderwidth": selectborderwidth,
            "text": text,
            # "text_color": text_color,
            # "text_color_disabled": text_color_disabled,
            # "validate": validate,
            # "validatecommand": validatecommand,
            # "width": width,
        }

        self._default_event = default_event

        # self.bind_event("<KeyRelease>",key=self.key,key_function=self._key_function)

        self.update(**_tk_kwargs)

    def _personal_init_inherit(self):
        self._set_tk_target_variable(tk.IntVar,kwargs_key="variable",default_key="default_value")

        if self._default_event:
            self._tk_kwargs["command"] = self.window.get_event_function(self,key=self.key,key_function=self._key_function,)
    
    def _get_value(self) -> bool:
        return bool(super()._get_value())

    def set_value(self,val:bool):
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

    def _update_special_key(self,key:str,new_val:any) -> bool|None:
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
            case "readonly":
                self._tk_kwargs["state"] = "disabled" if new_val else "normal"
            case _: # Not a match
                return False

        return True

    def _apply_update(self):
        # If the font changed, apply them to self._tk_kwargs
        if self.has_flag(ElementFlag.UPDATE_FONT):
            self._update_font()

        super()._apply_update() # Actually apply the update
