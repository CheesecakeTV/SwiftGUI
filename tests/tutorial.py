from typing import Any, Callable, Iterable, Self
import SwiftGUI as sg
from SwiftGUI import BaseCombinedElement


class Example(sg.BaseCombinedElement):
    defaults = sg.GlobalOptions.DEFAULT_OPTIONS_CLASS  # Change this to attach your own GlobalOption-class to the element

    def __init__(
            self,
            texts: list[str] = None,
            key: Any = None,
            key_function: Callable | Iterable[Callable] = None,
            apply_parent_background_color: bool = None,
    ):
        self._layout = [  # Put the containing layout here

        ]

        for text_now in texts:  # Add the rows one-by-one
            self._layout.append([
                sg.T(  # Same elements as before
                    text_now,
                    width=15,
                    anchor="w",
                ),
                sg.Input(
                    key_function= self.throw_event,  # call self.throw_event when the default-event occurs
                    default_event= True,
                ),
            ])

        self._layout.append(
            [
                sg.Button("Clear", key_function= self.clear_input_elements)
            ]
        )

        super().__init__(
            frame=sg.Frame(self._layout),  # You can use any kind of Frame, e.g. LabelFrame
            key=key,
            key_function=key_function,
            apply_parent_background_color=apply_parent_background_color,
        )

    def _get_value(self) -> any:
        """Returns the value (self.value) of this element"""
        _return = dict()

        for row in self._layout[:-1]:   # Every row but the last one
            _return[row[0].value] = row[1].value
        return _return

    def set_value(self, val: any):
        """Changes the value of this element (self.value = val)"""
        super().set_value(val)

    def init_window_creation_done(self) -> Self:
        """Runs once, after the window was created"""
        super().init_window_creation_done()  # Don't forget this call, very important!
        return self

    def _update_special_key(self, key: str, new_val: any) -> bool | None:
        """
        When calling .update, this method gets called first.
        If it returns anything truethy (like True), execution of .update ends for this key.

        Otherwise, ._update_default_keys gets called for the key.

        In combined elements, you'll most likely use ._update_special_key for every possible key.
        The whole update-routine is kinda complicated, so just stick with this one.
        """
        match key:
            case _:  # No other case covered this key, so let's let's the parent-class handle the rest
                return super()._update_special_key(key, new_val)

        return True  # Key was covered by match, so don't pass it to _update_default_keys

    @BaseCombinedElement._run_after_window_creation
    def clear_input_elements(self):
        for row in self._layout[:-1]:   # Not the last row, it contains buttons
            row[1].value = ""


layout = [
    [
        Example(
            texts = ["Name", "Birthday", "Organization", "Favorite Food"],
            key = "Form"
        )
    ]
]

w = sg.Window(layout)

for e,v in w:
    print(e)    # Form
    print(v)    # {'Form': {'Name': 'Eric', 'Birthday': '', 'Organization': 'SwiftGUI', 'Favorite Food': ''}}
    print() # Empty line

