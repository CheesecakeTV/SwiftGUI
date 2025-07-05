import tkinter as tk
from collections.abc import Iterable,Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Self, Literal
from warnings import deprecated
import inspect

from SwiftGUI import BaseElement, Frame, ElementFlag, Literals

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
    all_elements: list["AnyElement"] = list()   # Every single element

    exists:bool = False # True, if this window exists at the moment

    global_options = dict() # Standard-Values for options

    def __init__(
            self,
            layout:Iterable[Iterable[BaseElement]],
            title = "Some awesome SwiftGUI Window",
            # global_options:dict[str:str] = None, # Todo: This conflicts with other global-options
            alignment: Literals.alignment = None,
            titlebar:bool = True,   # Titlebar visible
            resizeable_width = False,
            resizeable_height = False,
            fullscreen:bool = False,
            transparency:Literals.transparency = 0, # 0-1, 1 meaning invisible
            size:tuple[int,int] = (None,None),
            position:tuple[int,int] = (None,None),  # Position on monitor
            min_size:tuple[int,int] = (None,None),
            max_size: tuple[int, int] = (None, None),
            icon:str = None,    # .ico file
            keep_on_top: bool = False,
    ):
        """

        :param layout:
        # :param global_options: Options applied to every element in the window
        """
        self.all_elements:list["AnyElement"] = list()   # Elements will be registered in here
        self.all_key_elements:dict[any,"AnyElement"] = dict()    # Key:Element, if key is present
        self.values = dict()

        self._tk = tk.Tk()

        self.update(title,titlebar, resizeable_width, resizeable_height, fullscreen, transparency, size, position, min_size, max_size, icon, keep_on_top)

        self._sg_widget:Frame = Frame(layout,alignment=alignment)
        self._sg_widget.window_entry_point(self._tk, self)

        for elem in self.all_elements:
            elem.init_window_creation_done()

        self.refresh_values()

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> tuple[any,dict[any:any]]:
        e,v = self.loop()

        if not self.exists:
            raise StopIteration

        return e,v

    def update(
            self,
            title = None,
            titlebar: bool = True,  # Titlebar visible
            resizeable_width=False,
            resizeable_height=False,
            fullscreen: bool = False,
            transparency: Literals.transparency = 0,  # 0-1, 1 meaning invisible
            size: tuple[int, int] = (None, None),
            position: tuple[int, int] = (None, None),  # Position on monitor # Todo: Center
            min_size: tuple[int, int] = (None, None),
            max_size: tuple[int, int] = (None, None),
            icon: str = None,  # .ico file
            keep_on_top: bool = False,
    ):
        self._tk.title(title)

        self._tk.overrideredirect(not titlebar)

        self._tk.resizable(resizeable_width,resizeable_height)
        self._tk.state("zoomed" if fullscreen else "normal")

        assert 0 <= transparency <= 1, "Window-Transparency must be between 0 and 1"
        self._tk.attributes("-alpha",1 - transparency)

        geometry = ""
        if size[0]:
            assert size[1], "Window-height was specified, but not its height"
            geometry += str(size[0])
        if size[1]:
            assert size[0], "Window-height was specified, but not its width"
            geometry += f"x{size[1]}"

        # if position == "center":
        #     position = (
        #         self._tk.winfo_screenwidth() / 2 - self._tk.winfo_width() / 2,
        #         self._tk.winfo_screenheight() / 2 - self._tk.winfo_height()
        #     )
        if position != (None,None):
            assert len(position) == 2, "The window-position should be a tuple with x and y coordinate: (x, y)"
            assert position[0] is not None, "No x-coordinate was given as window-position"
            assert position[1] is not None, "No y-coordinate was given as window-position"

            geometry += f"+{int(position[0])}+{int(position[1])}".replace("+-","-")

        if geometry:
            self._tk.geometry(geometry)

        self._tk.minsize(*min_size)
        self._tk.maxsize(*max_size)

        assert icon is None or icon.endswith(".ico"), "The window-icon has to be the path to a .ico-file. Other filetypes are not supported."
        self._tk.iconbitmap(icon)

        self._tk.attributes("-topmost",keep_on_top)

    @property
    def parent_tk_widget(self) ->tk.Widget:
        return self._sg_widget.parent_tk_widget

    def close(self):
        """
        Kill the window
        :return:
        """
        if self.has_flag(ElementFlag.IS_CREATED):
            self._tk.destroy()

    def loop_close(self) -> tuple[any,dict[any:any]]:
        """
        Loop once, then close
        :return:
        """
        e,v = self.loop()
        self.close()
        return e,v

    def loop(self) -> tuple[any,dict[any:any]]:
        """
        Main loop

        When window is closed, None is returned as the key.

        :return: Triggering event key; all values as _dict
        """
        self.exists = True
        self._tk.mainloop()

        try:
            assert self._tk.winfo_exists()
        except (AssertionError,tk.TclError):
            self.exists = False # This looks redundant, but it's easier to use self.exists from outside. So leave it!
            self.remove_flags(ElementFlag.IS_CREATED)
            return None,self.values

        return self._prev_event, self.values

    def register_element(self,elem:BaseElement):
        """
        Register an Element in this window
        :param elem:
        :return:
        """
        self.all_elements.append(elem)

        if not elem.has_flag(ElementFlag.DONT_REGISTER_KEY) and elem.key is not None:
            if elem.key in self.all_key_elements:
                print(f"WARNING! Key {elem.key} is defined multiple times!")

            self.all_key_elements[elem.key] = elem

    def throw_event(self,key:any,value:any=None):
        """
        Thread-safe method to generate a custom event.

        :param key:
        :param value: If not None, it will be saved inside the value-_dict until changed
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
        :param value: If not None, it will be saved inside the value-_dict until changed
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
