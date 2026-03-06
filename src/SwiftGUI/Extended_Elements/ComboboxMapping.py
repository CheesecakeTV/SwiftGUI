import tkinter as tk
from tkinter import colorchooser
from collections.abc import Iterable, Callable
from typing import Literal, Any, Hashable, Mapping

from SwiftGUI import GlobalOptions, Literals, Color, Combobox
from SwiftGUI.Compat import Self
from SwiftGUI.Widget_Elements.Button import Button

import logging

logger = logging.getLogger("SwiftGUI.ComboboxMapping")

class ComboboxMapping(Combobox):
    """
    Small Element to create a button that lets you chose a color
    """
    def __init__(
            self,
            choices: Mapping[Hashable, Any] = None,
            *,
            key: Hashable = None,
            key_function: Callable | Iterable[Callable] = None,
            default_event: bool = None,

            default_value: str = None,

            cursor: Literals.cursor = None,
            insertbackground: str | Color = None,

            background_color: str | Color = None,
            background_color_disabled: str | Color = None,
            selectbackground_color: str | Color = None,

            text_color: str | Color = None,
            text_color_disabled: str | Color = None,
            select_text_color: str | Color = None,

            fonttype: str = None,
            fontsize: int = None,
            font_bold: bool = None,
            font_italic: bool = None,
            font_underline: bool = None,
            font_overstrike: bool = None,

            button_background_color= None,
            button_background_color_active= None,

            arrow_color= None,
            arrow_color_active= None,

            disabled: bool = None,

            exportselection: bool = None,

            height: int = None,
            width: int = None,

            justify: Literals.left_center_right = None,

            takefocus: bool = None,

            # Add here
            expand: bool = None,
            expand_y: bool = None,
            tk_kwargs: dict[str:Any]=None
    ):
        """
        A lot of options are the same with sg.Input

        :param choices: All possible values in the list
        :param key:
        :param key_function:
        :param default_event:
        :param default_value:
        :param cursor:
        :param insertbackground:
        :param background_color:
        :param background_color_disabled:
        :param selectbackground_color:
        :param text_color:
        :param text_color_disabled:
        :param select_text_color:
        :param fonttype:
        :param fontsize:
        :param font_bold:
        :param font_italic:
        :param font_underline:
        :param font_overstrike:
        :param button_background_color:
        :param button_background_color_active: Button-color when the button is pressed down
        :param arrow_color:
        :param arrow_color_active: Button-arror-color when the button is pressed down
        :param disabled:
        :param exportselection:
        :param height:
        :param width:
        :param justify:
        :param takefocus:
        :param expand:
        :param expand_y:
        :param tk_kwargs:
        """

        if choices is None:
            choices = dict()

        if default_value is None:
            if choices:
                default_value = next(iter(choices.keys()))
            else:
                default_value = ""

        self._choices = choices

        super().__init__(
            key=key,
            key_function=key_function,
            default_event=default_event,
            default_value = default_value,
            choices = choices,
            cursor = cursor,
            exportselection = exportselection,
            height = height,
            width = width,
            justify = justify,
            takefocus = takefocus,
            disabled = disabled,
            can_change_text = False,
            background_color = background_color,
            background_color_disabled = background_color_disabled,
            selectbackground_color = selectbackground_color,
            text_color = text_color,
            text_color_disabled = text_color_disabled,
            select_text_color = select_text_color,
            button_background_color = button_background_color,
            button_background_color_active= button_background_color_active,
            arrow_color = arrow_color,
            arrow_color_active= arrow_color_active,

            fonttype=fonttype,
            fontsize=fontsize,
            font_bold=font_bold,
            font_italic=font_italic,
            font_underline=font_underline,
            font_overstrike=font_overstrike,

            insertbackground = insertbackground,
            expand=expand,
            expand_y=expand_y,
            tk_kwargs=tk_kwargs,
        )

    def _update_special_key(self,key:str,new_val:Any) -> bool|None:
        match key:
            case "choices":
                if new_val:
                    self._choices = new_val
                    self._tk_kwargs["values"] = tuple(map(str, new_val.keys()))
                else:
                    self._tk_kwargs["values"] = tuple()

            case _:
                return super()._update_special_key(key, new_val)

        return True

    def _get_value(self) -> Any:
        """
        Asymmectric in this case!!!
        get_value returns something set_value doesn't want
        :return:
        """
        val = super()._get_value()
        return self._choices.get(val)

    def set_value(self, val: Hashable) -> Self:
        if not val in self._choices:
            logger.error(f"You tried to set a ComboboxMapping with a key that isn't part of the choices.\n"
                         f"I am {self} and my choices are {self._choices}.\n"
                         f"You tried to set the value to {val}.")
            return self

        super().set_value(val)
        return self

    def to_json(self) -> Any:
        # Return the raw string instead of the value behind it
        return super()._get_value()

    choices: Mapping[Hashable, Any]
    @property
    def choices(self) -> Mapping[Hashable, Any]:
        """
        Elements in the drop-down-menu
        :return:
        """
        return self._choices.copy()

    @choices.setter
    def choices(self, new_val: Mapping[Hashable, Any]):
        """

        :param new_val:
        :return:
        """
        self.set_choices(new_val)

    @Combobox._run_after_window_creation
    def set_choices(self, new_val: Mapping[Hashable, Any]) -> Self:
        """
        Change the elements in the drop-down-menu

        :param new_val:
        :return:
        """
        self.update(choices=new_val)
        return self

