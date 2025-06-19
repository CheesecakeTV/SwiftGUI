import tkinter as tk
from collections.abc import Iterable

from SwiftGUI_LeButch import BaseElement,Key,Frame


# Windows-Class

class Window(BaseElement):
    def __init__(self,layout:Iterable[Iterable[BaseElement]]):
        self._tk = tk.Tk()
        self._sg_widget:Frame

        self._sg_widget = Frame(layout)
        self._sg_widget.window_entry_point(self._tk)

    def _init(self,parent:None=None):
        self.parent = self  # A window refers to itself, because why not

    @property
    def tk_widget(self) ->tk.Widget:
        return self._sg_widget.tk_widget

    def loop(self) -> any:
        """
        Main loop
        :return: Triggering event key
        """
        self._tk.mainloop()
        return None



