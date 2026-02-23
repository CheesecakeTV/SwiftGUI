
from collections.abc import Iterable, Callable
from functools import partial
from typing import Any, Hashable
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
            texts:Iterable[str] | Iterable[tuple[str, str]],    # Text = keys, or (Text, key)-pairs
            *,
            default_values: Iterable[Any] | dict[str, Any] = None,
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

        :param texts:
        :param default_values:
        :param key:
        :param key_function:
        :param default_event:
        :param small_clear_buttons:
        :param big_clear_button:
        :param submit_button: True, if there should be a submit-button that throws an event when clicked
        :param return_submits: True, if pressing enter should be equal to pressing submit
        """
        texts = list(texts)

        if isinstance(texts[0], str):
            self._texts = texts
            self._input_keys = texts
        else:
            self._texts, self._input_keys = list(zip(*texts))

        max_len = max(map(len,self._texts))

        self._text_elements = [
            Text(
                line,
                width=max_len + 1,
                padding=2
            )
            for line in self._texts
        ]

        self._input_elements = [
            Input(
                key_function= self.throw_default_event,
                default_event= default_event,
                key= t
            )
            for t in texts
        ]

        self._clear_buttons = [
            Button(
                "x",
                key_function= (
                    partial(lambda index: self._input_elements[index].set_value(""), n),
                    self.throw_default_event,
                ),
                width=2,
            ) if small_clear_buttons else Text()
            for n, _ in enumerate(self._input_elements)
        ]

        self.layout = list(zip(self._text_elements, self._input_elements, self._clear_buttons))

        # if Any((submit_button, big_clear_button)):
        #     self.layout.append([HorizontalSeparator()])
        self.layout.append([Spacer(height=5)])

        self.layout.append([])
        if submit_button:
            self._submit_button_element = Button(
                "Submit",
                #key= submit_key if submit_key is not None else None,
                key_function=[self.throw_event, lambda v:self.done(v)]
                #key_function= submit_key_function if submit_key_function else self.throw_event,
            )
            self.layout[-1].append(self._submit_button_element)

        if big_clear_button:
            self.layout[-1].append(Button(
                "Clear",
                key_function= (self.clear_all_values, self.throw_default_event)
            ))

        if return_submits:
            temp = self.throw_event
            # if submit_button: # Looks cool, but slows down the code...
            #     temp = (self.throw_event, self._submit_button_element.flash)

            for elem in self._input_elements:
                elem.bind_event(Event.KeyEnter, key_function=temp)

        super().__init__(Frame(self.layout), key=key, key_function=key_function, default_event=default_event)

        if default_values:
            if isinstance(default_values, dict):
                self.set_value(default_values)
            else:
                self.set_value({
                    k:v for k,v in zip(self._input_keys, default_values)
                })

    def _update_special_key(self,key:str,new_val:Any) -> bool|None:
        match key:
            case _:
                return super()._update_special_key(key, new_val)

        return True

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

    @BaseElement._run_after_window_creation
    def update_submit_button(self, **kwargs) -> Self:
        """
        Evoke .update on the submit-button
        :param kwargs:
        :return:
        """
        self._submit_button_element._update_initial(**kwargs)
        return self

    def clear_all_values(self):
        """
        Does what it says
        :return:
        """
        for elem in self._input_elements:
            elem.value = ""




