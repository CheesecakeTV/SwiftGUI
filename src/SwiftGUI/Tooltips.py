import threading
from typing import Callable, Protocol, Union

import SwiftGUI as sg
import time

### YOU MAY CHANGE THESE ###
tooltip_open_delay: float = 0.7  # How long the mouse must be still to open a tooltip
tooltip_close_delay: float = 0.1    # Maximum delay before a tooltip closes

### PLEASE DO NOT TOUCH ###
_last_mouse_movement = 0    # When the mouse last moved
_current_elem = None    # The sg.element the mouse is currently hovering over
_tooltips_active: bool = False  # If the tooltip-thread is running
_tooltip_function: Callable[[str], "SupportsClose"] | None = None # This gets called when a tooltip is opened. Must take one parameter: text

class SupportsClose(Protocol):
    def close(self):
        ...

def set_tooltip_callable(fct: Callable[[str], SupportsClose], only_if_nonexistent: bool = False):
    """
    Specify the function called on tooltip-opening
    :param fct: The function to call
    :param only_if_nonexistent: Only set that function if no function was set yet
    :return:
    """
    global _tooltip_function

    if only_if_nonexistent and _tooltip_function:
        return

    _tooltip_function = fct

def mouse_moved_callback():
    """Callback for the move-event"""
    global _last_mouse_movement
    _last_mouse_movement = time.time()

def mouse_entered_elem_callback(elem):  # Can't use typehints due to circular imports
    """
    Mouse entered an element (key-function)
    :param elem:
    :return:
    """
    global _current_elem
    _current_elem = elem

def mouse_exited_elem_callback(elem):
    """
    Mouse is no longer over an element
    :param elem:
    :return:
    """
    global _current_elem

    if _current_elem is elem:
        _current_elem = None

def _handle_tooltips():
    """
    Threaded.
    If the mouse hasn't moved in some time, open the tooltip
    :return:
    """
    global _last_mouse_movement
    _tooltip_open = False
    _opened_tooltip_object: Union["SupportsClose", None] = None  # The currently opened tooltip-object

    while True:
        while not _tooltip_open:
            time_since_movement = time.time() - _last_mouse_movement
            time_until_tooltip = tooltip_open_delay - time_since_movement

            if time_until_tooltip > 0:
                time.sleep(time_until_tooltip + 0.01)
                continue

            if _current_elem is None:
                time.sleep(tooltip_open_delay)
                continue

            _tooltip_open = True

        _last_mouse_movement = 0
        _opened_for_this_element = _current_elem
        _opened_tooltip_object = _tooltip_function(_current_elem.tooltip_text)  # Open tooltip

        while _tooltip_open: # Tooltip open
            time.sleep(tooltip_close_delay)

            if _current_elem is not _opened_for_this_element: # If the mouse moved again
                _tooltip_open = False
                break

        _opened_tooltip_object.close()  # Close tooltip
        _opened_tooltip_object = None

def activate_tooltips():
    """
    Activate the tooltip-thread if it isn't running already
    :return:
    """
    global _tooltips_active

    if _tooltips_active:
        return

    _tooltips_active = True
    threading.Thread(target=_handle_tooltips, daemon=True).start()


