from collections.abc import Iterable, Callable
from functools import wraps
from typing import Literal, Self, Union
import tkinter as tk

from SwiftGUI import Event, GlobalOptions, Color
from SwiftGUI.ElementFlags import ElementFlag

def run_after_window_creation(w_fkt: Callable) -> Callable:
    """
    Decorated methods will run if the window exists.
    Only use on methods, not functions!

    If you call it before, the call will be buffered and ran later.
    :return: If the decorated function doesn't execute, Self is returned for inline calls.
    """
    buffer: list[tuple[tuple, dict]] = list()

    def run_after():    # Actually run the functions
        nonlocal buffer
        for args,kwargs in buffer:
            w_fkt(*args, **kwargs)

        buffer = list() # Not needed anymore

    @wraps(w_fkt)
    def fkt(*args, **kwargs):
        self = args[0]

        if self.has_flag(ElementFlag.IS_CREATED):    # Window is already created
            return w_fkt(*args, **kwargs)

        if not buffer:  # If this is the first buffered call
            self._run_when_window_exists.append(run_after)  # Tell the element to call run_after, after window is created

        buffer.append((args, kwargs))
        return self

    return fkt


class BaseElement:
    """
    Base for every element and widget.

    The different to BaseWidget is that BaseWidget is designed for a single tk-Widget.
    BaseElement allows you to do whatever the f you want, it's just a class pattern.
    """
    parent:Self = None  # next higher Element
    _fake_tk_element:tk.Widget = None   # This gets returned when parent is None
    _element_flags:set[ElementFlag] # Properties the element has
    window = None # Main Window

    key:any = None  # If given, this will be written to the event-value. Elements without a key can not throw key-events
    _key_function: Callable | Iterable[Callable] = None  # Called as an event

    defaults:type[GlobalOptions.DEFAULT_OPTIONS_CLASS] = GlobalOptions.Common  # Change this to apply a different default configuration

    # So you can use it on inheriting classes without importing it
    _run_after_window_creation = run_after_window_creation

    _run_when_window_exists: list[Callable]
    def __init__(self):
        self._run_when_window_exists = list()

    def _init(self,parent:"BaseElement",window):
        """
        Not __init__

        This gets called when the window is initialized.

        :param parent: Element to contain this element
        :param window: Main Window
        :return:
        """
        self._init_defaults()   # Default configuration
        self._flag_init()
        self.add_flags(ElementFlag.IS_CREATED)

        self._normal_init(parent,window)
        self._personal_init()

        self._apply_update()

    def _flag_init(self):
        """
        Override this to add flags to the element.
        DONT FORGET TO CALL THE SUPER METHOD!
        :return:
        """
        # DON'T FORGET THIS CALL: super()._flag_init()
        # self.add_flags(...)
        pass

    @property
    def element_flags(self) -> set[ElementFlag]:
        if not hasattr(self,"_element_flags"):
            self._element_flags = set()

        return self._element_flags

    def add_flags(self,*flags:ElementFlag):
        """
        Add a flag to this element.

        :param flags:
        :return:
        """
        if not hasattr(self,"_element_flags"):
            self._element_flags = set()

        if not flags:
            return

        self._element_flags.update(set(flags))

    def remove_flags(self,*flags:ElementFlag):
        """
        Pretty self-explanitory
        :param flags:
        :return:
        """
        for i in flags:
            if self.has_flag(i):
                self._element_flags.remove(i)

    def has_flag(self,flag:ElementFlag) -> bool:
        """
        True, if this element has a certain flag
        :param flag:
        :return:
        """
        return flag in self.element_flags

    def _normal_init(self,parent:"BaseElement",window):
        """
        Don't override
        :param parent:
        :param window:
        :return:
        """
        self.parent = parent
        self.window = window

        if not self.has_flag(ElementFlag.DONT_REGISTER_KEY):
            window.register_element(self)

    def _personal_init(self):
        """
        Use to your liking
        :return:
        """
        ...

    def _get_value(self) -> any:
        """
        Returns the value(s) of the Element.
        Override this function.
        :return:
        """
        return None

    def set_value(self,val:any):
        """
        Set the value of the element
        :param val: New value
        :return:
        """
        pass

    @property
    def value(self) -> any:
        """
        Value of the surrounding object.
        Override _get_value to create custom values
        :return:
        """
        return self._get_value()

    @value.setter
    def value(self, val):
        self.set_value(val)

    @property
    def parent_tk_widget(self) ->tk.Widget:
        """
        This will be used to store all contained Widgets into
        :return:
        """
        if self.parent is None:
            return self._fake_tk_element
        return self.parent.parent_tk_widget

    def _init_defaults(self):
        """
        Apply default values in __init__, or here.
        Keep in mind that BaseWidget inherits this method.
        :return:
        """
        pass

    def _update_special_key(self,key:str,new_val:any) -> bool|None:
        """
        Inherit this method to pick out "special" keys to update.
        Keys are passed one-by-one.

        IF YOU RETURN ANYTHING TRUE, THE KEY WILL NOT BE USED IN DEFAULT UPDATE METHOD

        :param key: option-key
        :param new_val: new value for that key
        :return: bool if you want to catch this key, otherwise None
        """
        pass

    def _update_default_keys(self,kwargs):
        """
        Standard-Update method for all those keys that didn't get picked by the special method
        :param kwargs:
        :return:
        """
        pass

    def _apply_update(self):
        """
        Called after an update if the element was already created
        :return:
        """
        ...

    def update(self,**kwargs):
        """
        Update configurations of this element.
        :param kwargs:
        :return:
        """

        kwargs = self.defaults.apply(kwargs)
        kwargs = dict(filter(lambda a: not self._update_special_key(*a), kwargs.items()))
        self._update_default_keys(kwargs)

        if self.has_flag(ElementFlag.IS_CREATED) and self.window.has_flag(ElementFlag.IS_CREATED):
            self._apply_update()

    def init_window_creation_done(self):
        """
        ONLY FOR INHERITING CLASSES!!!
        DON'T CALL!!!

        Will be called oncce as soon as the element exists
        :return:
        """
        for fkt in self._run_when_window_exists:    # Call all those buffered functions
            fkt()


