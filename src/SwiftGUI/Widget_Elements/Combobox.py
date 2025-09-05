from tkinter import ttk
from typing import Any, Iterable, Callable
from SwiftGUI.Compat import Self

from SwiftGUI import GlobalOptions, BaseWidgetTTK, Literals, Color


class Combobox(BaseWidgetTTK):
    tk_widget:ttk.Combobox
    _tk_widget:ttk.Combobox
    _tk_widget_class:type = ttk.Combobox # Class of the connected widget
    defaults = GlobalOptions.Combobox

    _styletype:str = "TCombobox"

    # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/ttk-Notebook.html
    def __init__(
            self,
            values: Iterable[str] = tuple(),
            /,
            key: Any = None,
            key_function: Callable | Iterable[Callable] = None,
            default_event: bool = None,

            default_value: str = None,

            cursor: Literals.cursor = None,

            # background_color: str | Color = None,
            # background_color_active: str | Color = None,

            # text_color: str | Color = None,
            # text_color_active: str | Color = None,

            disabled: bool = None,
            can_change_text: bool = None,

            exportselection: bool = None,

            # Todo: validate,
            #  validatecommand,

            height: int = None,
            width: int = None,

            justify: Literals.left_center_right = None,

            takefocus: bool = None,

            # Add here
            expand: bool = None,
            expand_y: bool = None,
            tk_kwargs: dict[str:Any]=None
    ):
        super().__init__(key=key,tk_kwargs=tk_kwargs,expand=expand, expand_y = expand_y)

        values = tuple(values)
        if default_value is None and values:
            default_value = values[0]

        self._key_function = key_function

        self._default_event = default_event
        self._event_function = lambda *_:None   # Placeholder

        self._prev_value = default_value

        self._update_initial(
            default_value = default_value,
            values = values,
            cursor = cursor,
            exportselection = exportselection,
            height = height,
            width = width,
            justify = justify,
            takefocus = takefocus,
            disabled = disabled,
            can_change_text = can_change_text,
        )

    _tab_texts: dict[Any, str]
    _background_color_tabs_active = None   # If this stays None, normal background_color will be applied
    def _update_special_key(self,key:str,new_val:Any) -> bool|None:
        match key:
            case "values":
                if new_val:
                    self._tk_kwargs["values"] = tuple(new_val)
                else:
                    self._tk_kwargs["values"] = tuple()
                return False
            case "background_color":
                self._map_ttk_style(
                    background=[("!active", new_val)]
                )
            case "background_color_active":
                self._map_ttk_style(
                    background=[("active", new_val)]
                )

            case "text_color":
                self._map_ttk_style(
                    arrowcolor=[("!active", new_val)]
                )
            case "text_color_active":
                self._map_ttk_style(
                    arrowcolor=[("active", new_val)]
                )

            case "default_event":
                self._default_event = new_val

            case "disabled":
                if not self.window:
                    self.update_after_window_creation(disabled = new_val)
                    return True
                self.tk_widget.state(["disabled" if new_val else "!disabled"])

            case "can_change_text":
                if not self.window:
                    self.update_after_window_creation(can_change_text=new_val)
                    return True
                self.tk_widget.state(["!readonly" if new_val else "readonly"])

            case _:
                return super()._update_special_key(key, new_val)

        return True

    _prev_value: str    # Value of last callback
    def _value_change_callback(self, *_):
        if self.value == self._prev_value:
            return

        self._prev_value = self.value

        if self._default_event:
            self._event_function()

    def set_value(self,val:Any):
        self._prev_value = val  # So no event gets called
        super().set_value(val)

    def _personal_init_inherit(self):
        self._event_function = self.window.get_event_function(self, self.key, self._key_function)
        self._set_tk_target_variable(default_key="default_value", kwargs_key= "textvariable")
        self._tk_target_value.trace_add("write", self._value_change_callback)

    def init_window_creation_done(self):
        super().init_window_creation_done()
