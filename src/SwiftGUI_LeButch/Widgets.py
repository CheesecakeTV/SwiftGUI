import tkinter as tk
from collections.abc import Iterable, Callable
from SwiftGUI_LeButch import BaseElement
from .Base import BaseWidget,BaseContainer


# Todo: Add docstrings to __init__ methods

class Example(BaseWidget):
    """
    Copy this class ot create your own Widget

    The following methods are to be overwritten if needed:
    _get_value  (determines the value returned by this widget)
    _init_widget_for_inherrit   (Initializes the widget)
    """
    _tk_widget_class:type = None # Class of the connected widget

    def __init__(
            self,
            # Add here
            tk_args:tuple[any]=tuple(),
            tk_kwargs:dict[str:any]=None
    ):
        super().__init__(tk_args=tk_args,tk_kwargs=tk_kwargs)

        if tk_kwargs is None:
            tk_kwargs = dict()

        self._tk_args = self._tk_args + tk_args # Add anonymous arguments for the widget here
        self._tk_kwargs.update({
            **tk_kwargs
            # Insert named arguments for the widget here
        })

class Text(BaseWidget):
    """
    Copy this class ot create your own Widget
    """
    _tk_widget_class:type = tk.Label # Class of the connected widget

    def __init__(
            self,
            # Add here
            text:str = "",

            tk_args:tuple[any]=tuple(),
            tk_kwargs:dict[str:any]=None
    ):
        super().__init__(tk_args=tk_args,tk_kwargs=tk_kwargs)

        if tk_kwargs is None:
            tk_kwargs = dict()

        self._tk_kwargs.update({
            **tk_kwargs,
            "text":text,
        })

T = Text
Label = Text


class Frame(BaseContainer):
    """
    Copy this class ot create your own Widget
    """
    _tk_widget_class:type = tk.Frame # Class of the connected widget

    def __init__(
            self,
            layout:Iterable[Iterable[BaseElement]],
            # Add here
            tk_args:tuple[any]=tuple(),
            tk_kwargs:dict[str:any]=None
    ):
        super().__init__(tk_args=tk_args,tk_kwargs=tk_kwargs)

        self.contains = layout

        self._tk_args = self._tk_args + tk_args # Add anonymous arguments for the widget here
        if tk_kwargs is None:
            tk_kwargs = dict()
        self._tk_kwargs.update({
            **tk_kwargs
            # Insert named arguments for the widget here
        })


class Button(BaseWidget):
    """
    Copy this class ot create your own Widget

    The following methods are to be overwritten if needed:
    _get_value  (determines the value returned by this widget)
    _init_widget_for_inherrit   (Initializes the widget)
    """
    _tk_widget_class:type = tk.Button # Class of the connected widget

    def __init__(
            self,
            # Add here
            text:str = "",
            key:any = None,
            key_function:Callable|Iterable[Callable] = None,
            key_function_send_wev:bool = False,
            tk_args:tuple[any]=tuple(),
            tk_kwargs:dict[str:any]=None
    ):
        super().__init__(tk_args=tk_args,tk_kwargs=tk_kwargs)

        if tk_kwargs is None:
            tk_kwargs = dict()

        self._tk_args = self._tk_args + tk_args # Add anonymous arguments for the widget here
        self._tk_kwargs.update({
            **tk_kwargs,
            # Insert named arguments for the widget here
            "text":text,
        })
        #tk.Button(command=)

        self.key = key
        self.key_function = key_function
        self._key_function_send_wev = key_function_send_wev

    def _personal_init(self):
        self._tk_kwargs.update({
            "command": self.window.get_event_function(self.key, self.key_function, self._key_function_send_wev)
        })

        super()._personal_init()



