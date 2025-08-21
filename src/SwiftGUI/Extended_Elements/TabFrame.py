import tkinter as tk
from collections.abc import Iterable
from typing import Self

from SwiftGUI import BaseElement, ElementFlag, BaseWidgetContainer, GlobalOptions, Literals, Color, BaseWidget, Frame, \
    Text, font_windows
from SwiftGUI.Widget_Elements.Notebook import Notebook


class TabFrame(Frame):
    """
    Copy this class ot create your own Widget
    """
    _tk_widget_class: type[tk.Frame] = tk.Frame  # Class of the connected widget
    defaults = GlobalOptions.TabFrame

    def __init__(
            self,
            layout: Iterable[Iterable[BaseElement]],
            /,
            text: str = None,
            fake_key: str = None,

            key: str = None,
            alignment: Literals.alignment = None,
            expand: bool = False,
            expand_y: bool = False,
            background_color: str | Color = None,
            apply_parent_background_color: bool = None,
            pass_down_background_color: bool = None,
            borderwidth: int = None,
            cursor: Literals.cursor = None,
            highlightbackground_color: Color | str = None,
            highlightcolor: Color | str = None,
            highlightthickness: int = None,

            padx: int = None,
            pady: int = None,

            relief: Literals.relief = None,

            takefocus: bool = None,

            # Add here
            tk_kwargs: dict[str:any]=None,
    ):
        """

        :param layout:
        :param text: Text on the tab
        :param fake_key: Key to be used by the sg.Notebook
        :param key: Key to be registered into the main window
        :param alignment:
        :param expand:
        :param expand_y:
        :param background_color:
        :param apply_parent_background_color:
        :param pass_down_background_color:
        :param borderwidth:
        :param cursor:
        :param highlightbackground_color:
        :param highlightcolor:
        :param highlightthickness:
        :param padx:
        :param pady:
        :param relief:
        :param takefocus:
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
            fake_key = key

        self.fake_key = fake_key
        assert fake_key is not None, "You have to supply a fake_key, or a key to every TabFrame. fake_key only has to be unique inside the corresponding sg.Notebook!"

        if text is None:
            text = self.fake_key

        self.text = text

        self.myNotebook: Notebook | None = None

    @Frame._run_after_window_creation
    def select(self) -> Self:
        """
        Select this tab in the sg.Notebook
        :return:
        """
        ...

    def __matmul__(self, other: Notebook):
        """
        Attach the corresponding notebook
        :param other:
        :return:
        """
        self.myNotebook = other
