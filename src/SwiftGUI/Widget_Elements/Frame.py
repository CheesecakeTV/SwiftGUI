import tkinter as tk
from collections.abc import Iterable

from SwiftGUI import BaseElement, ElementFlag, BaseWidgetContainer, GlobalOptions, Literals, Color, BaseWidget


class Frame(BaseWidgetContainer):
    """
    Copy this class ot create your own Widget
    """
    _tk_widget_class:type[tk.Frame] = tk.Frame # Class of the connected widget
    defaults = GlobalOptions.Frame

    _transfer_keys = {
        "background_color":"background"
    }

    def __init__(
            self,
            layout: Iterable[Iterable[BaseElement]],
            /,
            key: str = None,
            alignment: Literals.alignment = None,
            expand: bool = False,
            expand_y: bool = False,
            background_color: str | Color = None,
            apply_parent_background_color: bool = None,
            pass_down_background_color: bool = None,
            # Add here
            tk_kwargs: dict[str:any]=None,
    ):
        super().__init__(key=key, tk_kwargs=tk_kwargs, expand_y=expand_y)

        self._contains = layout
        self._linked_background_elements = list()

        if background_color and not apply_parent_background_color:
            apply_parent_background_color = False

        if tk_kwargs is None:
            tk_kwargs = dict()

        _tk_kwargs = {
            **tk_kwargs,
            # Insert named arguments for the widget here
            "background_color":background_color,
            "apply_parent_background_color": apply_parent_background_color,
            "pass_down_background_color": pass_down_background_color,
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
        self.add_flags(ElementFlag.IS_CREATED)

    _linked_background_elements: list[BaseWidget]
    def link_background_color(self, *element: BaseWidget):
        """
        Link a tk-widget to the frame.
        When the frame's background-color is changed, the background-color of this widget is changed too
        :param element:
        :return:
        """
        self._linked_background_elements.extend(element)

    _background_color_initial: Color | str = None
    _pass_down_background_color: bool = False
    def _update_special_key(self,key:str,new_val:any) -> bool|None:

        match key:
            case "apply_parent_background_color":
                if new_val:
                    self.add_flags(ElementFlag.APPLY_PARENT_BACKGROUND_COLOR)
                else:
                    self.remove_flags(ElementFlag.APPLY_PARENT_BACKGROUND_COLOR)
            
            case "pass_down_background_color":
                self._pass_down_background_color = new_val

            case "background_color":
                if not self.has_flag(ElementFlag.IS_CREATED):
                    self._background_color_initial = new_val
                    return True

                for row in self._containing_row_frame_widgets:
                    row.configure(background=new_val)

                for elem in self._linked_background_elements:
                    elem.update(background_color = new_val)

                if self._pass_down_background_color:
                    for i in self._contains:
                        for elem in i:
                            if elem.has_flag(ElementFlag.APPLY_PARENT_BACKGROUND_COLOR):
                                elem.update(background_color = new_val)
            case _:
                return False

        return True

    def init_window_creation_done(self):
        if self._background_color_initial is not None:
            self.update(background_color = self._background_color_initial)

