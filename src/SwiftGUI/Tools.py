from typing import Any
import pyperclip

def clp_paste() -> Any:
    """
    Output current clipboard as return
    :return:
    """
    return pyperclip.paste()

def clp_copy(value: Any) -> Any:
    """
    Copy the value to clipboard.
    :param value:
    :return: The provided value for inline-calls
    """
    pyperclip.copy(value)
    return value

def remove_None_vals(from_dict:dict) -> dict:
    """
    Remove all None-values from a dictionary and return it as a new dictionary
    :param from_dict: Will not be changed
    :return:
    """
    return dict(filter(lambda a:a[1] is not None, from_dict.items()))
