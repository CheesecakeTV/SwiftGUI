import tkinter as tk
from collections.abc import Iterable

from SwiftGUI_LeButch import BaseElement,Key,Frame


# Windows-Class

class Window(BaseElement):
    _prev_event = None  # Most recent event (-key)
    values:dict = None  # Key:Value of all elements

    def __init__(self,layout:Iterable[Iterable[BaseElement]]):
        self.allElements = list()   # Elemente will be registered in here
        self.values = dict()

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
        return self._prev_event

    def register_element(self,elem:BaseElement):
        """
        Register an Element in this window
        :param elem:
        :return:
        """
        self.allElements.append(elem)

    def throw_event(self,key:any,value:any=None):
        """
        Thread-safe method to generate a custom event.

        :param key:
        :param value: Will be saved inside the value-dict until changed
        :return:
        """
        self.values[key] = value
        self._tk.after(0,self._receive_event,key)

    def _receive_event(self,key:any):
        """
        Gets called when an event is evoked
        :param key:
        :return:
        """
        self._prev_event = key
        print("Event:",key)
        self._tk.quit()

    def get_event_function(self,key:any)->callable:
        """
        Returns a function that sets the event-variable accorting to key
        :param key:
        :return:
        """

        def single_event():
            self._receive_event(key)

        return single_event
