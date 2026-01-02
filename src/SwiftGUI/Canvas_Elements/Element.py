from typing import Hashable

import SwiftGUI as sg
from SwiftGUI import Canvas_Elements
from SwiftGUI.Compat import Self

import tkinter as tk


class Element(Canvas_Elements.BaseCanvasElement):
    defaults = sg.GlobalOptions.Canvas_Element

    tk_widget: tk.Frame

    _create_method = "create_window"

    _transfer_keys = {

    }

    def __init__(
            self,
            position: tuple[float, float],
            element: sg.BaseElement,
            *,
            key: Hashable = None,

            anchor: sg.Literals.anchor = None,
            state: sg.Literals.canv_elem_state = None,
            tk_kwargs: dict = None,
    ):
        super().__init__(key=key, tk_kwargs=tk_kwargs)

        self.element: sg.BaseElement = element

        self._update_initial(
            *position,
            anchor = anchor,
            state = state,
        )

    def init_window_creation_done(self):
        super().init_window_creation_done()
        self.element.init_window_creation_done()

    @sg.BaseElement._run_after_window_creation
    def _update_default_keys(self,kwargs: dict, transfer_keys: bool = True):
        if not self._is_created:
            elem = sg.BaseElement()
            elem._fake_tk_element = tk.Frame(self.canvas.tk_widget, pady=0, padx=0)

            self.element._init(elem, self.window)

            kwargs["window"] = elem._fake_tk_element

        super()._update_default_keys(kwargs, transfer_keys)
