import tkinter as tk
from collections.abc import Iterable,Callable
from dataclasses import dataclass

from SwiftGUI_LeButch import BaseElement,Frame

@dataclass
class Options_Windowwide:
    ... # Contains options for all Elements inside a window

# Windows-Class

class Window(BaseElement):
    _prev_event = None  # Most recent event (-key)
    values:dict = None  # Key:Value of all named elements

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

    def get_event_function(self,key:any=None,key_function:Callable|Iterable[Callable]=None,key_function_send_wev:bool = True)->Callable:
        """
        Returns a function that sets the event-variable accorting to key
        :param key_function_send_wev: True, if additional_function should be called
        :param key_function: Will be called additionally to the event. YOU CAN PASS MULTIPLE FUNCTIONS as a list/tuple
        :param key: If passed, main loop will return this key
        :return: Function to use as a tk-event
        """
        if (key_function is not None) and not hasattr(key_function, "__iter__"):
            key_function = (key_function,)

        def single_event():
            self.refresh_values()

            if key_function: # Call key-functions
                for fkt in key_function:
                    if key_function_send_wev:
                        fkt(self,key,self.values)
                    else:
                        fkt()

                self.refresh_values() # In case you change values with the key-functions

            if not key is None: # Call named event
                self._receive_event(key)

        return single_event

    def refresh_values(self) -> dict:
        """
        "Picks up" all values from the elements to sore them in Window.values
        :return: new values
        """
        ...
