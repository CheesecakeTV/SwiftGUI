import tkinter as tk
from collections.abc import Iterable

from BaseWidget import BaseWidget,BaseContainer


class Example(BaseWidget):
    """
    Copy this class ot create your own Widget
    """
    tk_widget_class:type = None # Class of the connected widget

    def __init__(
            self,
            # Add here
            tk_args:tuple[any]=tuple(),
            tk_kwargs:dict[str:any]=None
    ):
        super().__init__(tk_args=tk_args,tk_kwargs=tk_kwargs)

        if tk_kwargs is None:
            tk_kwargs = dict()

        self._tk_args = self._tk_args + tk_args # Add anonymous arguments for the widget here
        self._tk_kwargs.update({
            **tk_kwargs
            # Insert named arguments for the widget here
        })

class Text(BaseWidget):
    """
    Copy this class ot create your own Widget
    """
    tk_widget_class:type = tk.Label # Class of the connected widget

    def __init__(
            self,
            # Add here
            text:str = "",

            tk_args:tuple[any]=tuple(),
            tk_kwargs:dict[str:any]=None
    ):
        super().__init__(tk_args=tk_args,tk_kwargs=tk_kwargs)

        if tk_kwargs is None:
            tk_kwargs = dict()

        self._tk_kwargs.update({
            **tk_kwargs,
            "text":text,
        })

class Frame(BaseContainer):
    """
    Copy this class ot create your own Widget
    """
    tk_widget_class:type = tk.Frame # Class of the connected widget

    def __init__(
            self,
            layout:Iterable[Iterable[BaseWidget]],
            # Add here
            tk_args:tuple[any]=tuple(),
            tk_kwargs:dict[str:any]=None
    ):
        super().__init__(tk_args=tk_args,tk_kwargs=tk_kwargs)

        self.contains = layout

        self._tk_args = self._tk_args + tk_args # Add anonymous arguments for the widget here
        if tk_kwargs is None:
            tk_kwargs = dict()
        self._tk_kwargs.update({
            **tk_kwargs
            # Insert named arguments for the widget here
        })

T = Text
Label = Text


if __name__ == '__main__':
    # Test
    root = tk.Tk()
    root.grid()

    layout = [
        [
            Text("Hallo"),
            T("Welt"),
        ],
        [
            Text("Hallo"),
            T("Welt"),
        ],
        [
            Text("Hallo"),
            T("Welt"),
        ],
        [
            Text("Hallo"),
            T("Welt"),
        ],
    ]

    # test = Text(tk_kwargs={"text":"Hallo Welt"})
    # test._init_widget(root)

    the_Frame = Frame(layout)
    the_Frame.window_entry_point(root)

    root.mainloop()


