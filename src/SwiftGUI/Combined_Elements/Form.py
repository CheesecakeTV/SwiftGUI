from typing import Any, Hashable, Mapping, Iterable, Callable
from SwiftGUI.Compat import Self

from SwiftGUI import BaseElement, Text, Input, BaseCombinedElement, Button, Event, GlobalOptions, ValueDict, Spacer


# Advanced / Combined elements
class Form(BaseCombinedElement):
    """
    Grid-Layout-Form with text-Input-combinations

    It is WIP, but I'm adding more functionality regularely
    I'll probably throw this whole class out of the window and redo it, since it is so unfathomly bad atm.
    """
    defaults = GlobalOptions.Form
    value: ValueDict | tuple

    def __init__(
            self,
            texts:Iterable[str] | Mapping[Hashable, str],    # Text = keys, or (Text, key)-pairs
            *,
            default_values: Iterable[Any] | Mapping[Hashable, str] = None,
            key: Hashable = None,
            key_function: Callable | Iterable[Callable] = None,
            default_event: bool = None,
            return_submits: bool = None,
            small_clear_buttons: bool = None,
            big_clear_button: bool = None,
            clear_button_text: str = None,
            submit_button: bool = None,
            submit_button_text: str = None,
            space_over_buttons: int = None,
            space_between_rows: int = None,
            #submit_key: Any = None,
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
        :param clear_button_text: Text on the clear-button
        :param submit_button_text: Text on the submit-button
        :param space_over_buttons: Height of the separator in the row before the buttons
        :param space_between_rows: Height of the separators between the rows
        """
        space_between_rows = self.defaults.single("space_between_rows", space_between_rows)
        space_over_buttons = self.defaults.single("space_over_buttons", space_over_buttons)

        self._mapping_mode = isinstance(texts, Mapping)

        if self._mapping_mode:
            values = list(texts.values())
        else:
            values = list(texts)

        _max_len = max(map(len, values)) + 2    # Todo: Make the additional space configurable

        self._input_elements: list[Input] = list()
        self._text_elements: list[Text] = list()
        self._small_clear_button_elements: list[Button] = list()

        self._small_clear_buttons = small_clear_buttons
        self._return_submits = return_submits

        if self._mapping_mode:
            rows = [
                self._make_row(k,t, text_len=_max_len) for t,k in texts.items()
            ]
        else:
            rows = [
                self._make_row(t, text_len=_max_len) for t in values
            ]

        layout = []
        if space_between_rows:
            for row in rows[:-1]:
                layout.append(row)
                layout.append([Spacer(height=space_between_rows)])

            if len(rows):
                layout.append(rows[-1])
        else:
            layout = rows

        button_row: list[BaseElement] = list()

        self.clear_button = Button(
            self.defaults.single("clear_button_text", clear_button_text),
            key_function= lambda: self.clear_all_values(throw_default_event=True),
        ).set_visible(big_clear_button)
        button_row.append(self.clear_button)

        self.submit_button = Button(
            self.defaults.single("submit_button_text", submit_button_text),
            key_function=self.throw_event,
        ).set_visible(submit_button)
        button_row.append(self.submit_button)

        if space_over_buttons:
            layout.append([Spacer(height=space_over_buttons)])
        elif space_between_rows:
            layout.append([Spacer(height=space_between_rows)])

        layout.append(button_row)

        super().__init__(
            layout,
            key=key,
            key_function=key_function,
            default_event=default_event,
        )

        if default_values is not None:
            self.set_value(default_values)

    def _update_special_key(self,key:str,new_val:Any) -> bool|None:
        match key:
            case "clear_button_text":
                self.clear_button.set_value(new_val)
            case "submit_button_text":
                self.submit_button.set_value(new_val)

            case _:
                return super()._update_special_key(key, new_val)

        return True

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
            input_elem.bind_event(Event.KeyEnter, key_function=self.throw_event)

        row: list[BaseElement] = [
            Text(
                text,
                width= text_len,
            ),
            input_elem,
        ]

        if self._small_clear_buttons:
            button = Button(
                text= "x",
                width=2,
                key_function= lambda: input_elem.set_value("", throw_event=True),
                takefocus= False,
            )
            row.append(button)
            self._small_clear_button_elements.append(button)

        return row

    def __getitem__(self, item: Hashable | int) -> str:
        assert self._mapping_mode or isinstance(item, int), f"{repr(self)} is created in list-mode, so only integer indexes can be used as key!"

        return self.value[item]

    def __setitem__(self, key: Hashable | int, value):
        assert self._mapping_mode or isinstance(key, int), f"{repr(self)} is created in list-mode, so only integer indexes can be used as key!"

        if self._mapping_mode:
            if not key in self.v:
                raise KeyError(f"{repr(self)} was given a key that it doesn't contain")
            self.v[key] = value
        else:
            self._input_elements[key].value = value

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

        return self

    def as_tuple(self) -> tuple:
        """
        Return a tuple with all form-values one after the other
        :return:
        """
        return tuple(map(lambda a:a.value, self._input_elements))

    def _get_value(self):
        if self._mapping_mode:
            return super()._get_value()

        return self.as_tuple()

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
        Evoke .update on every input-element
        :param kwargs:
        :return:
        """
        for elem in self._input_elements:
            elem._update_initial(**kwargs)
        return self

    @BaseElement._run_after_window_creation
    def update_small_clear_buttons(self,**kwargs) -> Self:
        """
        Evoke .update on every input-element
        :param kwargs:
        :return:
        """
        for elem in self._small_clear_button_elements:
            elem._update_initial(**kwargs)
        return self

    def clear_all_values(self, throw_default_event: bool = False) -> Self:
        """
        Does what it says
        :return:
        """
        for elem in self._input_elements:
            elem.value = ""

        if throw_default_event:
            self.throw_default_event()

        return self

    def set_focus(self) -> Self:
        """
        Focus the first row of this element
        :return:
        """
        self._input_elements[0].set_focus()
        return self



