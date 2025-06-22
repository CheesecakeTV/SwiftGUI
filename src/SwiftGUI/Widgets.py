import tkinter as tk
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

            # Standard-Tkinter options
            cursor:Literals.cursor = None,
            take_focus:bool = None,

            # Special Tkinter-options
            #underline:int = None,
            justify:Literal["left","right","center"] = None,
            background:str|Color = None,
            border:int = None,

            tk_kwargs:dict[str:any]=None
    ):
        """

        :param text: Default text to be displayed
        :param key: Element-Key. Can be used to change the text later
        :param cursor: Cursor-Type. Changes how the cursor looks when hovering over this element
        :param take_focus: True, if you want this element to be able to be focused when pressing tab. Most likely False for texts.
        :param tk_kwargs: Additional kwargs to pass to the ttk-widget
        :param background: Background-Color
        """
        # Not used:
        # :param underline: Which character to underline for alt+character selection of this element

        super().__init__(key=key,tk_kwargs=tk_kwargs)

        if tk_kwargs is None:
            tk_kwargs = dict()

        self._tk_kwargs.update({
            **tk_kwargs,
            "cursor":cursor,
            "takefocus":take_focus,
            #"underline":None,
            "justify":justify,
            "background":background,
            "border":border,
        })

        self._text = text

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
