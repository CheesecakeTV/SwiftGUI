from collections.abc import Iterable
from typing import Literal,Self
import tkinter as tk


class BaseElement:
    """
    Base for every element and widget.

    The different to BaseWidget is that BaseWidget is designed for a single tk-Widget.
    BaseElement allows you to do whatever the f you want, it's just a class pattern.
    """
    parent:Self = None  # next higher Element
    fake_tk_element:tk.Widget = None   # This gets returned when parent is None
    is_container:bool = False   # True, if this Element contains others
    window = None # Main Window

    def _init(self,parent:"BaseElement",window):
        """
        Not __init__

        This gets called when the window is initialized.

        :param parent: Element to contain this element
        :param window: Main Window
        :return:
        """
        self._normal_init(parent,window)
        self._personal_init()

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
        Returns the value(s) of the Element
        :return:
        """
        return None

    @property
    def tk_widget(self) ->tk.Widget:
        """
        This will be used to store all contained Widgets into
        :return:
        """
        if self.parent is None:
            return self.fake_tk_element
        return self.parent.tk_widget


class BaseWidget(BaseElement):
    """
    Base for every Widget
    """
    _tk_widget:tk.Widget
    _tk_widget_class:type = None # Class of the connected widget
    _tk_args:tuple = tuple()    # args and kwargs to pass to the tk_widget_class when initializing
    _tk_kwargs:dict = dict()

    _tk_target_value:tk.Variable = None

    _insert_kwargs:dict = dict()    # kwargs for the packer/grid

    is_container:bool = False   # True, if this widget contains other widgets
    contains:Iterable[Iterable[Self]] = []

    # @property
    # def is_container(self) -> bool:
    #     return False

    def __init__(self,tk_args:tuple[any]=tuple(),tk_kwargs:dict[str:any]=None):
        self._tk_args = tk_args

        if tk_kwargs is None:
            tk_kwargs = dict()
        self._tk_kwargs = tk_kwargs

        self._insert_kwargs = {"side":tk.LEFT}

    @property
    def tk_widget(self) ->tk.Widget:
        """
        Returns the tkinter widget connected to this sg-widget
        :return:
        """
        return self._tk_widget

    def _init_widget_for_inherrit(self,container) -> tk.Widget:
        """
        For inheritance to change the way the widget is instantiated
        :param container:
        :return:
        """
        return self._tk_widget_class(container, *self._tk_args, **self._tk_kwargs)

    def _personal_init(self):
        self._init_widget(self.parent.tk_widget)

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

        if self.is_container:
            self._init_containing()

    def _init_containing(self):
        """
        Initialize all containing widgets
        :return:
        """
        for i in self.contains:
            line = tk.Frame(self._tk_widget)

            line_elem = BaseElement()
            line_elem.fake_tk_element = line

            for k in i:
                k._init(line_elem,self.window)

            line.grid()

    @property
    def value(self) -> any:
        """
        Value of the surrounding object.
        Override _get_value to create custom values
        :return:
        """
        try:
            return self._get_value()
        except AttributeError:
            return None

    def _get_value(self) -> any:
        """
        This method is used when the value/state of the Widget is read.
        :return:
        """
        return self._tk_target_value.get()  # Standard target

class BaseContainer(BaseWidget):
    """
    Base for Widgets that contain other widgets
    """
    is_container = True

    def window_entry_point(self,root:tk.Tk,window:BaseElement):
        """
        Starting point for the whole window.
        Don't use this unless you overwrite the sg.Window class
        :param window: Window Element
        :param root: Window to put every element
        :return:
        """
        self.window = window
        self._init_widget(root)
