import tkinter as tk
from SwiftGUI import BaseWidget

class Spacer(BaseWidget):
    """
    Spacer with a certain width in pixels
    """
    _tk_widget_class = tk.Frame

    def __init__(
            self,
            width:int = None,
            height:int = None,
    ):
        super().__init__()

        self._tk_kwargs = {
            "width":width,
            "height":height,
        }
