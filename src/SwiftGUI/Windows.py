import io
import tkinter as tk
from os import PathLike
from tkinter import ttk
from collections.abc import Iterable,Callable
from typing import TYPE_CHECKING, Self, Any
import inspect
from PIL import Image, ImageTk

from SwiftGUI import BaseElement, Frame, ElementFlag, Literals, GlobalOptions, Color, Debug

if TYPE_CHECKING:
    from SwiftGUI import AnyElement

class ValueDict:
    def __init__(self, window: "Window", keys: set[Any]):
        super().__init__()
        self._values = dict()
        self._window: "Window" = window

        self._updated_keys: set = set()
        self._all_keys: set = keys

    def __getitem__(self, item: Any) -> Any:
        if item in self._updated_keys:
            return self._values[item]

        if item in self._window:
            self.refresh_key(item)

        return self._values[item]

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def __setitem__(self, key: Any, value: Any):
        try:
            self._window[key].value = value
        except KeyError:
            pass

        self._values[key] = value
        self._updated_keys.add(key)

    def refresh_key(self, *key: Any) -> Self:
        """
        Refresh a single key
        :param key:
        :return:
        """
        for k in key:
            self._values[k] = self._window[k].value
            self._updated_keys.add(k)

        return self

    def refresh_all(self) -> Self:
        """
        Refreshes all keys with their current values
        :return:
        """
        map(self.refresh_key, self._all_keys)

        return self

    def invalidate_all_values(self) -> Self:
        """
        Called after every loop
        :return:
        """
        #self.refresh_all()
        self._updated_keys.clear()
        return self

    @property
    def _not_updated_keys(self):
        return self._all_keys.symmetric_difference(self._updated_keys)

    def __str__(self) -> str:
        self.refresh_key(*self._not_updated_keys)
        return str(self._values)

    def __repr__(self):
        self.refresh_key(*self._not_updated_keys)
        return repr(self._values)

    def set_extra_value(self, key: Any, value: Any) -> Self:
        """
        Set a value that is not included in the actual window (like from threads)
        :param key:
        :param value:
        :return:
        """
        self._values[key] = value
        return self

    def update(self, vals: dict[Any:Any]) -> Self:
        """
        Apply all values from the provided dict
        :param vals:
        :return:
        """
        for key, val in vals.items():
            self.__setitem__(key, val)
        return self

