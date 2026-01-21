import tkinter as tk
from collections.abc import Iterable
from typing import Any, Hashable
from SwiftGUI.Compat import Self

from SwiftGUI import BaseElement, GlobalOptions, Literals, Color, Frame, Text


class LabelFrame(Frame):
    """
    Copy this class ot create your own Widget
    """
    _tk_widget_class: type[tk.LabelFrame] = tk.LabelFrame  # Class of the connected widget
    defaults = GlobalOptions.LabelFrame

    _transfer_keys = {
        "background_color_disabled": "disabledbackground",
        "background_color_readonly": "readonlybackground",
        "background_color": "background",
        "text_color": "foreground",
        "text_color_disabled": "disabledforeground",
        "highlightbackground_color": "highlightbackground",
        "selectbackground_color": "selectbackground",
        "select_text_color": "selectforeground",
        "pass_char": "show",
    }

    def __init__(
            self,
            layout: Iterable[Iterable[BaseElement]],
            *,
            key: Hashable = None,

            text: str = None,
            no_label: bool = None,

            fonttype: str = None,
            fontsize: int = None,
            font_bold: bool = None,
            font_italic: bool = None,
            font_underline: bool = None,
            font_overstrike: bool = None,
            text_color: Color | str = None,

            labelanchor: Literals.tabposition = None,

            # Normal Frame
            alignment: Literals.alignment = None,
            expand: bool = False,
            expand_y: bool = False,
            padx: int = None,
            pady: int = None,
            background_color: str | Color = None,
            apply_parent_background_color: bool = None,
            pass_down_background_color: bool = None,
            borderwidth: int = None,
            cursor: Literals.cursor = None,
            highlightbackground_color: Color | str = None,
            highlightcolor: Color | str = None,
            highlightthickness: int = None,
            relief: Literals.relief = None,
            takefocus: bool = None,
            tk_kwargs: dict[str:Any] = None,
    ):
        """
        Most options are the same in sg.Text, or sg.Frame

        :param layout:
        :param key:
        :param text:
        :param no_label: True, if the text should be hidden
        :param fonttype:
        :param fontsize:
        :param font_bold:
        :param font_italic:
        :param font_underline:
        :param font_overstrike:
        :param text_color:
        :param labelanchor: Position of the text relative to the frame
        :param alignment:
        :param expand:
        :param expand_y:
        :param padx:
        :param pady:
        :param background_color:
        :param apply_parent_background_color:
        :param pass_down_background_color:
        :param borderwidth:
        :param cursor:
        :param highlightbackground_color:
        :param highlightcolor:
        :param highlightthickness:
        :param relief:
        :param takefocus:
        :param tk_kwargs:
        """
        self._element = Text(relief="flat")    # Todo: Let the user pass an element
        self._element.defaults = self.defaults

        self._no_label = no_label

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

        self.link_background_color(self._element)

        self._update_initial(labelanchor=labelanchor, text=text, text_color=text_color, fonttype=fonttype,
                             fontsize=fontsize, font_bold=font_bold, font_italic=font_italic,
                             font_underline=font_underline, font_overstrike=font_overstrike)

    _keys_to_pass_to_element: list[str] = [ # All the keys that gets passed to update of the label-element
        "text",
        "text_color",
        "fonttype",
        "fontsize",
        "fontcolor",
        "font_bold",
        "font_italic",
        "font_underline",
        "font_overstrike",
    ]

    def set_value(self, val: str) -> Self:
        self._element.value = val
        return self

    def _get_value(self) -> Self:
        return self._element.value

    def _update_initial(self, **kwargs) -> Self:
        pass_to_element = dict()
        kwargs_copy: dict = kwargs.copy()
        for key,val in kwargs_copy.items():
            if key in self._keys_to_pass_to_element:
                pass_to_element[key] = val
                del kwargs[key]

        super()._update_initial(**kwargs)
        self._element._update_initial(**pass_to_element)
        return self

    def init_window_creation_done(self):
        self._element._init(self, self.window)
        super().init_window_creation_done()

        if not self._no_label:
            self._update_initial(labelwidget=self._element.tk_widget)

