from typing import Literal, Iterable
import tkinter.ttk as ttk

class GLOBAL_ELEMENT_OPTIONS:
    padding:int|tuple[int,int]|tuple[int,int,int,int] = 3
    relief:Literal["raised", "sunken", "flat", "ridge", "solid", "groove"] = "flat"
    background = "blue"

global_element_options_dict = dict()
def refresh_options_dict():
    """
    Refresh the options_dict from the class
    :return:
    """
    global global_element_options_dict

    # Remove everything "dunder"
    global_element_options_dict = dict(filter(lambda a:not a[0].startswith("__"), GLOBAL_ELEMENT_OPTIONS.__dict__.items()))


refresh_options_dict()

def do_global_config(config_dict:dict,global_options_from:dict = None) -> dict:
    """
    Replace everything with value None with the global standard for that key, if available

    :param global_options_from: None to use standard global options
    :param config_dict: dict to change values in
    :return: The passed dict. No need to use it, but just in case you want to do an inline...
    """
    if global_options_from is None:
        global_options_from = global_element_options_dict

    # Get keys with value None that are also in the global options
    items_change:Iterable[tuple] = filter(lambda a: a[1] is None and a[0] in global_options_from , config_dict.items())

    for key,_ in items_change:
        config_dict[key] = global_options_from[key]

    return config_dict