class BaseWidget(BaseElement):
    """
    Base for every Widget
    """
    _tk_widget:tk.Widget
    tk_widget:tk.Widget    # My own tk_widget. Wraps _tk_widget
    _tk_widget_class:type = None # Class of the connected widget
    _tk_kwargs:dict = dict()

    _tk_target_value:tk.Variable = None # By default, the value of this is read when fetching the value

    _insert_kwargs:dict         # kwargs for the packer/grid
    _insert_kwargs_rows:dict    # kwargs for the grid-rows

    #_is_container:bool = False   # True, if this widget contains other widgets
    _contains:Iterable[Iterable["BaseElement"]] = []

    _transfer_keys: dict[str:str] = dict()   # Rename a key from the update-function. from -> to; from_user -> to_widget

    _events_to_bind_later: list[dict]

    def __init__(self,key:any=None,tk_kwargs:dict[str:any]=None,expand:bool = False,**kwargs):
        super().__init__()
        self._events_to_bind_later = list()

        if tk_kwargs is None:
            tk_kwargs = dict()

        tk_kwargs.update(kwargs)
        self._tk_kwargs = tk_kwargs

        self._insert_kwargs = dict()
        self._insert_kwargs_rows = {
            #"sticky":"w"
        }

        self.key = key

        expand = self.defaults.single("expand",expand,False)
        if expand:
            self.add_flags(ElementFlag.EXPAND_ROW)

    def _window_is_dead(self) -> bool:
        """
        Returns True, if the window doesn't exist (anymore?)
        :return:
        """
        return not self.window.has_flag(ElementFlag.IS_CREATED)

    @property
    def tk_widget(self) -> tk.Widget:
        return self._tk_widget

    def bind_event(self,tk_event:str|Event,key_extention:Union[str,any]=None,key:any=None,key_function:Callable|Iterable[Callable]=None)->Self:
        """
        Bind a tk-event onto the underlying tk-widget

        To just throw the element-key, set key_extention = ""

        :param tk_event: tkinter event-string. You don't need to add brackets, if your event-text is longer than 1 char
        :param key_extention: Added to the event-key
        :param key: event-key. If None and key_extention is not None, it will be appended onto the element-key
        :param key_function: Called when this event is thrown
        :return: Calling element for inline-calls
        """
        new_key = None

        if not self.has_flag(ElementFlag.IS_CREATED):
            self._events_to_bind_later.append({
                "tk_event":tk_event,
                "key_extention":key_extention,
                "key":key,
                "key_function":key_function,
            })
            return self

        if hasattr(tk_event,"value"):
            tk_event = tk_event.value

        if len(tk_event) > 1 and not tk_event.startswith("<"):
            tk_event = f"<{tk_event}>"

        match (key_extention is not None,key is not None):
            case (True,True):
                new_key = key + key_extention
            case (False,True):
                new_key = key
            case (True,False):
                new_key = self.key + key_extention
            case (False,False):
                new_key = self.key
                assert new_key or key_function, f"You forgot to add either a key or key_function to this element... {self}"

        temp = self.window.get_event_function(self, new_key, key_function=key_function)

        self._tk_widget.bind(
            tk_event,
            temp
        )

        return self

    def _init_defaults(self):
        self.update(**self._tk_kwargs)

    def _init_widget_for_inherrit(self,container) -> tk.Widget:
        """
        For inheritance to change the way the widget is instantiated
        :param container:
        :return:
        """
        return self._tk_widget_class(container, **self._tk_kwargs)

    def _personal_init_inherit(self):
        """
        At window initialization before full widget initialization
        :return:
        """
        pass

    def _personal_init(self):
        self._personal_init_inherit()
        self._init_widget(self.parent.parent_tk_widget)    # Init the contained widgets

    def _set_tk_target_variable(self,value_type:type=tk.StringVar,kwargs_key:str="textvariable",default_key:str=None,default_value:any=None):
        """
        Define a target variable for this widget
        :param default_key: If given and in self._tk_args, self._tk_args[default_key] will be the default value. The key will be removed from the dict.
        :param value_type: Class of the needed variable
        :param kwargs_key: Key this value will be added into the tk-widget
        :param default_value: Passed to value
        :return:
        """
        if default_key is not None and default_key in self._tk_kwargs:
            default_value = self._tk_kwargs.get(default_key)
            del self._tk_kwargs[default_key]

        self._tk_target_value = value_type(self.parent_tk_widget, value=default_value)
        self._tk_kwargs[kwargs_key] = self._tk_target_value

    def _init_widget(self,container:tk.Widget|tk.Tk,mode:Literal["pack","grid"]="pack") -> None:
        """
        Initialize the widget to the container
        :return:
        """
        self._tk_widget = self._init_widget_for_inherrit(container)

        match mode:
            case "pack":
                #temp = {"expand":False,"side":"left"}
                temp = {"side":"left"}

                temp.update(self._insert_kwargs)

                if self.has_flag(ElementFlag.EXPAND_ROW):
                    temp["expand"] = temp.get("expand",True)
                    temp["fill"] = temp.get("fill","both")

                self._tk_widget.pack(**temp)
            case "grid":
                self._tk_widget.grid(**self._insert_kwargs)

        if self.has_flag(ElementFlag.IS_CONTAINER):
            self._init_containing()

    _containing_row_frame_widgets: list[tk.Frame]
    _background_color: str | Color
    def _init_containing(self):
        """
        Initialize all containing widgets
        :return:
        """
        ins_kwargs_rows = self._insert_kwargs_rows.copy()

        for i in self._contains:
            # line = tk.Frame(self._tk_widget,background="orange",relief="raised",borderwidth="3",border=3)
            # actual_line = tk.Frame(line,background="lightBlue")

            line = tk.Frame(self._tk_widget,relief="flat",background=self._background_color)  # This is the row
            actual_line = tk.Frame(line,background=self._background_color)    # This is where the actual elements are put in
            self._containing_row_frame_widgets.extend((line,actual_line))

            line_elem = BaseElement()
            line_elem._fake_tk_element = actual_line

            expand = False

            for k in i:
                k._init(line_elem,self.window)

                if not expand and k.has_flag(ElementFlag.EXPAND_ROW):
                    expand = True

            if expand:
                ins_kwargs_rows["fill"] = "x"
                ins_kwargs_rows["expand"] = True
            else:
                ins_kwargs_rows["fill"] = "none"
                ins_kwargs_rows["expand"] = False
            #self._insert_kwargs_rows["fill"] = "x"

            #line.pack(side="top",fill="both",expand=True)
            #line.grid(sticky="ew")
            line.pack(fill="x")
            actual_line.pack(**ins_kwargs_rows)

    def _get_value(self) -> any:
        """
        This method is used when the value/state of the Widget is read.
        :return:
        """
        try:
            return self._tk_target_value.get()  # Standard target
        except AttributeError:  # _tk_target_value isn't used
            return None

    def _transfer_kwargs_keys(self,kwargs: dict):
        """
        Transfer/rename keys in kwargs
        :param kwargs:
        :return:
        """
        transfer = set(filter(lambda a:a in kwargs.keys(),self._transfer_keys.keys()))

        for key in transfer:
            kwargs[self._transfer_keys[key]] = kwargs[key]
            del kwargs[key]

        return kwargs

    def _update_default_keys(self,kwargs: dict,transfer_keys: bool = True):
        """
        Transfers/renames keys in kwargs, then applies them
        :param transfer_keys: Simple way to bypass key-transfer
        :param kwargs:
        :return:
        """
        if transfer_keys:
            self._transfer_kwargs_keys(kwargs)

        self._tk_kwargs.update(kwargs)

    def _apply_update(self):
        self._tk_widget.configure(self._tk_kwargs)

    def set_value(self,val:any):
        try:
            self._tk_target_value.set(val)
        except AttributeError:
            pass

    def init_window_creation_done(self):
        super().init_window_creation_done()

        for params in self._events_to_bind_later:
            self.bind_event(**params)
        del self._events_to_bind_later  # Free some ram, because why not