class Window(BaseElement):
    _prev_event:any = None  # Most recent event (-key)

    all_key_elements: dict[Any, "AnyElement"]   # Key:Element, if key is present
    all_elements: list["AnyElement"] = list()   # Every single element

    exists:bool = False # True, if this window exists at the moment

    defaults = GlobalOptions.Window

    def __init__(
            self,
            layout:Iterable[Iterable[BaseElement]],
            /,
            title:str = None,
            alignment: Literals.alignment = None,
            titlebar: bool = None,  # Titlebar visible
            resizeable_width=None,
            resizeable_height=None,
            fullscreen: bool = None,
            transparency: Literals.transparency = None,  # 0-1, 1 meaning invisible
            size: tuple[int, int] = (None, None),
            position: tuple[int, int] = (None, None),  # Position on monitor # Todo: Center
            min_size: tuple[int, int] = (None, None),
            max_size: tuple[int, int] = (None, None),
            icon: str | PathLike | Image.Image | io.BytesIO = None,  # .ico file
            keep_on_top: bool = None,
            background_color: Color | str = None,
            grab_anywhere: bool = None,
            ttk_theme: str = None,
    ):
        """

        :param layout: Double-List (or other iterable) of your elements, row by row
        :param title: Window-title (seen in titlebar)
        :param alignment: How the elements inside the main layout should be aligned
        :param titlebar: False, if you want the window to have no titlebar
        :param resizeable_width: True, if you want the user to be able to resize the window's width
        :param resizeable_height: True, if you want the user to be able to resize the window's height
        :param fullscreen: True, if the window should be in window-fullscreen mode
        :param transparency: 0 - 1, with 1 being invisible, 0 fully visible
        :param size: Size of the window in pixels. Leave this blank to determine this automatically
        :param position: Position of the upper left corner of the window
        :param min_size: Minimal size of the window, when the user can resize it
        :param max_size: Maximum size of the window, when the user can resize it
        :param icon: Icon of the window. Has to be .ico
        :param keep_on_top: True, if the window should always be on top of any other window
        :param grab_anywhere: True, if the window can be "held and dragged" anywhere (exclusing certain elements)
        """
        super().__init__()
        self.all_elements:list["AnyElement"] = list()   # Elements will be registered in here
        self.all_key_elements:dict[any,"AnyElement"] = dict()    # Key:Element, if key is present
        self._grab_anywhere = self.defaults.single("grab_anywhere", grab_anywhere)

        self.root = tk.Tk()

        self._sg_widget:Frame = Frame(layout,alignment=alignment)

        self.ttk_style: ttk.Style = ttk.Style(self.root)
        self._update_initial(
            title=title,
            titlebar=titlebar,
            resizeable_width=resizeable_width,
            resizeable_height=resizeable_height,
            fullscreen=fullscreen,
            transparency=transparency,
            size=size,
            position=position,
            min_size=min_size,
            max_size=max_size,
            icon=icon,
            keep_on_top=keep_on_top,
            background_color=background_color,
            ttk_theme=ttk_theme,
            _first_update=True
        )

        self._sg_widget.window_entry_point(self.root, self)
        self._config_ttk_queue = list()

        for elem in self.all_elements:
            elem.init_window_creation_done()
        self.init_window_creation_done()
        self._sg_widget.init_window_creation_done()

        self._value_dict = ValueDict(self, set(self.all_key_elements.keys()))

        self.bind_grab_anywhere_to_element(self._sg_widget.tk_widget)


    def __iter__(self) -> Self:
        return self

    def __next__(self) -> tuple[any,dict[any:any]]:
        e,v = self.loop()

        if not self.exists:
            raise StopIteration

        return e,v

    # Todo: This need to be changed to new routine
    def _update_initial(
            self,
            title = None,
            titlebar: bool = None,  # Titlebar visible
            resizeable_width=None,
            resizeable_height=None,
            fullscreen: bool = None,
            transparency: Literals.transparency = None,  # 0-1, 1 meaning invisible
            size: tuple[int, int] = (None, None),
            position: tuple[int, int] = (None, None),  # Position on monitor # Todo: Center
            min_size: tuple[int, int] = (None, None),
            max_size: tuple[int, int] = (None, None),
            icon: str | PathLike | Image.Image | io.BytesIO = None,  # .ico file
            keep_on_top: bool = None,
            background_color: Color | str = None,
            ttk_theme: str = None,
            _first_update: bool = False,
    ):
        # Todo: This method needs to be put in proper shape
        if _first_update:
            title = self.defaults.single("title",title)
            titlebar = self.defaults.single("titlebar",titlebar)
            resizeable_width = self.defaults.single("resizeable_width",resizeable_width)
            resizeable_height = self.defaults.single("resizeable_height",resizeable_height)
            fullscreen = self.defaults.single("fullscreen",fullscreen)
            transparency = self.defaults.single("transparency",transparency)
            size = self.defaults.single("size",size)
            position = self.defaults.single("position",position)
            min_size = self.defaults.single("min_size",min_size)
            max_size = self.defaults.single("max_size",max_size)
            icon = self.defaults.single("icon",icon)
            keep_on_top = self.defaults.single("keep_on_top",keep_on_top)
            background_color = self.defaults.single("background_color",background_color)
            ttk_theme = self.defaults.single("ttk_theme", ttk_theme)

        if ttk_theme:
            self.ttk_style.theme_use(ttk_theme)

        if background_color is not None:
            self._sg_widget._update_initial(background_color=background_color)

        if title is not None:
            self.root.title(title)

        if titlebar is not None:
            self.root.overrideredirect(not titlebar)

        self.root.resizable(resizeable_width, resizeable_height)
        self.root.state("zoomed" if fullscreen else "normal")

        if transparency is not None:
            assert 0 <= transparency <= 1, "Window-Transparency must be between 0 and 1"
            self.root.attributes("-alpha", 1 - transparency)

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
            self.root.geometry(geometry)

        if min_size != (None,None):
            self.root.minsize(*min_size)

        if max_size != (None,None):
            self.root.maxsize(*max_size)

        # assert icon is None or icon.endswith(".ico"), "The window-icon has to be the path to a .ico-file. Other filetypes are not supported."
        # self.root.iconbitmap(icon)
        if icon is not None:
            self.update_icon(icon)

        if keep_on_top is not None:
            self.root.attributes("-topmost", keep_on_top)

        return self

    def __contains__(self, item):
        return item in self.all_key_elements.keys()

    @property
    def parent_tk_widget(self) ->tk.Widget:
        return self._sg_widget.parent_tk_widget

    def close(self):
        """
        Kill the window
        :return:
        """
        if self.has_flag(ElementFlag.IS_CREATED):
            self.root.destroy()

    def loop_close(self) -> tuple[any,dict[any:any]]:
        """
        Loop once, then close
        :return:
        """
        e,v = self.loop()
        self.close()
        return e,v

    def loop(self) -> tuple[Any, ValueDict]:
        """
        Main loop

        When window is closed, None is returned as the key.

        :return: Triggering event key; all values as _dict
        """
        self.exists = True
        self.root.mainloop()

        try:
            assert self.root.winfo_exists()
        except (AssertionError,tk.TclError):
            self.exists = False # This looks redundant, but it's easier to use self.exists from outside. So leave it!
            self.remove_flags(ElementFlag.IS_CREATED)
            return None,self._value_dict

        self._value_dict.invalidate_all_values()
        return self._prev_event, self._value_dict

    def register_element(self,elem:BaseElement):
        """
        Register an Element in this window
        :param elem:
        :return:
        """
        self.all_elements.append(elem)

        if not elem.has_flag(ElementFlag.DONT_REGISTER_KEY) and elem.key is not None:
            if Debug.enable_key_warnings and elem.key in self.all_key_elements:
                print(f"WARNING! Key {elem.key} is defined multiple times! Disable this message by setting sg.Debug.enable_key_warnings = False before creating the layout.")

            self.all_key_elements[elem.key] = elem

    def throw_event(self,key:any,value:any=None):
        """
        Thread-safe method to generate a custom event.

        :param key:
        :param value: If not None, it will be saved inside the value-_dict until changed
        :return:
        """
        if not self.exists:
            return

        #if value is not None:
            #self.values[key] = value
        self._value_dict.set_extra_value(key, value)
        self.root.after(0, self._receive_event, key)

    #@deprecated("WIP")
    def throw_event_on_next_loop(self,key:any,value:any=None):
        """
        NOT THREAD-SAFE!!!

        Generate an event instantly when window returns to loop
        :param key:
        :param value: If not None, it will be saved inside the value-_dict until changed
        :return:
        """
        # Todo
        raise NotImplementedError("sg.Window.throw_event_on_next_loop is not ready to use yet")

    def _receive_event(self,key:any):
        """
        Gets called when an event is evoked
        :param key:
        :return:
        """
        self._prev_event = key
        self.root.quit()

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
            did_refresh = False

            if key_function: # Call key-functions
                self.refresh_values()

                kwargs = {  # Possible parameters for function
                    "w": self,  # Reference to main window
                    "e": key,   # Event-key, if there is one
                    "v": self._value_dict,   # All values
                    "val": me.value,    # Value of element that caused the event
                    "elem": me,
                }

                for fkt in key_function:
                    wanted = set(inspect.signature(fkt).parameters.keys())
                    offers = kwargs.fromkeys(kwargs.keys() & wanted)
                    did_refresh = False

                    if fkt(**{i:kwargs[i] for i in offers}) is not None:
                        kwargs["val"] = me.value
                        self._value_dict.invalidate_all_values()
                        did_refresh = True

                if not did_refresh:
                    self._value_dict.invalidate_all_values()
                    did_refresh = True

            if key is not None: # Call named event
                if not did_refresh: # Not redundant, keep it!
                    self._value_dict.invalidate_all_values()

                self._receive_event(key)

        return single_event

    def refresh_values(self) -> ValueDict:
        """
        Invalidate all values from the value-dict so they will be refreshed the next time they are accessed
        :return: new values
        """
        self._value_dict.invalidate_all_values()

        return self._value_dict

    def __getitem__(self, item) -> "AnyElement":
        try:
            return self.all_key_elements[item]
        except KeyError:
            raise KeyError(f"The requested Element ({item}) wasn't found. Did you forget to set its key?")

    _icon = None
    def update_icon(self, icon: str | PathLike | Image.Image | io.BytesIO) -> Self:
        """
        Change the icon.
        Same as .update(icon = ...)

        :param icon:
        :return:
        """


        if not isinstance(icon, Image.Image):
            self._icon = Image.open(icon)
        else:
            self._icon = icon

        self._icon: Any | str = ImageTk.PhotoImage(self._icon)  # Typehint is just so the typechecker doesn't get annoying
        self.root.iconphoto(True, self._icon)

        return self

    ### grap_anywhere methods.
    ### Mainly inspired by this post: https://stackoverflow.com/questions/4055267/tkinter-mouse-drag-a-window-without-borders-eg-overridedirect1
    _lastClickX = None
    _lastClickY = None

    def _SaveLastClickPos(self, event):
        self._lastClickX = event.x
        self._lastClickY = event.y

    def _DelLastClickPos(self, *_):
        """Delete the click position, so the window doesn't move when clicking other elements"""
        self._lastClickX = None
        self._lastClickY = None

    def _Dragging(self, event):
        if self._lastClickX is None:
            return

        x, y = event.x - self._lastClickX + self.root.winfo_x(), event.y - self._lastClickY + self.root.winfo_y()
        self.root.geometry("+%s+%s" % (x , y))

    @BaseElement._run_after_window_creation
    def bind_grab_anywhere_to_element(self, widget: tk.Widget):
        """
        Add necessary bindings for window grab-and-move ("grab_anywhere") to the passed widget
        :param widget:
        :return:
        """
        if self._grab_anywhere:
            # Disable bindings if not necessary, for performance reasons
            # The downside is that it can't be enabled later on.

            widget.bind('<ButtonPress-1>', self._SaveLastClickPos)
            widget.bind('<ButtonRelease-1>', self._DelLastClickPos)
            widget.bind('<B1-Motion>', self._Dragging)
