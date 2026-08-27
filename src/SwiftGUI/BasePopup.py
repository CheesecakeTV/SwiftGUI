import io
from os import PathLike
from typing import Hashable, Any, Literal, Generic, Iterable
from typing_extensions import TypeVar
from PIL import Image

import SwiftGUI as sg
from SwiftGUI import Color, ValueDict, ReuseError
from SwiftGUI.Compat import Self

class BasePopupNonblocking:
    def __init__(
            self,
            layout: Iterable[Iterable[sg.BaseElement]],
            *,
            keep_on_top: bool = None,
            title: str = None,
            titlebar: bool = None,
            position: Literal["center", "cursor"] | tuple[int, int] = None,
            size: int | tuple[int, int] = (None, None),
            icon: str | PathLike | Image.Image | io.BytesIO = None,  # .ico file
            background_color: Color | str = None,
            grab_anywhere: bool = None,
            **kwargs,
    ):

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
            position = position,
            **kwargs,
        )

        self.w.bind_destroy_event(self._on_destruction)

    def _event_loop(self, e: Hashable, v: sg.ValueDict):
        """
        All key-events will call this method.
        You can use it exactly like your normal event-loop.

        :param e: Contains the element-key
        :param v: Contains all values
        :return:
        """
        ...

    def close(self) -> Self:
        """
        Closes the window.
        This is implemented so you can use it in key-functions of the internal layout better.
        :return:
        """
        self.w.close()
        return self

    def _on_destruction(self, v: ValueDict):
        """
        This is called when the popup gets destroyed (closed) for any reason.
        :return:
        """
        ...

return_type = TypeVar("return_type", default=Any)

class BasePopupTyped(BasePopupNonblocking, Generic[return_type]):
    def __init__(
            self,
            layout: Iterable[Iterable[sg.BaseElement]],
            *,
            default: return_type = None,     # Returned instead of None
            keep_on_top: bool = True,
            title: str = None,
            titlebar: bool = None,
            size: int | tuple[int, int] = (None, None),
            position: Literal["center", "cursor"] | tuple[int, int] = None,
            icon: str | PathLike | Image.Image | io.BytesIO = None,  # .ico file
            background_color: Color | str = None,
            grab_anywhere: bool = None,
            **kwargs,
    ):

        self._return = None
        self._default = default
        self._used_up = False

        super().__init__(
            layout,
            keep_on_top= keep_on_top,
            title = title,
            titlebar = titlebar,
            size = size,
            icon = icon,
            background_color = background_color,
            grab_anywhere = grab_anywhere,
            position = position,
            **kwargs,
        )

    def done(self, val: Any = None) -> return_type:
        """
        Call this instead of return.
        The popup will close and return_value is returned.
        :param val: Return-value of the popup
        :return:
        """
        self._return = val
        self.w.close()

    def __call__(self, *args, **kwargs) -> return_type:
        """
        Execute the popup-functionality.
        YOU DON'T NEED TO CALL THIS!

        :param args:
        :param kwargs:
        :return:
        """
        if self._used_up:
            raise ReuseError("You cannot re-open popup-instances. Create a new instance to re-use the popup.")
        self._used_up = True

        self.w.block_others_until_close()

        if self._return is None:
            return self._default

        return self._return

class BasePopup(BasePopupTyped, Generic[return_type]):

    def __new__(cls, *args, **kwargs) -> return_type:
        me = super().__new__(cls)
        me.__init__(*args, **kwargs)

        return me() # Run the popup and return the result