class BaseWidgetContainer(BaseWidget):
    """
    Base for Widgets that contain other widgets
    """
    def __init__(self,key:any=None,tk_kwargs:dict[str:any]=None,expand:bool = False,**kwargs):
        super().__init__(key,tk_kwargs,expand,**kwargs)

        self._containing_row_frame_widgets = list()
        self._background_color: str | Color = self.defaults.single("background_color",None)

    def _flag_init(self):
        super()._flag_init()
        self._line_insert_kwargs = dict()
        self.add_flags(ElementFlag.IS_CONTAINER)

class BaseWidgetTTK(BaseWidget):
    _styletype: str = None  # Style will be named n.styletype
    _style: str = None  # Registered style of this widget
    _stylecounter: int = 0   # This ensures every style has an unique number

    _transfer_keys = {  # Usual couple of keys
        # "background_color_disabled":"disabledbackground",
        "background_color":"background",
        # "text_color_disabled": "disabledforeground",
        "highlightbackground_color": "highlightbackground",
        "selectbackground_color": "selectbackground",
        "select_text_color": "selectforeground",
        # "pass_char":"show",
        "background_color_active" : "activebackground",
        "text_color_active" : "activeforeground",
        "text_color":"foreground",
    }

    _tk_kwargs_for_style: list = [  # These will not pass through to the widget, but to its style
        "background_color",
        "text_color",
        #"relief",
        #"font",
    ]

    def __init__(self, *args, **kwargs):
        self._style = str(BaseWidgetTTK._stylecounter)
        BaseWidgetTTK._stylecounter += 1

        if not "style" in kwargs:
            kwargs["style"] = self._style + "." + self._styletype

        super().__init__(*args, **kwargs)

    def init_window_creation_done(self):
        super().init_window_creation_done()

        #self.window.ttk_style.map(self._style, **self.window.ttk_style.map(self._styletype))

    @run_after_window_creation
    def _config_ttk_style(self, style_ext: str = "", styletype: str = None, **kwargs):
        """
        Don't use unless you create your own ttk-widget, which you probably won't do.
        Changes the configuration of a ttk-style.

        :param style_ext:   Appended to the element-style
        :param styletype:   Pass this to overwrite the default styletype (self._styletype)
        :param kwargs: passed to the style
        :return:
        """

        if style_ext:
            style_ext = f".{style_ext}"

        if not styletype:
            styletype = self._styletype

        self.window.ttk_style.configure(self._style + "." + styletype + style_ext, **kwargs)

    @run_after_window_creation
    def _map_ttk_style(self, style_ext: str = "", styletype: str = None, overwrite_all: bool = False, **kwargs):
        """
        Don't use unless you create your own ttk-widget, which you probably won't do.
        Changes the configuration of a ttk-style.

        :param style_ext:   Appended to the element-style
        :param styletype:   Pass this to overwrite the default styletype (self._styletype)
        :param kwargs: passed to the style
        :param overwrite_all: True, if not only kwargs-keys should be changed, but everything should be mapped. Might overwrite other options.
        :return:
        """

        if style_ext:
            style_ext = f".{style_ext}"

        if not styletype:
            styletype = self._styletype

        stylename = self._style + "." + styletype + style_ext

        kwargs: dict[str, tuple]
        if not overwrite_all:
            new_kwargs = dict()
            for key,val in kwargs.items():
                current = dict(self.window.ttk_style.map(stylename).get(key, []))   # Current mapping converted to dict

                # Remove None-values while we are iterating anyways
                val = filter(lambda a:a[1] is not None, val)

                # Apply passed arguments
                # for inner_key, inner_val in val:  # Readable equivalence
                #     current[inner_key] = inner_val
                current.update(dict(val))   # Faster (probably)

                new_kwargs[key] = list(current.items()) # Convert the mapping back to list for ttk
        else:
            new_kwargs = kwargs


        self.window.ttk_style.map(stylename, **new_kwargs)



