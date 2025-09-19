import ctypes
import random
import string
import io
import tkinter as tk
from os import PathLike
from tkinter import ttk, Widget
from collections.abc import Iterable,Callable
from typing import TYPE_CHECKING, Any, Union
from SwiftGUI.Compat import Self
import inspect
from PIL import Image, ImageTk

from SwiftGUI import BaseElement, Frame, ElementFlag, Literals, GlobalOptions, Color, Debug

if TYPE_CHECKING:
    from SwiftGUI import AnyElement

class ValueDict:
    def __init__(self, window: "BaseKeyHandler", keys: set[Any]):
        super().__init__()
        self._values = dict()
        self._window: "BaseKeyHandler" = window

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

class BaseKeyHandler(BaseElement):
    """
    The base-class for anything window-ish.
    Don't use unless you absolutely know what you're doing.
    """
    all_key_elements: dict[Any, "AnyElement"]   # Key:Element, if key is present
    all_elements: list["AnyElement"] = list()   # Every single element

    exists: bool = False # True, if this window exists at the moment

    def __init__(self, event_loop_function: Callable = None):
        """

        :param event_loop_function: This function is called when a keyed event occurs. Replaces the event-loop, needs e and v as parameters.
        """
        super().__init__()

        self._value_dict: ValueDict | None = None
        self._grab_anywhere: bool | None = None
        #self.ttk_style: ttk.Style | None = None
        self.root: tk.Tk | Widget | None = None
        self._sg_widget: Frame | None = None

        self.all_elements:list["AnyElement"] = list()   # Elements will be registered in here
        self.all_key_elements:dict[any,"AnyElement"] = dict()    # Key:Element, if key is present
        self._grab_anywhere_window: Self | None = None  # This window will handle the callbacks of the grab-anywhere methods

        self._key_event_callback_function = event_loop_function
        if event_loop_function is None:
            self._key_event_callback_function = lambda *_:None

    @BaseElement._run_after_window_creation
    def set_custom_event_loop(self, key_event_callback_function: Callable) -> Self:
        """
        Specify a function/method that gets called instead of breaking out of the loop
        :param key_event_callback_function:
        :return:
        """

        self._key_event_callback_function = key_event_callback_function
        return self

    def init(
            self,
            sg_element: Frame,
            container: tk.Tk | Widget, # Container of this sub-window
            grab_anywhere_window: Self = None,
    ):
        """Should be called by the window when/after it is being created"""
        self._sg_widget: Frame = sg_element

        self.root = container

        if grab_anywhere_window is not None:
            self._grab_anywhere_window = grab_anywhere_window

        if not hasattr(self, "ttk_style"):
            self.ttk_style = ttk_style

        if not hasattr(self, "_grab_anywhere"):
            self._grab_anywhere = False

        self._sg_widget.window_entry_point(self.root, self)

        self._value_dict = ValueDict(self, set(self.all_key_elements.keys()))

        self.exists = True

        for elem in self.all_elements:
            elem.init_window_creation_done()

        self._sg_widget.init_window_creation_done()

        super().init_window_creation_done()


    def __iter__(self) -> Self:
        return self

    def __next__(self) -> tuple[any,dict[any:any]]:
        e,v = self.loop()

        if not self.exists:
            raise StopIteration

        return e,v

    def __contains__(self, item):
        return item in self.all_key_elements.keys()

    def close(self):
        """
        Kill the window
        :return:
        """
        ...

    def loop_close(self) -> tuple[Any,dict[Any:Any]]:
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
        raise NotImplementedError(f"A {self.__class__.__name__}-object can't be looped (yet).")

    def register_element(self,elem:BaseElement):
        """
        Register an Element in this window
        :param elem:
        :return:
        """
        self.all_elements.append(elem)

        if not elem.has_flag(ElementFlag.DONT_REGISTER_KEY) and elem.key is not None:
            if Debug.enable_key_warnings and elem.key in self.all_key_elements:
                print(f"WARNING! Key {elem.key} is defined multiple times in its key-system! Disable this message by setting sg.Debug.enable_key_warnings = False before creating the layout.")

            self.all_key_elements[elem.key] = elem

    def throw_event(self, key: Any = None, value: Any= None, function: Callable= None, function_args: tuple = tuple(), function_kwargs: dict = None):
        """
        Thread-safe method to generate a custom event.

        :param function_kwargs: Will be passed to function
        :param function_args: Will be passed to function
        :param function: This function will be called on the main thread
        :param key:
        :param value: If not None, it will be saved inside the value-_dict until changed
        :return:
        """
        if not self.exists:
            return

        if key is not None:
            self._value_dict.set_extra_value(key, value)

        if function_kwargs is None and function is not None:
            function_kwargs = dict()

        # Throw the event on the main window so it is thread-safe
        main_window.throw_event(function= self._receive_event, function_kwargs={
            "key": key,
            "callback": function,
            "callback_args": function_args,
            "callback_kwargs": function_kwargs,
        })

    #@deprecated("WIP")
    # Todo: def throw_event_on_next_loop(self,key:Any,value:Any=None):
    #
    #     """
    #     NOT THREAD-SAFE!!!
    #
    #     Generate an event instantly when window returns to loop
    #     :param key:
    #     :param value: If not None, it will be saved inside the value-_dict until changed
    #     :return:
    #     """
    #     raise NotImplementedError("sg.Window.throw_event_on_next_loop is not ready to use yet")

    def _receive_event(self, key:Any = None, callback: Callable = None, callback_args: tuple = tuple(), callback_kwargs: dict = None):
        """
        Gets called when an event is evoked
        :param key:
        :return:
        """
        # Call the function if given
        if callback is not None:
            if callback_kwargs is None:
                callback_kwargs = dict()

            self._value_dict.invalidate_all_values()
            callback(*callback_args, **callback_kwargs)

        # Break out of the loop if a key is given
        if key is not None:
            self._value_dict.invalidate_all_values()
            self._key_event_callback_function(key, self._value_dict)

    def get_event_function(self,me:BaseElement = None,key:Any=None,key_function:Callable|Iterable[Callable]=None,
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
                    "val": None if me is None else me.value,    # Value of element that caused the event
                    "elem": me,
                }

                for fkt in key_function:
                    wanted = set(inspect.signature(fkt).parameters.keys())
                    offers = kwargs.fromkeys(kwargs.keys() & wanted)
                    did_refresh = False

                    if fkt(**{i:kwargs[i] for i in offers}) is not None:
                        if me is not None:
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

    def _get_value(self) -> Any:
        return self._value_dict

    def set_value(self,val:Any) -> Self:
        raise NotImplementedError("You can't change the value of this element like that.")

    ### grap_anywhere methods.
    ### Mainly inspired by this post: https://stackoverflow.com/questions/4055267/tkinter-mouse-drag-a-window-without-borders-eg-overridedirect1
    _lastClickX = None
    _lastClickY = None

    def _SaveLastClickPos(self, event):
        ...

    def _DelLastClickPos(self, *_):
        ...

    def _Dragging(self, event):
        ...

    def bind_grab_anywhere_to_element(self, widget: tk.Widget) -> Self:
        """
        Add necessary bindings for window grab-and-move ("grab_anywhere") to the passed widget.
        This should be called on every widget the user should be able to grab and pull the window from.

        ONLY WORKS IF w._grab_anywhere == True

        :param widget:
        :return:
        """
        if self._grab_anywhere_window is not None:
            self._grab_anywhere_window.bind_grab_anywhere_to_element(widget)
        return Self

