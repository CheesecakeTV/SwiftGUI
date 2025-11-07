from typing import Any, Callable, Iterable, Self
import SwiftGUI as sg


class Example(sg.BaseCombinedElement):
    defaults = sg.GlobalOptions.DEFAULT_OPTIONS_CLASS   # Change this to attach your own GlobalOption-class to the element

    def __init__(
            self,
            key: Any = None,
            key_function: Callable | Iterable[Callable] = None,
            apply_parent_background_color: bool = None,
    ):
        self._layout = [    # Put the containing layout here

        ]

        super().__init__(frame=sg.Frame(self._layout), key=key, key_function=key_function,
                         apply_parent_background_color=apply_parent_background_color)

        self._update_initial(
            # Put all of your options in here
        )

    def _event_loop(self, e: Any, v: dict):
        """An event-loop just for this element. Use self.w to refer to keys inside this element."""
        ...

    def _get_value(self) -> Any:
        """Returns the value (self.value) of this element"""
        return super()._get_value()

    def set_value(self,val: Any):
        """Changes the value of this element (self.value = val)"""
        super().set_value(val)

    def init_window_creation_done(self) -> Self:
        """Runs once, after the window was created"""
        super().init_window_creation_done() # Don't forget this call, very important!
        return self

    def _update_special_key(self,key:str,new_val:any) -> bool|None:
        """
        When calling .update, this method gets called first.
        If it returns anything truethy (like True), execution of .update ends for this key.

        Otherwise, ._update_default_keys gets called for the key.

        In combined elements, you'll most likely only use ._update_special_key, but knock yourself out.
        """
        match key:
            case _: # No other case covered this key, so let's let's the parent-class handle the rest
                return super()._update_special_key(key, new_val)

        return True # Key was covered by match, so don't pass it to _update_default_keys

    def _update_default_keys(self,kwargs):
        """
        Standard-Update method for all those keys that didn't get picked by the special method
        :param kwargs:
        :return:
        """
        super()._update_default_keys(kwargs)
