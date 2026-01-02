from typing import Any, Callable, Iterable, Hashable
import SwiftGUI as sg
from SwiftGUI.Compat import Self
from datetime import datetime as dt

class Console(sg.BaseCombinedElement):
    defaults = sg.GlobalOptions.Console   # Change this to attach your own GlobalOption-class to the element

    _input_prefix: str  # Added to "prints" when an input is submitted
    _print_prefix: str  # Always added in front of "prints"
    _add_timestamp: bool    # True, if the current time should be printed in front of prints
    def __init__(
            self,
            *,
            key: Hashable = None,
            key_function: Callable | Iterable[Callable] = None,
            default_event: bool = False,
            input_prefix: str = None,
            print_prefix: str = None,
            add_timestamp: bool = None,
            scrollbar: bool = None,
            width: int = None,
            height: int = None,
            apply_parent_background_color: bool = None,
    ):
        self._prev_value: str = ""  # Last thing input and submitted
        self._default_event: bool = default_event   # If default event should be active

        self._layout = [    # Put the containing layout here
            [
                _textField := sg.TextField(
                    readonly= True,
                    scrollbar= self.defaults.single("scrollbar", scrollbar),
                ),
            ],[
                _input := sg.Input(
                    expand= True,
                ).bind_event(
                    sg.Event.KeyEnter,
                    key_function= [
                        lambda val: self.make_input(val, trigger_event= default_event),   # Submit to console
                        lambda elem: elem.set_value(""),    # Clear input
                    ]
                ),
            ]
        ]

        self.input: sg.Input = _input
        self.textField: sg.TextField = _textField

        super().__init__(sg.Frame(self._layout), key=key, key_function=key_function,
                         apply_parent_background_color=apply_parent_background_color, internal_key_system=False)

        self._update_initial(
            input_prefix = input_prefix,
            print_prefix = print_prefix,
            add_timestamp = add_timestamp,
            width = width,
            height = height,
        )

    def _get_value(self) -> Any:
        return self._prev_value

    def set_value(self,val: Any):
        raise NotImplementedError("You can't directly set the value of sg.Console.\n"
                                  "Use [sg.Console].input.value to change the value of the input-field.\n"
                                  "Use [sg.Console].make_input(...) to simulate a user-input")

    def _update_special_key(self,key:str,new_val:any) -> bool|None:
        # Divert to text-field
        if key in ["height"]:
            self.textField.update(**{key:new_val})
            return True

        # Divert to input
        if key in []:
            self.input.update(**{key:new_val})
            return True

        match key:
            case "input_prefix":
                if new_val is None:
                    return
                self._input_prefix = new_val
            case "print_prefix":
                if new_val is None:
                    return
                self._print_prefix = new_val
            case "add_timestamp":
                self._add_timestamp = new_val
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
        self.input.update(**kwargs)
        self.textField.update(**kwargs)

    @staticmethod
    def get_time() -> str:
        """
        Return the current time as a string
        :return:
        """
        return dt.now().strftime("%H:%M:%S")

    @sg.BaseCombinedElement._run_after_window_creation
    def print(self, *text: Any, sep: str = " ", end = "\n") -> Self:
        """
        Print to the console.
        Arguments are the same as with normal print(...)
        :param text:
        :param sep:
        :param end:
        :return:
        """
        text = map(str, text)

        text = self._print_prefix + sep.join(text)

        if self._add_timestamp:
            text = self.get_time() + text

        self.append(text + end, add_newline=False)
        return self

    @sg.BaseCombinedElement._run_after_window_creation
    def make_input(self, text: str, trigger_event: bool = False) -> Self:
        """
        Simulate an user-input.
        :param trigger_event: True, if this should trigger the default event. It will trigger no matter if specified enabled or not when creating the element.
        :param text:
        :return:
        """
        self._prev_value = text

        text = self._input_prefix + text

        if self._add_timestamp:
            text = self.get_time() + text

        self.append(text + "\n", add_newline= False)

        if trigger_event:
            self.throw_event()

        return self

    def append(self, text: str, add_newline: bool = True) -> Self:
        """
        Just append to the text-field, nothing more, nothing less
        :param add_newline: True, if \n should be appended too
        :param text:
        :return:
        """
        self.textField.append(text, add_newline=add_newline)
        self.textField.see_end()
        return self

    def clear(self) -> Self:
        """
        Clear the whole output-history.
        Does not clear .value
        :return:
        """
        self.textField.value = ""
        return self
