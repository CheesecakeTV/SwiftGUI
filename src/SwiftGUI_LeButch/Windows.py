import tkinter as tk
from collections.abc import Iterable

from SwiftGUI_LeButch import BaseElement,Key,Frame


# Windows-Class

class Window(BaseElement):
    def __init__(self,layout:Iterable[Iterable[BaseElement]]):
        self.allElements = list()   # Elemente will be registered in here

        self._tk = tk.Tk()
        self._sg_widget:Frame

        self._sg_widget = Frame(layout)
        self._sg_widget.window_entry_point(self._tk, self)

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

    def register_element(self,elem:BaseElement):
        """
        Register an Element in this window
        :param elem:
        :return:
        """
        self.allElements.append(elem)