class SubLayout(BaseKeyHandler):
    """
    Can be used as an sg-element.
    Collects all containing keys and diverts them to a specified loop-"function"
    """

    def __init__(
            self,
            layout: Frame | Iterable[Iterable[BaseElement]],
            event_loop_function: Callable = None,
    ):
        super().__init__(event_loop_function)

        if not isinstance(layout, Frame):
            layout = Frame(layout)

        self.add_flags(ElementFlag.APPLY_PARENT_BACKGROUND_COLOR)
        self._frame = layout

    def _init(self, parent:"BaseElement", window):
        super()._init(parent, window)

        self.init(self._frame, self.parent_tk_widget, self.window)

    def _update_special_key(self,key:str,new_val:Any) -> bool|None:
        if key == "background_color":
            if self._frame.has_flag(ElementFlag.APPLY_PARENT_BACKGROUND_COLOR):
                self._frame.update(background_color = new_val)
                return True

        return super()._update_special_key(key, new_val)

ttk_style: ttk.Style | None = None
main_window: Union["Window", None] = None
all_decorator_key_functions = dict() # All decorator-functions collected, key: function
class Window(BaseKeyHandler):
    """
    Main Window-object.
    Don't use for "second" windows
    """

    _prev_event:any = None  # Most recent event (-key)
    defaults = GlobalOptions.Window

    @staticmethod
    def _make_taskbar_icon_changeable(title: str = None):
        myappid = "SwiftGUI." + "".join(random.choices(string.ascii_letters, k=8))
        if title:
            myappid += "." + title

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    def __init__(
            self,
            layout:Iterable[Iterable[BaseElement]],
            /,
            title:str = None,
            alignment: Literals.alignment = None,
            titlebar: bool = None,  # Titlebar visible
            resizeable_width: bool = None,
            resizeable_height: bool = None,
            transparency: Literals.transparency = None,  # 0-1, 1 meaning invisible
            size: int | tuple[int, int] = (None, None),
            position: tuple[int, int] = (None, None),  # Position on monitor # Todo: Center
            min_size: int | tuple[int, int] = (None, None),
            max_size: int | tuple[int, int] = (None, None),
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
        :param transparency: 0 - 1, with 1 being invisible, 0 fully visible
        :param size: Size of the window in pixels. Leave this blank to determine this automatically
        :param position: Position of the upper left corner of the window
        :param min_size: Minimal size of the window, when the user can resize it
        :param max_size: Maximum size of the window, when the user can resize it
        :param icon: Icon of the window. Has to be .ico
        :param keep_on_top: True, if the window should always be on top of any other window
        :param grab_anywhere: True, if the window can be "held and dragged" anywhere (exclusing certain elements)
        """
        global ttk_style
        global main_window

        self._make_taskbar_icon_changeable(title)

        if main_window is None or not main_window.exists: # Some users might use sg.Window for popups, don't overwrite the global in that case
            ttk_style = None
            main_window = self

        super().__init__(event_loop_function=self._keyed_event_callback)
        self._grab_anywhere = self.defaults.single("grab_anywhere", grab_anywhere)

        self._sg_widget:Frame = Frame(layout,alignment= self.defaults.single("alignment", alignment), expand_y=True, expand=True)
        self.root = tk.Tk()
        self.ttk_style: ttk.Style = ttk.Style(self.root)

        if ttk_style is None:
            ttk_style = self.ttk_style

        self.window = self
        self._update_initial(
            title=title,
            titlebar=titlebar,
            resizeable_width=resizeable_width,
            resizeable_height=resizeable_height,
            transparency=transparency,
            size=size,
            position=position,
            min_size=min_size,
            max_size=max_size,
            icon=icon,
            keep_on_top=keep_on_top,
            background_color=background_color,
            ttk_theme=ttk_theme,
        )

        self.init(self._sg_widget, self.root, grab_anywhere_window= self)

        self.bind_grab_anywhere_to_element(self._sg_widget.tk_widget)

        if position == (None, None):
            self.center()

        self._decorated_key_functions = dict()
        for key, val in all_decorator_key_functions.items():
            self._decorated_key_functions[key] = self.get_event_function(key= key, key_function= val)

    _resizeable_width = False
    _resizeable_height = False
    def _update_special_key(self, key:str, new_val:Any) -> bool|None:
        # if not self.window.has_flag(ElementFlag.IS_CREATED) and key in ["fullscreen"]:
        #     self.update_after_window_creation(**{key: new_val})
        #     return True

        match key:
            case "title":
                if new_val is not None:
                    self.root.title(new_val)
            case "titlebar":
                if new_val is not None:
                    self.root.overrideredirect(not new_val)
            case "resizeable_width":
                if new_val is None:
                    return True
                self._resizeable_width = new_val
                self.root.resizable(new_val, self._resizeable_height)
            case "resizeable_height":
                if new_val is None:
                    return True
                self._resizeable_height = new_val
                self.root.resizable(self._resizeable_width, new_val)
            case "fullscreen":
                if new_val is None:
                    return True
                self.root.state("zoomed" if new_val else "normal")
            case "transparency":
                if new_val is not None:
                    assert 0 <= new_val <= 1, "Window-Transparency must be between 0 and 1"
                    self.root.attributes("-alpha", 1 - new_val)
            case "size":
                if new_val is None:
                    return True

                if isinstance(new_val, int):
                    new_val = (new_val, new_val)

                geometry = ""
                if new_val[0]:
                    assert new_val[1], "Window-width was specified, but not its height"
                    geometry += str(new_val[0])
                if new_val[1]:
                    assert new_val[0], "Window-height was specified, but not its width"
                    geometry += f"x{new_val[1]}"

                if geometry:
                    self.root.geometry(geometry)
            case "position":
                if new_val is None:
                    return True

                geometry = ""
                if new_val != (None, None):
                    assert len(new_val) == 2, "The window-position should be a tuple with x and y coordinate: (x, y)"
                    assert new_val[0] is not None, "No x-coordinate was given as window-position"
                    assert new_val[1] is not None, "No y-coordinate was given as window-position"

                    geometry += f"+{int(new_val[0])}+{int(new_val[1])}".replace("+-", "-")
                    self.root.geometry(geometry)

            case "min_size":
                if new_val is None:
                    return True
                if isinstance(new_val, int):
                    new_val = (new_val, new_val)
                if new_val != (None, None):
                    self.root.minsize(*new_val)
            case "max_size":
                if new_val is None:
                    return True
                if isinstance(new_val, int):
                    new_val = (new_val, new_val)
                if new_val != (None, None):
                    self.root.maxsize(*new_val)
            case "icon":
                if new_val is not None:
                    self.update_icon(new_val)
            case "keep_on_top":
                if new_val is not None:
                    self.root.attributes("-topmost", new_val)
            case "background_color":
                if new_val is not None:
                    self._sg_widget._update_initial(background_color=new_val)
            case "ttk_theme":
                if new_val is not None:
                    self.ttk_style.theme_use(new_val)
            case _:
                return False

        return True

    def update(
            self,
            title = None,
            titlebar: bool = None,  # Titlebar visible
            resizeable_width: bool = None,
            resizeable_height: bool = None,
            fullscreen: bool = None,
            transparency: Literals.transparency = None,  # 0-1, 1 meaning invisible
            size: int | tuple[int, int] = (None, None),
            position: tuple[int, int] = (None, None),  # Position on monitor # Todo: Center
            min_size: int | tuple[int, int] = (None, None),
            max_size: int | tuple[int, int] = (None, None),
            icon: str | PathLike | Image.Image | io.BytesIO = None,  # .ico file
            keep_on_top: bool = None,
            background_color: Color | str = None,
            ttk_theme: str = None,
    ):
        super().update(
            title = title,
            titlebar = titlebar,
            resizeable_width = resizeable_width,
            resizeable_height = resizeable_height,
            fullscreen = fullscreen,
            transparency = transparency,
            size = size,
            position = position,
            min_size = min_size,
            max_size = max_size,
            icon = icon,
            keep_on_top = keep_on_top,
            background_color = background_color,
            ttk_theme = ttk_theme,
        )

        return self

    # @BaseElement._run_after_window_creation
    # def _update_initial(self,**kwargs) -> Self:
    #     super()._update_initial(**kwargs)
    #     return self

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

    def loop(self) -> tuple[Any, ValueDict]:
        """
        Main loop

        When window is closed, None is returned as the key.

        :return: Triggering event key; all values as _dict
        """
        self.exists = True

        while True:
            self.root.mainloop()

            try:
                assert self.root.winfo_exists()
            except (AssertionError,tk.TclError):
                self.exists = False # This looks redundant, but it's easier to use self.exists from outside. So leave it!
                self.remove_flags(ElementFlag.IS_CREATED)
                return None,self._value_dict

            self._value_dict.invalidate_all_values()

            # decorator-keys
            if self._prev_event in self._decorated_key_functions:
                self._decorated_key_functions[self._prev_event]()
                continue    # Go on looping, key is handled

            break   # Actually escape the loop

        return self._prev_event, self._value_dict

    def throw_event(self, key: Any = None, value: Any= None, function: Callable= None, function_args: tuple = tuple(), function_kwargs: dict = None):
        """
        Thread-safe method to generate a custom event.

        :param function_kwargs: Will be passed to function
        :param function_args: Will be passed to function
        :param function: This function will be called on the main thread
        :param key:
        :param value: If not None, it will be saved inside the value-_dict until changed
        :return:
        """
        if not self.exists:
            return

        if key is not None:
            self._value_dict.set_extra_value(key, value)

        if function_kwargs is None and function is not None:
            function_kwargs = dict()

        self.root.after(0, self._receive_event, key, function, function_args, function_kwargs)

    def _keyed_event_callback(self, key: Any, _):
        self._prev_event = key
        self.root.quit()

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
    def center(self) -> Self:
        """
        Centers the window on the current screen
        :return:
        """
        self.root.eval("tk::PlaceWindow . center")
        return self

    @BaseElement._run_after_window_creation
    def bind_grab_anywhere_to_element(self, widget: tk.Widget):
        """
        Add necessary bindings for window grab-and-move ("grab_anywhere") to the passed widget.
        This should be called on every widget the user should be able to grab and pull the window from.

        ONLY WORKS IF w._grab_anywhere == True

        :param widget:
        :return:
        """
        if self._grab_anywhere:
            # Disable bindings if not necessary, for performance reasons
            # The downside is that it can't be enabled later on.

            widget.bind('<ButtonPress-1>', self._SaveLastClickPos)
            widget.bind('<ButtonRelease-1>', self._DelLastClickPos)
            widget.bind('<B1-Motion>', self._Dragging)