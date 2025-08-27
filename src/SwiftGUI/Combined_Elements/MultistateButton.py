from typing import Any, Callable, Iterable, Self, Literal
from functools import partial

import SwiftGUI as sg


class MultistateButton(sg.BaseCombinedElement):
    _state = 0  # Which button is selected ATM
    defaults = sg.GlobalOptions.MultistateButton

    def __init__(
            self,

            button_texts: Iterable[str] = tuple(),
            button_keys: Iterable[Any] = tuple(),
            default_selection: Any = None,
            default_select_first: bool = None,

            text_color: str | sg.Color = None,
            button_background_color: str | sg.Color = None,
            background_color_active: str | sg.Color = None,
            text_color_active: str | sg.Color = None,

            width: int = None,
            height: int = None,

            can_deselect: bool = None,

            horizontal_orientation: bool = False,

            label_text: str = None,

            key: Any = None,
            key_function: Callable | Iterable[Callable] = None,
            apply_parent_background_color: bool = True
    ):
        frame_type: type(sg.Frame) = sg.Frame
        if label_text:
            frame_type = sg.LabelFrame

        button_texts = list(button_texts)
        button_keys = list(button_keys)

        if not button_keys:
            button_keys = button_texts

        if default_select_first:
            default_selection = button_keys[0]

        self._buttons: dict[Any: sg.Button] = {
            b_key: sg.Button(
                b_text,
                key_function= partial(self._button_callback, key= b_key),
                expand= True,
                expand_y= True,
            ) for b_text, b_key in zip(button_texts, button_keys)
        }

        if horizontal_orientation:
            frame = frame_type([self._buttons.values()])
        else:
            frame = frame_type(
                map(lambda a: [a], self._buttons.values())
            )

        if label_text:
            frame.update_after_window_creation(text = label_text)

        super().__init__(frame = frame, key=key, key_function=key_function, apply_parent_background_color=apply_parent_background_color)

        self._update_initial(
            text_color = text_color,
            text_color_active = text_color_active,
            button_background_color = button_background_color,
            background_color_active = background_color_active,
            can_deselect = can_deselect,
            default_selection = default_selection,
            width = width,
            height = height,
        )

    def __getitem__(self, item: Any) -> sg.Button:
        return self._buttons[item]

    def _update_special_key(self,key:str,new_val:any) -> bool|None:
        match key:
            case "text_color":
                self._text_color = new_val
                return False    # Still use the key
            case "button_background_color":
                self._button_background_color = self.defaults.single("background_color", new_val)
            case "background_color_active":
                self._background_color_active = new_val
                return False  # Still use the key
            case "text_color_active":
                self._text_color_active = new_val
                return False  # Still use the key
            case "can_deselect":
                self._can_deselect = new_val
            case "default_selection":
                if not hasattr(self, "window"):
                    self.update_after_window_creation(default_selection = new_val)
                    return True
                self.value = new_val
            case _:
                return super()._update_special_key(key, new_val)

        return True

    def _update_default_keys(self,kwargs):
        for elem in self._buttons.values():
            elem.update(**kwargs)

    def _button_callback(self, key):
        if key == self._current_val:
            if self._can_deselect:
                self.value = None
                self._throw_event()
            return

        self.value = key
        self._throw_event()

    _current_val = None
    def _get_value(self) -> Any:
        return self._current_val

    def set_value(self, val:Any):
        if self._current_val is not None:
            elem = self._buttons[self._current_val]
            elem.update(relief="raised")
            elem.update(background_color=self._button_background_color)
            elem.update(text_color=self._text_color)

        if not val in self._buttons:
            self._current_val = None
            return

        self._current_val = val
        elem = self._buttons[val]

        elem.update(relief = "sunken")
        elem.update(background_color = self._background_color_active)
        elem.update(text_color = self._text_color_active)


