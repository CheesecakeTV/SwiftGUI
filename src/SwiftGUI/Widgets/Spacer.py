import tkinter as tk
from SwiftGUI import BaseWidget, ElementFlag


class Spacer(BaseWidget):
    """
    Spacer with a certain width in pixels
    """
    _tk_widget_class = tk.Frame

    _transfer_keys = {
        "background_color":"bg"
    }

    def __init__(
            self,
            width:int = None,
            height:int = None,
    ):
        super().__init__()

        self.add_flags(ElementFlag.APPLY_PARENT_BACKGROUND_COLOR)

        self._tk_kwargs = {
            "width":width,
            "height":height,
            "background":"",
        }
