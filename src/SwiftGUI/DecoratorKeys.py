from collections.abc import Callable
from typing import Any

import SwiftGUI as sg

def attach_function_to_key(*key: Any) -> Callable:
    """
    This decorator will "extend the main loop".
    When the main loop receives the passed key, the decorated function is called, roughly equivalent to

    for e,v in w:
        ...

        if e == key:
            my_function(...)
            continue

    The decorated function may accept the following parameters, simmilar to key-functions:
    w     - Window (useful for changing elements)
    e     - Event-key (Will be the same every time in this case)
    v     - Value-"dict"

    :param key: Which key(s) to look out for
    :return:
    """
    if sg._main_window is not None:
        raise RuntimeError("You can only use decorator-keys BEFORE creating the main window.\nMove your decorated functions up.")

    def decorator(fct: Callable) -> Callable:
        for k in key:
            sg.all_decorator_key_functions[k] = fct
        return fct

    return decorator
