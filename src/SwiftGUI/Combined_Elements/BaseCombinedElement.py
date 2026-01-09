from collections.abc import Iterable, Callable
from typing import Any, Hashable

from SwiftGUI import BaseElement, SubLayout, Frame
from SwiftGUI.Compat import Self
from SwiftGUI.ElementFlags import ElementFlag
from SwiftGUI.Windows import ValueDict

class BaseCombinedElement(BaseElement):
    """
    Derive from this class to create an element consisting of multiple inner elements.
    """
    _sg_widget: Frame | SubLayout

    def __init__(
            self,
            layout: Frame | Iterable[Iterable[BaseElement]],
            *,
            key: Hashable = None,
            key_function: Callable | Iterable[Callable] = None,
            apply_parent_background_color: bool = True,
            internal_key_system: bool = True,
    ):
        """

        :param layout: Pass a layout or a Frame containing all the elements you'd like to have inside this element
        :param key: Pass a key to register it in main window
        :param apply_parent_background_color: True, if the background_color of the parent container should also apply to this frame
        :param internal_key_system: True, if keys should be passed up to the main event loop instead of ._event_loop
        """
        super().__init__()

        if isinstance(layout, Frame):
            frame = layout
        else:
            frame = Frame(layout)

        if internal_key_system:
            self._has_sublayout = True
            self._sg_widget = SubLayout(frame, self._event_loop)
        else:
            self._has_sublayout = False
            self._sg_widget = frame

        self.key = key
        self._key_function = key_function

        self._throw_event: Callable = lambda :None

        if apply_parent_background_color:
            self.add_flags(ElementFlag.APPLY_PARENT_BACKGROUND_COLOR)

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
        Throw the default event to the window
        :return:
        """
        self._throw_event()

    def _personal_init(self):
        self._sg_widget._init(self, self.window)
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
                self._sg_widget._update_initial(background_color=new_val)
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

        return self._sg_widget

    @property
    def v(self):
        """
        Reference to the value-dict
        """
        return self.w.value

    def _get_value(self) -> Any:
        """
        Overwrite this to return a custom value
        :return:
        """
        return self._sg_widget.value

    def __getitem__(self, item: Hashable):
        if not self._has_sublayout:
            raise NotImplementedError(f"{self} has no sub-layout, so __getitem__ is not defined.")
        return self._sg_widget[item]

    def __setitem__(self, key: Hashable, value: Any):
        if not self._has_sublayout:
            raise NotImplementedError(f"{self} has no sub-layout, so __setitem__ is not defined.")
        self._sg_widget[key].value = value

    def set_value(self, val:Any) -> Self:
        """
        Overwrite multiple values at once.
        Works like .update for dicts, so ignores non-passed keys
        :param val:
        :return:
        """
        if not self._has_sublayout:
            raise NotImplementedError(f"{self} has no sub-layout, so set_value is not defined.")

        self._sg_widget.set_value(val)

    def delete(self) -> Self:
        """
        Remove this element permanently from the layout.

        Keep in mind that its row still exists, even if it is empty.
        This can cause performance issues.
        """
        self._sg_widget.delete()
        self.remove_flags(ElementFlag.IS_CREATED)
        return self
