import tkinter as tk
from tkinter import ttk

from SwiftGUI import BaseWidget, GlobalOptions

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
            widget_type:type[tk.Widget | ttk.Widget],
            /,
            key:str = None,
            pack_kwargs:dict = None,
            expand:bool = False,
            expand_y: bool = None,
            **tk_kwargs,
    ):
        """
        Integrate a tkinter widget into your layout
        :param widget_type: Class of the widget
        :param key: Widget-key. Will only be used in key-functions and to retrieve the element out of sg.Window
        :param pack_kwargs: When .pack is called, these kwargs will be passed to .pack.
        :param expand: True, if this widget should fill the whole row
        :param tk_kwargs: These kwargs will be passed directly to the widget when it is initialized.
        """
        super().__init__(key=key,tk_kwargs=tk_kwargs,expand=expand,expand_y=expand_y)

        self._tk_widget_class = widget_type

        if pack_kwargs:
            self._insert_kwargs = pack_kwargs
        else:
            self._insert_kwargs = dict()

    # def set_target_variable(self,variable:tk.Variable) -> Self:
    #     """
    #     If you pass the target variable of this widget, you can use .value to get/set the value.
    #     Also, the value will be included in key_functions and value-dict
    #     :param variable: tkinter variable
    #     :return: The object itself for inline declaration
    #     """
    #     self._tk_target_value = variable
    #     return self
