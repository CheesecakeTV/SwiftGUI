import tkinter as tk
import tkinter.font as font
import tkinter.ttk as ttk
from collections.abc import Iterable, Callable
from typing import Literal

from SwiftGUI import BaseElement, ElementFlag, BaseWidget, BaseWidgetContainer, GlobalOptions, Literals, Color


# Todo: Add docstrings to __init__ methods

class Example(BaseWidget):
    """
    Copy this class ot create your own Widget

    The following methods are to be overwritten if needed:
    _get_value  (determines the value returned by this widget)
    _init_widget_for_inherrit   (Initializes the widget)
    """
    _tk_widget_class:type[tk.Widget] = None # Class of the connected widget
    defaults = GlobalOptions.Common # Change this to your default-option-class if needed

    def __init__(
            self,
            # Add here
            tk_kwargs:dict[str:any]=None
    ):
        super().__init__(tk_kwargs=tk_kwargs)

        if tk_kwargs is None:
            tk_kwargs = dict()

        self._tk_kwargs.update({
            **tk_kwargs
            # Insert named arguments for the widget here
        })

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
            take_focus:bool = None,

            # Special Tkinter-options
            underline:int = None,
            justify:Literal["left","right","center"] = None,
            background_color:str|Color = None,
            text_color:str|Color = None,
            #borderwidth:int = None, # Todo: Check if this even exists
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
        :param take_focus: True, if you want this element to be able to be focused when pressing tab. Most likely False for texts.
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
            "takefocus":take_focus,
            "underline":underline,
            "justify":justify,
            "background":self.defaults.single("background_color",background_color),
            #"borderwidth":borderwidth,
            "relief":relief,
            "foreground":self.defaults.single("text_color",text_color),
            "padding":padding,
            "width":width,
            # "wraplength":"1c" # Todo: integrate wraplength in a smart way
            "fonttype":fonttype,
            "fontsize":fontsize,
            "font_bold":font_bold,
            "font_italic":font_italic,
            "font_underline":font_underline,
            "font_overstrike":font_overstrike,
        }
        self.update(**_tk_kwargs)

        self._text = text

    def _update_font(self):
        # self._tk_kwargs will be passed to tk_widget later
        self._tk_kwargs["font"] = font.Font(
            self.window.tk_widget,
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

# Aliases
T = Text
Label = Text


class Frame(BaseWidgetContainer):
    """
    Copy this class ot create your own Widget
    """
    _tk_widget_class:type[ttk.Frame] = ttk.Frame # Class of the connected widget

    def __init__(
            self,
            layout:Iterable[Iterable[BaseElement]],
            # Add here
            tk_args:tuple[any]=tuple(),
            tk_kwargs:dict[str:any]=None
    ):
        super().__init__(tk_kwargs=tk_kwargs)

        self._contains = layout

        if tk_kwargs is None:
            tk_kwargs = dict()
        self._tk_kwargs.update({
            **tk_kwargs
            # Insert named arguments for the widget here
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
        self.add_flags(ElementFlag.IS_CONTAINER)
        self._init_widget(root)


# Aliases
Column = Frame

class Button(BaseWidget):
    """
    Copy this class ot create your own Widget

    The following methods are to be overwritten if needed:
    _get_value  (determines the value returned by this widget)
    _init_widget_for_inherrit   (Initializes the widget)
    """
    _tk_widget_class:type = ttk.Button # Class of the connected widget

    def __init__(
            self,
            # Add here
            text:str = "",
            key:any = None,
            key_function:Callable|Iterable[Callable] = None,
            tk_kwargs:dict[str:any]=None
    ):
        super().__init__(key=key,tk_kwargs=tk_kwargs)

        if tk_kwargs is None:
            tk_kwargs = dict()

        self._tk_kwargs.update({
            **tk_kwargs,
            # Insert named arguments for the widget here
            "text":text,
        })
        #tk.Button(command=)

        self._key_function = key_function

    def _personal_init(self):
        self._tk_kwargs.update({
            "command": self.window.get_event_function(self, self.key, self._key_function)
        })

        super()._personal_init()

class Input(BaseWidget):
    """
    Copy this class ot create your own Widget

    The following methods are to be overwritten if needed:
    _get_value  (determines the value returned by this widget)
    _init_widget_for_inherrit   (Initializes the widget)
    """
    _tk_widget_class:type = ttk.Entry # Class of the connected widget

    def __init__(
            self,
            # Add here
            text:str = "",
            key:any = None,
            key_function:Callable|Iterable[Callable] = None,
            tk_args:tuple[any]=tuple(),
            tk_kwargs:dict[str:any]=None
    ):
        super().__init__(key=key,tk_kwargs=tk_kwargs)

        if tk_kwargs is None:
            tk_kwargs = dict()

        self._tk_kwargs.update({
            **tk_kwargs,
            # Insert named arguments for the widget here
            "text":text,
        })
        #tk.Button(command=)

        self._key_function = key_function

    def _personal_init(self):
        self._tk_target_value = tk.StringVar(self.window.tk_widget)

        self._tk_kwargs.update({
            #"command": self.window.get_event_function(self.key, self._key_function),
            "textvariable":self._tk_target_value,
        })

        super()._personal_init()

# Aliases
In = Input
Entry = Input
