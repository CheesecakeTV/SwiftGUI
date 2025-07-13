import tkinter as tk
import tkinter.font as font
import tkinter.ttk as ttk
from collections.abc import Iterable, Callable
from typing import Literal

from SwiftGUI import BaseElement, ElementFlag, BaseWidget, BaseWidgetContainer, GlobalOptions, Literals, Color

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
