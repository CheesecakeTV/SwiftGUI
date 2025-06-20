from collections.abc import Iterable, Callable
from typing import Literal, Self, Union
import tkinter as tk

from SwiftGUI_LeButch import Event
from SwiftGUI_LeButch.ElementFlags import ElementFlag


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

    _key_function_send_wev:bool = False   # True, if window, event, value should be sent to key_function
    _key_function_send_val:bool = False   # True, if current event value shall be sent to key_function
    # If both are True, it will be sent like this: window, event, values, value

    def _init(self,parent:"BaseElement",window):
        """
        Not __init__

        This gets called when the window is initialized.

        :param parent: Element to contain this element
        :param window: Main Window
        :return:
        """
        self._flag_init()
        self._normal_init(parent,window)
        self._personal_init()

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
    def tk_widget(self) ->tk.Widget:
        """
        This will be used to store all contained Widgets into
        :return:
        """
        if self.parent is None:
            return self._fake_tk_element
        return self.parent.tk_widget


class BaseWidget(BaseElement):
    """
    Base for every Widget
    """
    _tk_widget:tk.Widget
    _tk_widget_class:type = None # Class of the connected widget
    _tk_args:tuple = tuple()    # args and kwargs to pass to the tk_widget_class when initializing
    _tk_kwargs:dict = dict()

    _tk_target_value:tk.Variable = None # By default, the value of this is read when fetching the value

    _insert_kwargs:dict = dict()    # kwargs for the packer/grid

    #_is_container:bool = False   # True, if this widget contains other widgets
    _contains:Iterable[Iterable[Self]] = []

    # @property
    # def _is_container(self) -> bool:
    #     return False

    def __init__(self,key:any=None,tk_args:tuple[any]=tuple(),tk_kwargs:dict[str:any]=None):
        self._tk_args = tk_args

        if tk_kwargs is None:
            tk_kwargs = dict()
        self._tk_kwargs = tk_kwargs

        self._insert_kwargs = {"side":tk.LEFT}
        self.key = key

    def bind_event(self,tk_event:str|Event,key_extention:Union[str,any]=None,key:any=None,key_function:Callable|Iterable[Callable]=None,send_wev:bool=False,send_val:bool=False)->Self:
        """
        Bind a tk-event onto the underlying tk-widget

        To just throw the element-key, set key_extention = ""

        :param tk_event: tkinter event-string. You don't need to add brackets, if your event-text is longer than 1 char
        :param key_extention: Added to the event-key
        :param key: event-key. If None and key_extention is not None, it will be appended onto the element-key
        :param key_function: Called when this event is thrown
        :param send_wev: Send window, event, values to functions
        :param send_val: Send element-value to functions
        :return: Calling element for inline-calls
        """
        new_key = None

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
                pass

        temp = self.window.get_event_function(self, new_key, key_function=key_function, key_function_send_wev=send_wev,
                                       key_function_send_val=send_val)

        self._tk_widget.bind(
            tk_event,
            temp
        )

        return self

    # @property
    # def tk_widget(self) ->tk.Widget:
    #     """
    #     Returns the tkinter widget connected to this sg-widget
    #     :return:
    #     """
    #     return self._tk_widget

    def _init_widget_for_inherrit(self,container) -> tk.Widget:
        """
        For inheritance to change the way the widget is instantiated
        :param container:
        :return:
        """
        return self._tk_widget_class(container, *self._tk_args, **self._tk_kwargs)

    def _personal_init_inherit(self):
        """
        At window initialization before full widget initialization
        :return:
        """
        pass

    def _personal_init(self):
        self._personal_init_inherit()
        self._init_widget(self.parent.tk_widget)    # Init the contained widgets

    def _set_tk_target_variable(self,value_type:type=tk.StringVar,kwargs_key:str="textvariable",default_value:any=None):
        """
        Define a target variable for this widget
        :param value_type: Class of the needed variable
        :param kwargs_key: Key this value will be added into the tk-widget
        :param default_value: Passed to value
        :return:
        """
        self._tk_target_value = value_type(self.tk_widget,value=default_value)
        self._tk_kwargs[kwargs_key] = self._tk_target_value

    def _init_widget(self,container:tk.Widget|tk.Tk,mode:Literal["pack","grid"]="pack") -> None:
        """
        Initialize the widget to the container
        :return:
        """
        self._tk_widget = self._init_widget_for_inherrit(container)

        match mode:
            case "pack":
                self._tk_widget.pack(**self._insert_kwargs)
            case "grid":
                self._tk_widget.grid(**self._insert_kwargs)

        if self.has_flag(ElementFlag.IS_CONTAINER):
            self._init_containing()

    def _init_containing(self):
        """
        Initialize all containing widgets
        :return:
        """
        for i in self._contains:
            line = tk.Frame(self._tk_widget)

            line_elem = BaseElement()
            line_elem._fake_tk_element = line

            for k in i:
                k._init(line_elem,self.window)

            line.grid()

    def _get_value(self) -> any:
        """
        This method is used when the value/state of the Widget is read.
        :return:
        """
        try:
            return self._tk_target_value.get()  # Standard target
        except AttributeError:  # _tk_target_value isn't used
            return None

    def set_value(self,val:any):
        try:
            self._tk_target_value.set(val)
        except AttributeError:
            pass

class BaseWidgetContainer(BaseWidget):
    """
    Base for Widgets that contain other widgets
    """
    def _flag_init(self):
        super()._flag_init()
        self.add_flags(ElementFlag.IS_CONTAINER)

