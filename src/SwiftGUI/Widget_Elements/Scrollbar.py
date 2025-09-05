from tkinter import ttk
from typing import Any
from SwiftGUI.Compat import Self

from SwiftGUI import BaseWidget, GlobalOptions, BaseWidgetTTK, Literals, Color


class Scrollbar(BaseWidgetTTK):
    tk_widget:ttk.Scrollbar
    _tk_widget:ttk.Scrollbar
    _tk_widget_class:type = ttk.Scrollbar # Class of the connected widget
    defaults = GlobalOptions.Scrollbar

    _styletype:str = "Vertical.TScrollbar"

    # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/ttk-Notebook.html
    def __init__(
            self,
            /,
            key: Any = None,

            cursor: Literals.cursor = None,
            #takefocus: bool = None,

            background_color: str | Color = None,
            background_color_active: str | Color = None,

            text_color: str | Color = None,
            text_color_active: str | Color = None,

            troughcolor: str | Color = None,

            # Add here
            expand: bool = None,
            expand_y: bool = None,
            tk_kwargs: dict[str:Any]=None
    ):
        super().__init__(key=key,tk_kwargs=tk_kwargs,expand=expand, expand_y = expand_y)

        self._update_initial(
            cursor = cursor,
            background_color = background_color,
            background_color_active = background_color_active,

            text_color = text_color,
            text_color_active = text_color_active,

            troughcolor = troughcolor,
            #takefocus = takefocus,
        )

    _tab_texts: dict[Any, str]
    _background_color_tabs_active = None   # If this stays None, normal background_color will be applied
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

    def init_window_creation_done(self):
        """Don't touch!"""
        super().init_window_creation_done()

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
