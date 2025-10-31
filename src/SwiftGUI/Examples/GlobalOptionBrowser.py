from collections.abc import Iterable
from typing import Hashable
import SwiftGUI as sg
from SwiftGUI.GlobalOptions import all_option_classes


class global_option_browser(sg.BasePopup):

    def __init__(self):

        all_options = set()
        for cls in all_option_classes:
            all_options.update(cls._provides)
        print(all_options)

        for cls in all_option_classes:
            cls._fetch(all_options)

        layout_left = sg.Frame([
            [
                # sg.In(
                #     expand= True
                # )
            ],[
                my_table := sg.Table(
                    [[x] for x in all_option_classes],
                    headings= ["Classes"],
                    column_width= [70],
                    key_function= self._select_class,
                    default_event= True,
                ).sort(0, str),
            ]
        ])

        self._all_classes_table = my_table

        layout_middle = sg.Frame([
            [
                # sg.In(
                #     expand= True
                # )
            ],[
                my_table := sg.Table(
                    [[i, ""] for i in all_options],
                    headings= ["Provided option", "Value"],
                    column_width= [40, 20],
                ).sort(),
            ]
        ])

        self._provided_table = my_table

        layout_right = sg.Frame([
            [
                # sg.In(
                #     expand= True
                # )
            ],[
                my_table := sg.Table(
                    [[i, ""] for i in all_options],
                    headings= ["Available option", "Value"],
                    column_width= [40, 20],
                ).sort(),
            ]
        ])

        self._available_table = my_table

        layout_inheritance = sg.Frame([
            [
                # sg.In(
                #     expand= True
                # )
            ],[
                my_table := sg.Table(
                    headings= ["Inherits from"],
                    column_width= [70],
                    key_function= self._select_class,
                    default_event= True,
                )
            ]
        ])

        self._inherits_table = my_table

        layout = [
            [
                layout_left,
            ],[
                sg.Button(
                    "Clear selection",
                    key_function= self._clear_selection
                )
            ],[
                layout_inheritance,
                layout_middle,
                layout_right,
            ]
        ]

        super().__init__(
            layout,
        )

    def _event_loop(self, e: Hashable, v: sg.ValueDict):
        ...

    def _select_class(self, val: list[sg.GlobalOptions.DEFAULT_OPTIONS_CLASS]):
        if val is None:
            return
        cls = val[0]

        refresh_inherit = True
        if self._all_classes_table.index is None or not cls is self._all_classes_table.value[0]:
            refresh_inherit = False
        #     self._all_classes_table.set_index(self._all_classes_table.index_of([cls]))
        #     self._all_classes_table.see_selection()
        #     return

        self._provided_table.filter(key= lambda a: a in cls._provides, by_column= 0)
        for row in self._provided_table.table_elements:
            row[1] = cls._values.get(row[0])

        self._available_table.filter(key= lambda a: a in cls._values.keys(), by_column= 0)
        for row in self._available_table.table_elements:
            row[1] = cls._values.get(row[0])

        if refresh_inherit:
            self._inherits_table.overwrite_table(self._tablefy(cls.__mro__[:-1]))

    def _clear_selection(self):
        self._provided_table.reset_filter()
        self._all_classes_table.reset_filter()
        self._available_table.reset_filter()
        self._inherits_table.overwrite_table([])

        self._provided_table.set_index()
        self._all_classes_table.set_index()
        self._available_table.set_index()
        self._inherits_table.set_index()

    @staticmethod
    def _tablefy(my_list: Iterable) -> list[list]:
        return list(map(lambda a:[a], my_list))
