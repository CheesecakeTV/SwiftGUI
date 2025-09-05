import tkinter as tk
from tkinter import ttk
from typing import Literal, Any, Self

from SwiftGUI import ElementFlag, BaseWidget, GlobalOptions, BaseWidgetTTK


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

            # Add here
            expand: bool = None,
            expand_y: bool = None,
            tk_kwargs: dict[str:Any]=None
    ):
        super().__init__(key=key,tk_kwargs=tk_kwargs,expand=expand, expand_y = expand_y)

        self._update_initial(

        )

    _tab_texts: dict[Any, str]
    _background_color_tabs_active = None   # If this stays None, normal background_color will be applied
    def _update_special_key(self,key:str,new_val:Any) -> bool|None:
        match key:
            case "tabposition":
                self._config_ttk_style(tabposition=new_val)
            case "apply_parent_background_color":
                if new_val:
                    self.add_flags(ElementFlag.APPLY_PARENT_BACKGROUND_COLOR)
                else:
                    self.remove_flags(ElementFlag.APPLY_PARENT_BACKGROUND_COLOR)
            case "tab_texts":
                self._tab_texts.update(new_val)
            case "background_color":
                self._config_ttk_style(background=new_val)
                #self._config_ttk_style(background=new_val, style_ext = "Tab")

                for tab in self._elements:
                    if tab.has_flag(ElementFlag.APPLY_PARENT_BACKGROUND_COLOR):
                        tab._update_initial(background_color=new_val)

                if self._background_color_tabs_active is None:  # If no active tab-color, apply the background color. Looks better
                    self._map_ttk_style("Tab", background=[("selected", new_val)])

            case "background_color_tabs":
                self._map_ttk_style("Tab", background = [("!selected", new_val)])
            case "background_color_tabs_active":
                self._background_color_tabs_active = new_val
                self._map_ttk_style("Tab", background = [("selected", self.defaults.single("background_color", new_val))])

            case "text_color_tabs":
                self._map_ttk_style("Tab", foreground=[("!selected", new_val)])
            case "text_color_tabs_active":
                self._map_ttk_style("Tab", foreground=[("selected", new_val)])

            case "fonttype_tabs":
                self._fonttype_tabs = self.defaults.single("fonttype", self.defaults.single(key,new_val))
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "fontsize_tabs":
                self._fontsize_tabs = self.defaults.single("fontsize", self.defaults.single(key,new_val))
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "font_bold_tabs":
                self._bold_tabs = self.defaults.single("font_bold", self.defaults.single(key,new_val))
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "font_italic_tabs":
                self._italic_tabs = self.defaults.single("font_italic", self.defaults.single(key,new_val))
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "font_underline_tabs":
                self._underline_tabs = self.defaults.single("font_underline", self.defaults.single(key,new_val))
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "font_overstrike_tabs":
                self._overstrike_tabs = self.defaults.single("font_overstrike", self.defaults.single(key,new_val))
                self.add_flags(ElementFlag.UPDATE_FONT)


            case "borderwidth":
                self._config_ttk_style(borderwidth=new_val)
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
