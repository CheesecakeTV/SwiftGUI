import tkinter as tk
from tkinter import ttk
from typing import Any, Iterable, Callable, Hashable

from SwiftGUI.Compat import Self

from SwiftGUI import GlobalOptions, BaseWidgetTTK, Literals, Color, ElementFlag


class Progressbar(BaseWidgetTTK):
    tk_widget:ttk.Progressbar
    _tk_widget:ttk.Progressbar
    _tk_widget_class:type = ttk.Progressbar # Class of the connected widget
    defaults = GlobalOptions.Progressbar

    _styletype:str = "Horizontal.TProgressbar"

    _orient = "horizontal"

    _transfer_keys = {
        "number_max": "maximum",
    }

    # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/ttk-Notebook.html
    def __init__(
            self,
            default_value: float = None,
            /,
            key: Hashable = None,
            number_max: float = None,

            cursor: Literals.cursor = None,

            bar_color: str | Color = None,
            background_color: str | Color = None,

            takefocus: bool = None,
            mode: Literals.progress_mode = None,

            # Add here
            expand: bool = None,
            expand_y: bool = None,
            tk_kwargs: dict[str:Any]=None
    ):
        super().__init__(key=key,tk_kwargs=tk_kwargs,expand=expand, expand_y = expand_y)

        self._update_initial(
            bar_color = bar_color,
            background_color = background_color,
            default_value = default_value,
            takefocus = takefocus,
            cursor = cursor,
            orient = self._orient,
            mode = mode,
            number_max = number_max,
        )


    def _update_special_key(self,key:str,new_val:Any) -> bool|None:
        # if not self.window and key in ["background_color", "text_color", "selectbackground_color", "select_text_color"]:    # These can only be handled once the element exists
        #     self.update_after_window_creation(**{key: new_val})
        #     return True

        match key:
            case "default_value":
                if not self.window:
                    self.update_after_window_creation(default_value = new_val)
                    return True
                self.set_value(new_val)

            case "background_color":
                self._config_ttk_style(troughcolor= new_val)

            case "bar_color":
                self._config_ttk_style(background= new_val)

            case _:
                return super()._update_special_key(key, new_val)

        return True

    def _personal_init_inherit(self):
        self._set_tk_target_variable(default_key="default_value", kwargs_key= "variable", value_type= tk.DoubleVar)

    @BaseWidgetTTK._run_after_window_creation
    def start(self, interval: float = 0.05) -> Self:
        """
        Start increasing the value by 1 every interval
        :param interval: interval in seconds
        :return:
        """
        interval = int(interval * 1000)
        self.tk_widget.start(interval)
        return self

    @BaseWidgetTTK._run_after_window_creation
    def stop(self) -> Self:
        self.tk_widget.stop()
        return self

    @BaseWidgetTTK._run_after_window_creation
    def step(self, step_length: float = 1) -> Self:
        self.tk_widget.step(step_length)
        return self

class ProgressbarVertical(Progressbar):
    _styletype:str = "Vertical.TProgressbar"
    _orient = "vertical"

