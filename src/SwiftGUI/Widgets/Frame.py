import tkinter as tk
import tkinter.ttk as ttk
from collections.abc import Iterable

from SwiftGUI import BaseElement, ElementFlag, BaseWidgetContainer, GlobalOptions, Literals, Color

class Frame(BaseWidgetContainer):
    """
    Copy this class ot create your own Widget
    """
    _tk_widget_class:type[ttk.Frame] = tk.Frame # Class of the connected widget
    defaults = GlobalOptions.Frame

    _transfer_keys = {
        "background_color":"background"
    }

    def __init__(
            self,
            layout: Iterable[Iterable[BaseElement]],
            /,
            alignment: Literals.alignment = None,
            expand: bool = False,
            background_color: str | Color = None,
            apply_parent_background_color: bool = None,
            # Add here
            tk_kwargs: dict[str:any]=None,
    ):
        super().__init__(tk_kwargs=tk_kwargs)

        self._contains = layout

        if background_color and not apply_parent_background_color:
            apply_parent_background_color = False

        if tk_kwargs is None:
            tk_kwargs = dict()

        _tk_kwargs = {
            **tk_kwargs,
            # Insert named arguments for the widget here
            "background_color":background_color,
            "apply_parent_background_color": apply_parent_background_color,
        }
        self.update(**_tk_kwargs)

        self._insert_kwargs["expand"] = self.defaults.single("expand",expand)

        self._insert_kwargs_rows.update({
            "side":self.defaults.single("alignment",alignment),
        })

    def window_entry_point(self,root:tk.Tk|tk.Widget,window:BaseElement):
        """
        Starting point for the whole window, or part of the layout.
        Don't use this unless you overwrite the sg.Window class
        :param window: Window Element
        :param root: Window to put every element
        :return:
        """
        self.window = window
        self.window.add_flags(ElementFlag.IS_CREATED)
        self.add_flags(ElementFlag.IS_CONTAINER)
        self._init_widget(root)

    def _update_special_key(self,key:str,new_val:any) -> bool|None:

        match key:
            case "apply_parent_background_color":
                if new_val:
                    self.add_flags(ElementFlag.APPLY_PARENT_BACKGROUND_COLOR)
                else:
                    self.remove_flags(ElementFlag.APPLY_PARENT_BACKGROUND_COLOR)

            case "background_color":
                for row in self._containing_row_frame_widgets:
                    row.configure(background=new_val)

                for i in self._contains:
                    for elem in i:
                        if elem.has_flag(ElementFlag.APPLY_PARENT_BACKGROUND_COLOR):
                            elem.update(background_color = new_val)

                return True
            case _:
                return False

        return True