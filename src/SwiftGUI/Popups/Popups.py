from collections.abc import Iterable
import SwiftGUI as sg


# Note to myself:
# New popups need to be "registered" at the end of the file!

def popup_text(
        text:str,
):
    """
    Simple text-popup
    :param text:
    :return:
    """
    layout = [
        [
            sg.T(text)
        ]
    ]

    sg.Window(layout).loop_close()

def popup_yes_no(
        text:str,
) -> bool:
    """
    Simple yes-or-no-question.

    If the user selects "Yes", True will be returned.
    Otherwise False.

    :param text:
    :return:
    """
    layout = [
        [
            sg.T(text,anchor="center")
        ],[
            sg.Button("Yes",key=True),
            sg.Button("No",key=False),
        ]
    ]

    e,v = sg.Window(layout).loop_close()
    return bool(e)

def popup_button_menu(
        elements:Iterable[str],
        text:str="",
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

    e,v = sg.Window(layout).loop_close()
    return e

def popup_get_form() -> dict:
    ...

def popup_get_text(
        text:str = "",
        default:str = None,
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
            sg.In(width=50,key="In").bind_event(sg.Event.KeyEnter)
        ],[
            sg.Button("Confirm",key="Confirm",justify="center")
        ]
    ]

    e,v = sg.Window(layout).loop_close()

    if e is None:
        return default

    return v["In"]


