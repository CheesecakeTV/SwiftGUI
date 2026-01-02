import tkinter as tk
from typing import Hashable

from SwiftGUI import BaseWidget, ElementFlag, GlobalOptions


class Spacer(BaseWidget):
    """
    Spacer with a certain width in pixels
    """
    _tk_widget_class = tk.Frame
    defaults = GlobalOptions.Common_Background

    _grab_anywhere_on_this = True

    _transfer_keys = {
        "background_color": "bg"
    }

    def __init__(
            self,
            width: int = None,
            height: int = None,
            *,
            key: Hashable = None,
            #expand: bool = None,
            expand_y: bool = None,
    ):
        super().__init__(key= key, expand_y = expand_y)

        self.add_flags(ElementFlag.APPLY_PARENT_BACKGROUND_COLOR)

        self._tk_kwargs = {
            "width":width,
            "height":height,
            "background":"",
        }
