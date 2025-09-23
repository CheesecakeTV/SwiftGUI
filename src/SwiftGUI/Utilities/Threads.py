import threading
from typing import Any
import SwiftGUI as sg
import time

from SwiftGUI import clipboard_paste
import pyperclip


def _clipboard_observer(w: sg.Window, key: Any, check_interval: float = 0.3, throw_initial_value: bool = True) -> None:
    """
    Threaded method.
    Refer to clipboard_observer for actual docstring.
    """

    if throw_initial_value:
        w.throw_event(key, clipboard_paste())

    while True:
        try:
            prev_paste = clipboard_paste()
        except pyperclip.PyperclipException:
            time.sleep(check_interval)
            continue

        temp = prev_paste

        while temp == prev_paste:
            temp = clipboard_paste()
            time.sleep(check_interval)

        w.throw_event(key, temp)

def clipboard_observer(w: sg.Window, key: Any, check_interval: float = 0.3, throw_initial_value: bool = True) -> threading.Thread:
    """
    When the clipboard changes, an event will be thrown.

    :param throw_initial_value: True, if the observer should always throw an event in the beginning, setting the starting-value
    :param w: sg.Window
    :param key: Key the event should be thrown to
    :param check_interval: How much time (in seconds) between checks if the keyboard changed
    :return: The thread. No need to start it manually
    """
    thread = threading.Thread(target= _clipboard_observer, args=(w, key), kwargs={"check_interval": check_interval, "throw_initial_value": throw_initial_value}, daemon=True)
    thread.start()
    return thread



