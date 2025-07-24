import tkinter as tk
import tkinter.font as font
import tkinter.ttk as ttk
from collections.abc import Iterable, Callable
from typing import Literal

from SwiftGUI import ElementFlag, BaseWidget, GlobalOptions, Literals, Color


class TKContainer(BaseWidget):
    """
    Integrate a single TK-Widget into the layout
    """
    tk_widget:tk.BaseWidget
    #_tk_widget_class:type = tk.Button # Class of the connected widget
    defaults = GlobalOptions.DEFAULT_OPTIONS_CLASS  # No default options here...

    def __init__(
            self,
            # Add here
            widget_type:type[tk.Widget],
            /,
            key:str = None,
            pack_arguments:dict = None,
            expand:bool = False,
            **tk_kwargs,
    ):
        """
        Integrate a tkinter widget into your layout
        """
        super().__init__(key=key,tk_kwargs=tk_kwargs,expand=expand)

        self._tk_widget_class = widget_type

        if pack_arguments:
            self._insert_kwargs = pack_arguments
        else:
            self._insert_kwargs = dict()

