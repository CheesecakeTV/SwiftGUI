from collections.abc import Iterable, Callable
from typing import Any, Hashable

from SwiftGUI import BaseElement, SubLayout, Frame
from SwiftGUI.Compat import Self
from SwiftGUI.ElementFlags import ElementFlag
from SwiftGUI.Windows import ValueDict
from SwiftGUI.Popups import ElementPopup, ElementPopupNonblocking

# Placeholder-function
def _do_nothing(*_) -> None:
    pass

class BaseCombinedElement(BaseElement):
    """
    Derive from this class to create an element consisting of multiple inner elements.
    """
    sg_widget: Frame | SubLayout

    def __init__(
            self,
            layout: Frame | Iterable[Iterable[BaseElement]],
            *,
            default_event: bool = False,
            key: Hashable = None,
            key_function: Callable | Iterable[Callable] = None,
            apply_parent_background_color: bool = True,
            internal_key_system: bool = True,
            popup_kwargs: dict[str, Any] = None,
    ):
        """

        :param layout: Pass a layout or a Frame containing all the elements you'd like to have inside this element
        :param default_event: True, if throw_default_event should throw an event
        :param key: Pass a key to register it in main window
        :param apply_parent_background_color: True, if the background_color of the parent container should also apply to this frame
        :param internal_key_system: True, if keys should be passed up to the main event loop instead of ._event_loop
        :param popup_kwargs: When passing a dict, these values are passed to .popup and .popup_nonblocking automatically
        """
        super().__init__()

        self._default_event = default_event

        if isinstance(layout, Frame):
            frame = layout
        else:
            frame = Frame(layout)

        if internal_key_system:
            self._has_sublayout = True
            self.sg_widget = SubLayout(frame, self._event_loop)
        else:
            self._has_sublayout = False
            self.sg_widget = frame

        self.key = key
        self._key_function = key_function

        self._throw_event: Callable = _do_nothing

        if apply_parent_background_color:
            self.add_flags(ElementFlag.APPLY_PARENT_BACKGROUND_COLOR)

        if popup_kwargs is None:
            popup_kwargs = dict()
        self._popup_kwargs = popup_kwargs

    def _event_loop(self, e: Any, v: ValueDict):
        """
        All key-events will call this method, if internal key-system is enabled.
        You can use it exactly like your normal event-loop.

        :param e: Contains the element-key
        :param v: Contains all values
        :return:
        """
        ...

    def throw_event(self):
        """
        Throw an event of this element, no matter if default-event is enabled or not.
        You may overwrite this to change the event behavior.
        The actual event-function that causes the event is self._throw_event(), so don't forget to call it.
        :return:
        """
        self._throw_event()

    def throw_default_event(self):
        """
        Throw an event, but only if the default-event is enabled.
        You may overwrite this to change the event behavior.
        :return:
        """
        if self._default_event:
            self.throw_event()

    def _personal_init(self):
        """
        Do not overwrite.
        This initializes the internal sub-layout/frame and requests an event-function from the key-handler
        :return:
        """
        self.sg_widget._init(self, self.window)
        self._throw_event = self.window.get_event_function(me= self, key= self.key, key_function= self._key_function)

    def _update_special_key(self,key:str,new_val:Any) -> bool|None:
        """
        Inherit (use) this method to pick out "special" keys to update.
        Keys are passed one-by-one.

        When calling .update, this method gets called first.
        If it returns anything truethy, execution of .update ends for this key.

        Otherwise, ._update_default_keys gets called for the key.

        Just copy the whole method and add more cases.

        :param key:
        :param new_val:
        :return:
        """
        match key:
            case "background_color":
                self.sg_widget._update_initial(background_color=new_val)
            case "default_event":
                self._default_event = new_val
            case _:
                # The key wasn't found in any other case
                return super()._update_special_key(key, new_val)    # Look in the parent-class

        # The key was found in match-case
        return True

    @property
    def w(self):
        """
        References the "window" (Sub-layout)
        :return:
        """
        if not self._has_sublayout:
            return self.window

        return self.sg_widget

    @property
    def v(self):
        """
        Reference to the value-dict.
        You may know this one from
            e, v = w.read()
        """
        return self.w.value

    def _get_value(self) -> Any:
        """
        This is returned when
            elem.value
        is called on this element.
        Overwrite it to specify the value this element generates
        :return:
        """
        return self.sg_widget.value

    def __getitem__(self, item: Hashable):
        if not self._has_sublayout:
            raise NotImplementedError(f"{self} has no sub-layout, so __getitem__ is not defined.")
        return self.sg_widget[item]

    def __setitem__(self, key: Hashable, value: Any):
        if not self._has_sublayout:
            raise NotImplementedError(f"{self} has no sub-layout, so __setitem__ is not defined.")
        self.sg_widget[key].value = value

    @BaseElement._run_after_window_creation
    def set_value(self, val: Any) -> Self:
        """
        This is called when
            elem.value = ...
        is used.
        Overwrite it to specify the behavior of .value

        :param val:
        :return:
        """
        if not self._has_sublayout:
            raise NotImplementedError(f"{self} has no sub-layout, so set_value is not defined.")

        self.sg_widget.set_value(val)
        return self

    def delete(self) -> Self:
        """
        Remove this element permanently from the layout.

        Keep in mind that its row still exists, even if it is empty.
        This can cause performance issues.
        You should not overwrite this.
        """
        self.sg_widget.delete()
        self.remove_flags(ElementFlag.IS_CREATED)
        return self

    done_method: Callable = _do_nothing   # Overwritten by the actual .done later
    def done(self, val: Any = None) -> None:
        """
        If this element is opened as a popup, .done(...) will call the popups .done().
        Otherwise, this does nothing.
        You should not overwrite this.

        :param val: "Return"-value
        :return:
        """
        self.done_method(val)

    def popup(self, **window_kwargs) -> Any:
        """
        Open this NEW AND UNUSED element as a blocking popup
        self.done(...) will work like with normal popups.

        You may overwrite this, but make sure to not forget to call super().popup(...)

        :param window_kwargs: Passed to the window. Use this to set a title, etc.
        :return: Return of the popup
        """
        kwargs = self._popup_kwargs.copy()
        kwargs.update(window_kwargs)
        return ElementPopup(self, **kwargs)

    def popup_nonblocking(self, **window_kwargs) -> ElementPopupNonblocking:
        """
        Open this NEW AND UNUSED element as a non-blocking popup
        self.done(...) will close the window, but return nothing

        You may overwrite this, but make sure to not forget to call super().popup_nonblocking(...)

        :param window_kwargs: Passed to the window. Use this to set a title, etc.
        :return: Return of the popup
        """
        kwargs = self._popup_kwargs.copy()
        kwargs.update(window_kwargs)
        return ElementPopupNonblocking(self, **kwargs)

