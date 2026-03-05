
from collections.abc import Iterable, Callable
from functools import partial
from typing import Any, Hashable, Mapping
from SwiftGUI.Compat import Self
import json

from SwiftGUI import BaseElement, Frame, Text, Input, BaseCombinedElement, Button, Event
#from SwiftGUI.Widget_Elements.Separator import HorizontalSeparator
from SwiftGUI.Extended_Elements.Spacer import Spacer


# Advanced / Combined elements
class Form(BaseCombinedElement):
    """
    Grid-Layout-Form with text-Input-combinations

    It is WIP, but I'm adding more functionality regularely
    I'll probably throw this whole class out of the window and redo it, since it is so unfathomly bad atm.
    """

    def __init__(
            self,
            texts:Iterable[str] | Mapping[Hashable, str],    # Text = keys, or (Text, key)-pairs
            *,
            default_values: Iterable[Any] | Mapping[Hashable, str] = None,
            key: Hashable = None,
            key_function: Callable | Iterable[Callable] = None,
            default_event: bool = None,
            small_clear_buttons: bool = None,
            big_clear_button: bool = None,
            submit_button: bool = None,
            #submit_key: Any = None,
            return_submits: bool = None,
    ):
        """

        :param texts: Texts displayed before the input-elements. Pass a dict to specify the keys of each input. Beware: The value becomes a dict if you specify keys
        :param default_values: Initial values. Pass as a list or a dict
        :param key:
        :param key_function:
        :param default_event: If any input changes, an event gets thrown
        :param small_clear_buttons: Small x-buttons behind each input to clear it with one click
        :param big_clear_button: One big clear-button under the inputs to clear all inputs at once
        :param submit_button: True, if there should be a submit-button that throws an event when clicked. Ignores the default event
        :param return_submits: True, if pressing enter should be equal to pressing submit. Ignores the default event
        """
        self._has_key_mapping = isinstance(texts, Mapping)

        if self._has_key_mapping:
            values = list(texts.values())
        else:
            values = list(texts)

        _max_len = max(map(len, values))

        self._input_elements: list[Input] = list()
        self._text_elements: list[Text] = list()

        self._small_clear_buttons = small_clear_buttons
        self._return_submits = return_submits

        if self._has_key_mapping:
            layout = [
                *[
                    self._make_row(k,t, text_len=_max_len) for t,k in texts.items()
                ]
            ]
        else:
            layout = [
                *[
                    self._make_row(t, text_len=_max_len) for t in values
                ]
            ]

        button_row: list[BaseElement] = list()

        if big_clear_button:
            self.clear_button = Button(
                "Clear",
                key_function= lambda: self.clear_all_values(throw_default_event=True),
            )
            button_row.append(self.clear_button)

        if submit_button:
            self.submit_button = Button(
                "Submit",
                key_function=self.throw_event,
            )
            button_row.append(self.submit_button)

        if button_row:
            layout.append(button_row)

        super().__init__(
            layout,
            key=key,
            key_function=key_function,
            default_event=default_event,
        )

        if default_values is not None:
            self.set_value(default_values)

    def _make_row(self, text: str, key: Hashable = None, text_len: int = 20) -> list[BaseElement]:
        """
        Create a single row of elements
        :param text:
        :param key:
        :return:
        """
        input_elem = Input(
            key=key,
            default_event=True,
            key_function=self.throw_default_event,
        )
        self._input_elements.append(input_elem)

        if self._return_submits:
            input_elem.bind_event(
                Event.KeyEnter,
                key_function= self.throw_event,
            )

        row: list[BaseElement] = [
            Text(
                text,
                width= text_len,
            ),
            input_elem,
        ]

        if self._small_clear_buttons:
            row.append(Button(
                text= "x",
                width=2,
                key_function= lambda: input_elem.set_value("", throw_event=True),
                takefocus= False,
            ))

        return row

    @BaseCombinedElement._run_after_window_creation
    def set_value(self, val: Iterable | Mapping) -> Self:
        """
        Either pass a dict (Mapping) to overwrite specific items or an iterable to overwrite one after another
        :param val:
        :return:
        """
        if isinstance(val, Mapping):
            super().set_value(val)
        else:
            for value, elem in zip(val, self._input_elements):
                elem.value = value

    def values(self) -> tuple:
        """
        Return a tuple with all form-values one after the other
        :return:
        """
        return tuple(map(lambda a:a.value, self._input_elements))

    def _get_value(self):
        if self._has_key_mapping:
            return super()._get_value()

        return self.values()

    @BaseElement._run_after_window_creation
    def update_texts(self,**kwargs) -> Self:
        """
        Evoke .update on every text-element
        :param kwargs:
        :return:
        """
        for elem in self._text_elements:
            elem._update_initial(**kwargs)
        return self

    @BaseElement._run_after_window_creation
    def update_inputs(self,**kwargs) -> Self:
        """
        Evoke .update on every text-element
        :param kwargs:
        :return:
        """
        for elem in self._input_elements:
            elem._update_initial(**kwargs)
        return self

    def clear_all_values(self, throw_default_event: bool = False):
        """
        Does what it says
        :return:
        """
        for elem in self._input_elements:
            elem.value = ""

        if throw_default_event:
            self.throw_default_event()

    def set_focus(self):
        """
        Focus the first row of this element
        :return:
        """
        self._input_elements[0].set_focus()




