import io
from collections.abc import Iterable
from os import PathLike
from typing import Hashable, Any
from PIL import Image

import SwiftGUI as sg
from SwiftGUI import Color


class BasePopup:

    def __init__(
            self,
            layout: Iterable[Iterable[sg.BaseElement]],
            /,
            default: Any = None,     # Returned instead of None
            keep_on_top: bool = True,
            title: str = None,
            titlebar: bool = None,
            size: int | tuple[int, int] = (None, None),
            icon: str | PathLike | Image.Image | io.BytesIO = None,  # .ico file
            background_color: Color | str = None,
            grab_anywhere: bool = None,
    ):

        self._return = None
        self._default = default

        self.w = sg.SubWindow(
            layout,
            event_loop_function= self._event_loop,
            keep_on_top= keep_on_top,
            title = title,
            titlebar = titlebar,
            size = size,
            icon = icon,
            background_color = background_color,
            grab_anywhere = grab_anywhere,
        )

    def _event_loop(self, e: Hashable, v: sg.ValueDict):
        """
        All key-events will call this method.
        You can use it exactly like your normal event-loop.

        :param e: Contains the element-key
        :param v: Contains all values
        :return:
        """
        ...

    def __new__(cls, *args, **kwargs) -> Any:
        me = super().__new__(cls)
        me.__init__(*args, **kwargs)

        return me() # Run the popup and return the result

    def done(self, val: Any = None):
        """
        Call this instead of return.
        The popup will close and return_value is returned.
        :param val: Return-value of the popup
        :return:
        """
        self._return = val
        self.w.close()

    def __call__(self, *args, **kwargs):
        """
        Execute the popup-functionality.
        YOU DON'T NEED TO CALL THIS!

        :param args:
        :param kwargs:
        :return:
        """
        self.w.block_others_until_close()

        if self._return is None:
            return self._default

        return self._return
