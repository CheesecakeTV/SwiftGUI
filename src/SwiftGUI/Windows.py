import tkinter as tk
from collections.abc import Iterable,Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING
from warnings import deprecated
import inspect

from SwiftGUI import BaseElement, Frame

if TYPE_CHECKING:
    from SwiftGUI import AnyElement


@deprecated("WIP")
@dataclass
class Options_Windowwide:
    ... # Contains options for all Elements inside a window

# Windows-Class

class Window(BaseElement):
    _prev_event:any = None  # Most recent event (-key)
    values:dict  # Key:Value of all named elements

    all_key_elements: dict[any, "AnyElement"]   # Key:Element, if key is present

    exists:bool = False # True, if this window exists at the moment

    global_options = dict() # Standard-Values for options

    def __init__(
            self,
            layout:Iterable[Iterable[BaseElement]],
            # global_options:dict[str:str] = None, # Todo: This conflicts with other global-options
    ):
        """

        :param layout:
        # :param global_options: Options applied to every element in the window
        """
        self.all_elements:list["AnyElement"] = list()   # Elemente will be registered in here
        self.all_key_elements:dict[any,"AnyElement"] = dict()    # Key:Element, if key is present
        self.values = dict()

        self._tk = tk.Tk()


        # if global_options:
        #     for key,val in global_options.items():
        #         if not (key.startswith("*") or "." in key):
        #             key = "*" + key
        #
        #         self._tk.option_add(key,val,priority=1)


        self._sg_widget:Frame = Frame(layout)
        self._sg_widget.window_entry_point(self._tk, self)

        self.refresh_values()

    @property
    def tk_widget(self) ->tk.Widget:
        return self._sg_widget.tk_widget

    def loop(self) -> tuple[any,dict[any:any]]:
        """
        Main loop

        When window is closed, None is returned as the key.

        :return: Triggering event key; all values as dict
        """
        self.exists = True
        self._tk.mainloop()

        try:
            assert self._tk.winfo_exists()
        except (AssertionError,tk.TclError):
            self.exists = False
            return None,self.values

        return self._prev_event, self.values

    def register_element(self,elem:BaseElement):
        """
        Register an Element in this window
        :param elem:
        :return:
        """
        self.all_elements.append(elem)

        if elem.key is not None:
            if elem.key in self.all_key_elements:
                print(f"WARNING! Key {elem.key} is defined multiple times!")

            self.all_key_elements[elem.key] = elem

    def throw_event(self,key:any,value:any=None):
        """
        Thread-safe method to generate a custom event.

        :param key:
        :param value: If not None, it will be saved inside the value-dict until changed
        :return:
        """
        if value is not None:
            self.values[key] = value
        self._tk.after(0,self._receive_event,key)

    @deprecated("WIP")
    def throw_event_on_next_loop(self,key:any,value:any=None):
        """
        NOT THREAD-SAFE!!!

        Generate an event instantly when window returns to loop
        :param key:
        :param value: If not None, it will be saved inside the value-dict until changed
        :return:
        """
        # Todo
        ...

    def _receive_event(self,key:any):
        """
        Gets called when an event is evoked
        :param key:
        :return:
        """
        self._prev_event = key
        self._tk.quit()

    def get_event_function(self,me:BaseElement,key:any=None,key_function:Callable|Iterable[Callable]=None,
                           )->Callable:
        """
        Returns a function that sets the event-variable accorting to key
        :param me: Calling element
        :param key_function: Will be called additionally to the event. YOU CAN PASS MULTIPLE FUNCTIONS as a list/tuple
        :param key: If passed, main loop will return this key
        :return: Function to use as a tk-event
        """
        if (key_function is not None) and not hasattr(key_function, "__iter__"):
            key_function = (key_function,)

        def single_event(*_):
            self.refresh_values()

            if key_function: # Call key-functions
                kwargs = {  # Possible parameters for function
                    "w": self,  # Reference to main window
                    "e": key,   # Event-key, if there is one
                    "v": self.values,   # All values
                    "val": me.value,    # Value of element that caused the event
                    "elem": me,
                }

                for fkt in key_function:
                    wanted = set(inspect.signature(fkt).parameters.keys())
                    offers = kwargs.fromkeys(kwargs.keys() & wanted)

                    fkt(**{i:kwargs[i] for i in offers})

                self.refresh_values() # In case you change values with the key-functions

            if key is not None: # Call named event
                self._receive_event(key)

        return single_event

    def refresh_values(self) -> dict:
        """
        "Picks up" all values from the elements to store them in Window.values
        :return: new values
        """
        for key,elem in self.all_key_elements.items():
            self.values[key] = elem.value

        return self.values

    def __getitem__(self, item) -> "AnyElement":
        try:
            return self.all_key_elements[item]
        except KeyError:
            raise KeyError(f"The requested Element ({item}) wasn't found. Did you forget to set its key?")
