from typing import Any, Callable, Hashable

import SwiftGUI as sg
from SwiftGUI.Compat import Self


class BaseCanvasElement(sg.BaseWidget): # Inheritance mainly for the update-routine
    defaults = sg.GlobalOptions.Common_Canvas_Element

    canvas: sg.Canvas   # "my" canvas

    _create_method: str = ""    # This should be the name of the method used to create this element with

    _grab_anywhere_on_this = False

    def __init__(
            self,
            key: Hashable = None,
            tk_kwargs: dict = None,
    ):
        super().__init__(key=key, tk_kwargs=tk_kwargs)
        self._is_created = False    # True, if _update_default_keys ran at least once
        self.canvas_id: int | None = None   # This is used to identify the element in the canvas-widget

    def attach_to_canvas(self, my_canvas: sg.Canvas):
        my_canvas.add_canvas_element(self)

    @sg.BaseElement._run_after_window_creation
    def _update_initial(self,*args,**kwargs) -> Self:
        kwargs["_args"] = args
        super()._update_initial(**kwargs)
        return self

    def _update_default_keys(self,kwargs: dict,transfer_keys: bool = True):
        super()._update_default_keys(kwargs, transfer_keys=transfer_keys)

        if not self._is_created:
            fct = getattr(self.canvas.tk_widget, self._create_method)
            args = kwargs["_args"]
            del kwargs["_args"]

            self.canvas_id = fct(args, **kwargs)

            self._is_created = True
            return

        if "_args" in kwargs:
            del kwargs["_args"]
        self.canvas.tk_widget.itemconfigure(self.canvas_id, **kwargs)

    def init_window_creation_done(self):
        self.add_flags(sg.ElementFlag.IS_CREATED)
        self.window = self.canvas.window

        super().init_window_creation_done()

    def _apply_update(self):
        """This should do nothing for canvas-elements!"""
        return

    def _get_value(self) -> Any:
        raise AttributeError(f"{self} has no value!")

    def set_value(self, new_val: Any) -> Any:
        raise AttributeError(f"{self} has no value to set!")

    def _bind_event_to_widget(self, tk_event: str, event_function: Callable) -> Self:
        self.canvas.tk_widget.tag_bind(self.canvas_id, tk_event, event_function)
        return self

    @sg.BaseWidget._run_after_window_creation
    def delete(self) -> Self:
        """
        Delete the element from the canvas.
        :return:
        """
        self.canvas.tk_widget.delete(self.canvas_id)
        return self

    @sg.BaseWidget._run_after_window_creation
    def move_to(self, x: float, y: float) -> Self:
        """
        Move the element to specified coordinates

        :param x:
        :param y:
        :return:
        """
        self.canvas.tk_widget.moveto(self.canvas_id, x, y)
        return self

