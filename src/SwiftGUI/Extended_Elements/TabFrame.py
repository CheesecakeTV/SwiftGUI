import tkinter as tk
from collections.abc import Iterable
from typing import Any, Callable
from SwiftGUI.Compat import Self

from SwiftGUI import BaseElement, GlobalOptions, Literals, Color, Frame
from SwiftGUI.Widget_Elements.Notebook import Notebook


class TabFrame(Frame):
    _tk_widget_class: type[tk.Frame] = tk.Frame  # Class of the connected widget
    defaults = GlobalOptions.TabFrame

    def __init__(
            self,
            layout: Iterable[Iterable[BaseElement]],
            /,
            text: str = None,
            fake_key: str = None,
            default_event: bool = False,

            key: str = None,
            key_function: Callable | Iterable[Callable] = None,

            # Normal sg.Frame-options
            alignment: Literals.alignment = None,

            apply_parent_background_color: bool = None,
            pass_down_background_color: bool = None,
            borderwidth: int = None,
            cursor: Literals.cursor = None,

            background_color: str | Color = None,
            highlightbackground_color: Color | str = None,
            highlightcolor: Color | str = None,
            highlightthickness: int = None,

            padx: int = None,
            pady: int = None,

            relief: Literals.relief = None,

            takefocus: bool = None,

            expand: bool = False,
            expand_y: bool = False,

            # Add here
            tk_kwargs: dict[str:Any]=None,
    ):
        """

        :param layout:
        :param text:
        :param fake_key:
        :param default_event:
        :param key:
        :param key_function:
        :param alignment:
        :param apply_parent_background_color:
        :param pass_down_background_color:
        :param borderwidth:
        :param cursor:
        :param background_color:
        :param highlightbackground_color:
        :param highlightcolor:
        :param highlightthickness:
        :param padx:
        :param pady:
        :param relief:
        :param takefocus:
        :param expand:
        :param expand_y:
        :param tk_kwargs:
        """

        super().__init__(
            layout,
            key = key,
            alignment = alignment,
            expand = expand,
            expand_y = expand_y,
            background_color = background_color,
            apply_parent_background_color = apply_parent_background_color,
            pass_down_background_color = pass_down_background_color,
            borderwidth = borderwidth,
            cursor = cursor,
            highlightbackground_color = highlightbackground_color,
            highlightcolor = highlightcolor,
            highlightthickness = highlightthickness,
            relief = relief,
            takefocus = takefocus,
            tk_kwargs = tk_kwargs,
            padx = padx,
            pady = pady,
        )

        if fake_key is None:
            if key is not None:
                fake_key = key
            elif text is not None:
                fake_key = text

        self.fake_key = fake_key
        assert fake_key is not None, "You have to supply a fake_key, or a key to every TabFrame. fake_key only has to be unique inside the corresponding sg.Notebook!"

        if text is None:
            text = self.fake_key

        self.text = text

        self._myNotebook: Notebook | None = None

        if default_event:
            self._bind_event_to_tab(key=key, key_function=key_function)

    @BaseElement._run_after_window_creation
    def select(self) -> Self:
        """
        Select this tab in the sg.Notebook
        :return:
        """
        self._myNotebook.value = self.fake_key
        return self

    def is_selected(self) -> bool:
        """
        True, if this tab is currently open
        :return:
        """
        return self._myNotebook.value == self.fake_key

    @BaseElement._run_after_window_creation
    def _bind_event_to_tab(self, key_extention:str | Any=None, key:Any=None, key_function:Callable|Iterable[Callable]=None) -> Self:
        """
        When this tab gets opened, the specified event will be called.

        :param key_extention:
        :param key:
        :param key_function:
        :return:
        """
        self._myNotebook.bind_event_to_tab(self.fake_key, key_function= key_function, key_extention= key_extention, key = key)
        return self

    def __matmul__(self, other: Notebook):
        """
        Attach the corresponding notebook
        :param other:
        :return:
        """
        self._myNotebook = other

    def init_window_creation_done(self):
        super().init_window_creation_done()
