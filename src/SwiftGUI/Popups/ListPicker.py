from collections.abc import Iterable, Hashable

import SwiftGUI as sg

# Todo: Turn this into a combined element
class list_picker(sg.BasePopup, tuple):
    text_available = "Available"
    text_picked = "Used"
    text_filter = "Filter: "
    text_done = "Done"
    text_cancel = "Cancel"

    def __init__(
            self,
            possible_values: Iterable[Hashable] = tuple(),
            *,
            title: str = "",
            default_selection: Iterable[Hashable] = tuple(),
            enable_filter: bool = True,
            button_fontsize: int = None,
            # Todo: max_selections: int = None, # How many can be selected at once
            **kwargs,
    ):
        possible_values = set(possible_values)
        default_selection = set(default_selection)
        #self.max_selections = max_selections if max_selections else (len(possible_values) + len(default_selection))

        possible_values = possible_values.difference(default_selection)

        button_fontsize = sg.Button.defaults.single("fontsize", button_fontsize)

        middle = sg.Frame([
            [
                sg.Button(
                    "►",
                    key="Pick",
                    width=5,
                    fontsize= button_fontsize,
                )
            ],[
                sg.Button(
                    "►►",
                    key= "PickAll",
                    width=5,
                    fontsize=button_fontsize,
                )
            ],[
                sg.HSep()
            ],[
                sg.Button(
                    "◄",
                    key="Unpick",
                    width=5,
                    fontsize=button_fontsize,
                )
            ], [
                sg.Button(
                    "◄◄",
                    key="UnpickAll",
                    width=5,
                    fontsize=button_fontsize,
                )
            ]
        ])

        main_layout = sg.Frame([
            [
                available := sg.Table(
                    map(lambda a:[a], possible_values),
                    headings= (self.text_available, ),
                    selectmode= "extended",
                ).bind_event(
                    sg.Event.ClickDoubleLeft,
                    key= "Pick",
                ),
                middle,
                chosen := sg.Table(
                    map(lambda a: [a], default_selection),
                    headings=(self.text_picked, ),
                    selectmode = "extended",
                ).bind_event(
                    sg.Event.ClickDoubleLeft,
                    key= "Unpick",
                ),
            ]
        ])
        self.available = available
        self.chosen = chosen

        filter_frame = sg.Frame([
            [
                sg.T(self.text_filter),
                filter_input := sg.Input(
                    expand=True,
                    key_function=self._apply_filter,
                    default_event=True,
                ).bind_event(
                    sg.Event.KeyEnter,
                    key_function= [
                        lambda val: self._move_all(self.available, self.chosen), # Move all over
                        lambda : filter_clear_button.push_once(),   # Clear input and filter by "pressing" the x-button
                    ]
                ),
                filter_clear_button := sg.Button(
                    "x",
                    width=2,
                    key_function=[
                        lambda :filter_input.set_value(""), # Clear input
                        lambda :self._apply_filter(),   # Reset filter
                    ],
                    fontsize = button_fontsize,
                )
        ],[
                sg.HSep()
            ]
        ], expand=True)

        layout = [
            [
                filter_frame if enable_filter else sg.T()
            ], [
                main_layout
            ],[
                sg.Button(
                    self.text_done,
                    key= "Done",
                    fontsize= button_fontsize,
                ),
                sg.Button(
                    self.text_cancel,
                    key= "Cancel",
                    fontsize=button_fontsize,
                )
            ]
        ]

        super().__init__(
            layout,
            default= tuple(default_selection),
            title = title,
            **kwargs
        )

    def _apply_filter(self, val: str = None):
        if not val:
            self.available.reset_filter()
            self.chosen.reset_filter()
            return

        try:
            self.available.filter(lambda row: val.casefold() in str(row).casefold(), by_column=0)
            self.chosen.filter(lambda row: val.casefold() in str(row).casefold(), by_column=0)
        except AttributeError:
            raise TypeError("Never use enable_filter=True on types that can't be converted to string!")

    def _event_loop(self, e: Hashable, v: sg.ValueDict):

        if e == "Pick":
            self._move_rows(self.available, self.chosen)

        if e == "PickAll":
            self._move_all(self.available, self.chosen)

        if e == "Unpick":
            self._move_rows(self.chosen, self.available)

        if e == "UnpickAll":
            self._move_all(self.chosen, self.available)

        if e == "Done":
            # Return everything from the chosen table
            self.chosen.reset_filter()
            self.done(
                tuple(map(lambda a:a[0], self.chosen.all_remaining_rows))
            )

        if e == "Cancel":
            self.done() # Return default selection

    @staticmethod
    def _move_rows(from_t: sg.Table, to_t: sg.Table) -> int:
        qtt = len(to_t.extend(from_t.all_values))

        for i in from_t.all_indexes[::-1]:
            del from_t[i]

        return qtt

    @staticmethod
    def _move_all(from_t: sg.Table, to_t: sg.Table):
        to_t.extend(from_t.all_remaining_rows)
        for i in range(len(from_t.all_remaining_rows)):
            del from_t[0]

