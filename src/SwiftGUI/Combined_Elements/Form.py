
from collections.abc import Iterable, Callable
from functools import partial
from typing import Any
from SwiftGUI.Compat import Self
import json

from SwiftGUI import BaseElement, Frame, Text, Input, BaseCombinedElement, Button
#from SwiftGUI.Widget_Elements.Separator import HorizontalSeparator
from SwiftGUI.Widget_Elements.Spacer import Spacer


# Advanced / Combined elements
class Form(BaseCombinedElement):
    """
    Grid-Layout-Form with text-Input-combinations

    Still very WIP (of course), just a proof of concept
    """

    def __init__(
            self,
            texts:Iterable[str] | Iterable[tuple[str, str]],    # Text = keys, or (Text, key)-pairs
            /,
            default_values: Iterable[str] | dict[str:str] = None,
            key:Any = None,
            key_function: Callable | Iterable[Callable] = None,
            default_event: bool = None,
            small_clear_buttons: bool = None,
            big_clear_button: bool = None,
            submit_button: bool = None,
            submit_key: Any = None,
    ):
        texts = list(texts)
        self._default_event = default_event

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
                key_function= self._throw_default_event,
                default_event= default_event,
            )
            for _ in texts
        ]

        self._clear_buttons = [
            Button(
                "x",
                key_function= (
                    partial(lambda index: self._input_elements[index].set_value(""), n),
                    self._throw_default_event,
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
                key= submit_key if submit_key is not None else None,
                key_function=self.throw_event
                #key_function= submit_key_function if submit_key_function else self.throw_event,
            )
            self.layout[-1].append(self._submit_button_element)

        if big_clear_button:
            self.layout[-1].append(Button(
                "Clear",
                key_function= (self.clear_all_values, self._throw_default_event)
            ))

        super().__init__(Frame(self.layout), key=key, key_function=key_function)

        if default_values:
            if isinstance(default_values, dict):
                self.set_value(default_values)
            else:
                self.set_value({
                    k:v for k,v in zip(self._input_keys, default_values)
                })

    def _throw_default_event(self):
        """
        Throw an event if default event is wanted
        :return:
        """
        if self._default_event:
            self.throw_event()

    def _get_value(self) -> Any:
        return {
            line:elem.value for line,elem in zip(self._input_keys, self._input_elements)
        }

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
        Evoke .update on every text-element
        :param kwargs:
        :return:
        """
        self._submit_button_element._update_initial(**kwargs)
        return self

    @BaseElement._run_after_window_creation
    def set_value(self,val:dict[str:str]) -> Self:
        """
        Update only passed keys with their value
        :param val:
        :return:
        """
        for i,text in enumerate(self._input_keys):
            if text in val.keys():
                self._input_elements[i].value = val[text]

        return self

    def clear_all_values(self):
        """
        Does what it says
        :return:
        """
        for elem in self._input_elements:
            elem.value = ""

    def export_json(self, indent:int = None, **kwargs) -> str:
        """
        Return the values as json
        :return:
        """
        return json.dumps(self.value, indent= indent, **kwargs)

    @BaseElement._run_after_window_creation
    def import_json(self, json_str: str, **kwargs) -> Self:
        """
        Load values from a json-string
        :param json_str:
        :param kwargs:
        :return:
        """
        self.value = json.loads(json_str, **kwargs)
        return self





