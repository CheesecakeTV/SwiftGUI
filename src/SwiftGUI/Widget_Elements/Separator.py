import tkinter as tk
from typing import Any
from SwiftGUI import ElementFlag, BaseWidget, Color, GlobalOptions


class Separator(BaseWidget):
    _tk_widget_class = tk.Frame

    _grab_anywhere_on_this = True

    defaults = GlobalOptions.Separator

    _transfer_keys = {
        "color":"bg"
    }

    def __init__(
            self,
            key: Any = None,
            color: str | Color = None,
            weight: int = None,
    ):
        super().__init__(key=key)
        self._update_initial(color=color, weight=weight)
        self._insert_kwargs["pady"] = 3
        self._insert_kwargs["padx"] = 3

    def _update_special_key(self,key:str,new_val:any) -> bool|None:
        if key == "weight":
            self._update_initial(height=new_val, width=new_val)
            return True

        return False

class VerticalSeparator(Separator):
    defaults = GlobalOptions.SeparatorVertical
    def __init__(
            self,
            key: Any = None,
            color: str | Color = None,
            weight: int = None,
    ):
        super().__init__(
            key=key,
            color = color,
            weight = weight,
        )

    def _personal_init_inherit(self):
        self._insert_kwargs["fill"] = "y"

class HorizontalSeparator(Separator):
    defaults = GlobalOptions.SeparatorHorizontal
    def __init__(
            self,
            key: Any = None,
            color: str | Color = None,
            weight: int = None,
    ):
        super().__init__(
            key=key,
            color = color,
            weight = weight,
        )

    def _personal_init_inherit(self):
        self._insert_kwargs["fill"] = "x"
        self._insert_kwargs["expand"] = True

        self.add_flags(ElementFlag.EXPAND_ROW)

