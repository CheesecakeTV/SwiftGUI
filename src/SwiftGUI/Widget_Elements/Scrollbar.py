import tkinter as tk
from tkinter import ttk
from typing import Any, Hashable
from SwiftGUI.Compat import Self

from SwiftGUI import BaseWidget, GlobalOptions, BaseWidgetTTK, Literals, Color


class Scrollbar(BaseWidgetTTK):
    tk_widget:ttk.Scrollbar
    _tk_widget:ttk.Scrollbar
    _tk_widget_class:type = ttk.Scrollbar # Class of the connected widget
    defaults = GlobalOptions.Scrollbar

    _styletype:str = "Vertical.TScrollbar"
    _orient: str = "vertical"

    # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/ttk-Notebook.html
    def __init__(
            self,
            /,
            key: Hashable = None,

            cursor: Literals.cursor = None,

            background_color: str | Color = None,
            background_color_active: str | Color = None,

            text_color: str | Color = None,
            text_color_active: str | Color = None,

            troughcolor: str | Color = None,

            # Add here
            expand: bool = False,
            expand_y: bool = True,
            tk_kwargs: dict[str:Any]=None,
    ):
        super().__init__(key=key,tk_kwargs=tk_kwargs,expand=expand, expand_y = expand_y)

        self._update_initial(
            cursor = cursor,
            background_color = background_color,
            background_color_active = background_color_active,

            text_color = text_color,
            text_color_active = text_color_active,

            troughcolor = troughcolor,

            orient = self._orient,
        )

    def _update_special_key(self,key:str,new_val:Any) -> bool|None:
        match key:
            case "background_color":
                self._map_ttk_style(
                    background=[("!pressed", new_val)]
                )
            case "background_color_active":
                self._map_ttk_style(
                    background=[("pressed", new_val)]
                )

            case "text_color":
                self._map_ttk_style(
                    arrowcolor=[("!pressed", new_val)]
                )
            case "text_color_active":
                self._map_ttk_style(
                    arrowcolor=[("pressed", new_val)]
                )

            case "troughcolor":
                self._config_ttk_style(troughcolor = new_val)
                return True

            case _:
                return super()._update_special_key(key, new_val)

        return True

    @BaseWidgetTTK._run_after_window_creation
    def bind_to_element(self, elem: BaseWidget) -> Self:
        """
        Bind this scrollbar to its element/widget
        :param elem:
        :return:
        """
        elem._update_initial(yscrollcommand=self.tk_widget.set)
        self.tk_widget.configure(command=elem.tk_widget.yview)
        return self

class ScrollbarHorizontal(Scrollbar):
    _styletype:str = "Horizontal.TScrollbar"
    _orient = "horizontal"

    def __init__(
            self,
            /,
            key: Any = None,

            cursor: Literals.cursor = None,

            background_color: str | Color = None,
            background_color_active: str | Color = None,

            text_color: str | Color = None,
            text_color_active: str | Color = None,

            troughcolor: str | Color = None,

            expand: bool = True,
            expand_y: bool = False,
            tk_kwargs: dict[str:Any]=None
    ):
        super().__init__(
            key = key,
            cursor = cursor,
            background_color = background_color,
            background_color_active = background_color_active,
            text_color = text_color,
            text_color_active = text_color_active,
            troughcolor = troughcolor,
            expand = expand,
            expand_y = expand_y,
            tk_kwargs = tk_kwargs,
        )


    @BaseWidgetTTK._run_after_window_creation
    def bind_to_element(self, elem: BaseWidget) -> Self:
        """
        Bind this scrollbar to its element/widget
        :param elem:
        :return:
        """
        elem._update_initial(xscrollcommand=self.tk_widget.set)
        self.tk_widget.configure(command=elem.tk_widget.xview)
        return self
