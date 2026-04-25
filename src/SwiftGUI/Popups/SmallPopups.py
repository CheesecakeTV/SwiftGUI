from collections.abc import Iterable
from typing import Mapping
import SwiftGUI as sg

def _apply_defaults(kwargs: Mapping, **defaults) -> dict:
    """
    Quick and dirty way to add default values to a dict
    :param kwargs:
    :param defaults:
    :return:
    """
    defaults.update(kwargs)
    return defaults

def show_text(
        text: str,
        block: bool = True,
        **window_kwargs,
):
    """
    Simple text-popup
    :param block: True, if the main window should be suspended/blocked
    :param text:
    :return:
    """
    layout = [
        [
            sg.T(text)
        ]
    ]

    w = sg.SubWindow(layout, **_apply_defaults(
        window_kwargs,
        padx=30,
        pady=30,
        keep_on_top=True,
    ))

    if block:
        w.block_others_until_close()

def yes_no(
        text:str,
        **window_kwargs,
) -> bool | None:
    """
    Simple yes-or-no-question.

    If the user selects "Yes", True will be returned.
    If the user selects nothing, None is returned.
    Otherwise, False.

    :param text:
    :return:
    """
    answer = None
    def set_answer(a):
        nonlocal answer
        answer = a
        w.close()

    layout = [
        [
            sg.T(text,anchor="center", padding=(0,0,0,10))
        ],[
            sg.Button("Yes", key_function=lambda :set_answer(True), width=3),
            sg.Button("No", key_function=lambda :set_answer(False), width=3)
        ]
    ]

    w = sg.SubWindow(
        layout,
        **_apply_defaults(
            window_kwargs,
            keep_on_top= True,
            padx= 50 if len(text) < 50 else 0,
            pady= 5,
        )
    )

    w.block_others_until_close()
    return answer

def button_menu(
        elements:Iterable[str],
        text:str="",
        **window_kwargs,
) -> str:
    """
    Asks the user to select one element from a list of elements.
    :param text: Displayed on top
    :param elements:
    :return: Selected element, or None if closed
    """
    length = max(map(len,elements))

    layout = [
        [
            sg.T(text,anchor="center")
        ],
        *[
            [sg.Button(elem,key=elem,width=length)] for elem in elements
        ]
    ]

    e,v = sg.SubWindow(
        layout,
        **_apply_defaults(
            window_kwargs,
        )
    ).loop_close()
    return e

def get_form() -> dict:
    raise NotImplementedError("Nothing to see here right now...")

def get_text(
        text:str = "",
        default:str = None,
        **window_kwargs,
) -> str:
    """
    Ask the user to input some text.
    The user can confirm by pressing enter.

    :param default: Returned if user closes the window
    :param text:
    :return:
    """
    layout = [
        [
            sg.T(text,anchor="center") if text else sg.HSep()
        ],[
            in_elem := sg.In(width=50,key="In").bind_event(sg.Event.KeyEnter)
        ],[
            sg.Button("Confirm",key="Confirm",justify="center")
        ]
    ]

    w = sg.SubWindow(
        layout,
        **_apply_defaults(
            window_kwargs,
            keep_on_top=True,
        )
    )
    in_elem.set_focus()
    e,v = w.loop_close()

    if e is None:
        return default

    return v["In"]


