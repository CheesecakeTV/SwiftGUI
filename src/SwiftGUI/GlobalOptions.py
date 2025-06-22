import tkinter as tk    # Not needed, but helpful to figure out default vals
from tkinter import ttk
from collections.abc import Iterable
from typing import Literal, Union
from SwiftGUI import Literals

_all_configs:list[Union["DEFAULT_OPTIONS_CLASS",type]] = list()

def persist_all_changes():
    """
    Persist the changes in every configuration
    :return:
    """
    for i in _all_configs:
        i.persist_changes()

class DefaultOptionsMeta(type):

    def __new__(mcs, name, bases, namespace):
        cls:"DEFAULT_OPTIONS_CLASS"|type = super().__new__(mcs, name, bases, namespace)
        _all_configs.append(cls)

        prev = cls.__mro__[1]
        cls.dict = dict(cls.__dict__)
        if hasattr(prev,"dict"):
            cls.dict.update(dict(prev.__dict__))

        cls.persist_changes()

        return cls

class DEFAULT_OPTIONS_CLASS(metaclass=DefaultOptionsMeta):

    _prev_dict:dict = None
    _prev_class_dict:dict = None
    @classmethod
    def persist_changes(cls):
        """
        Call this to persist changes you made into the option-class.
        I know this is kinda nasty, but still better than looping every time this gets applied...
        :return:
        """

        collected = dict()
        for i in cls.__mro__[-1::-1]:
            collected.update(i.__dict__)

        cls.dict = dict(filter(lambda a: not a[0].startswith("_") and not a[0] in ["dict","apply","single","persist_changes"], collected.items()))


    @classmethod
    def apply(cls,apply_to:dict) -> dict:
        """
        Apply default configuration TO EVERY NONE-ELEMENT of apply_to

        :param apply_to: It will be changed AND returned
        :return: apply_to will be changed AND returned
        """
        my_dict = cls.dict

        # Get keys with value None that are also in the global options
        items_change:Iterable[tuple] = filter(lambda a: a[1] is None and a[0] in my_dict , apply_to.items())

        for key,_ in items_change:
            apply_to[key] = my_dict[key]

        return apply_to

    @classmethod
    def single(cls,key:str,val:any) -> any:
        """
        If val is None, cls.key will be returned.
        Else val.
        :param key:
        :param val:
        :return:
        """
        if val is None:
            return getattr(cls,key)
        return None

class Common(DEFAULT_OPTIONS_CLASS):
    ...#cursor:Literals.cursor = "arrow"

class Text(Common):
    text:str = ""

class Frame(Common):
    padding:int|tuple[int,int]|tuple[int,int,int,int] = 3
    relief:Literal["raised", "sunken", "flat", "ridge", "solid", "groove"] = "flat"
    #background = "blue"

