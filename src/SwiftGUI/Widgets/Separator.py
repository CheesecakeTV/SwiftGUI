import tkinter.ttk as ttk
from typing import Literal
from SwiftGUI import ElementFlag, BaseWidget

class Separator(BaseWidget):
    _tk_widget_class = ttk.Separator

    def __init__(self,orient:Literal["vertical","horizontal"]):
        super().__init__(key=None,tk_kwargs={"orient":orient})

class VerticalSeparator(Separator):
    def __init__(self):
        super().__init__(orient="vertical")

    def _personal_init_inherit(self):
        self._insert_kwargs["fill"] = "y"

class HorizontalSeparator(Separator):
    def __init__(self):
        super().__init__(orient="horizontal")

    def _personal_init_inherit(self):
        self._insert_kwargs["fill"] = "x"
        self._insert_kwargs["expand"] = True

        self.add_flags(ElementFlag.EXPAND_ROW)

