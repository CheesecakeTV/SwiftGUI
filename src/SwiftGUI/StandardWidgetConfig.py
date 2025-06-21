from typing import Literal
import tkinter.ttk as ttk

class GLOBAL_ELEMENT_OPTIONS:
    padding:int|tuple[int,int]|tuple[int,int,int,int] = 3
    relief:Literal["raised", "sunken", "flat", "ridge", "solid", "groove"] = "flat"

global_element_options_dict = dict()
def refresh_options_dict():
    """
    Refresh the options_dict from the class
    :return:
    """
    global global_element_options_dict
    global_element_options_dict = dict(filter(lambda a:not a[0].startswith("__"), GLOBAL_ELEMENT_OPTIONS.__dict__.items()))
refresh_options_dict()

