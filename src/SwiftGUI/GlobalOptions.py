import tkinter as tk    # Not needed, but helpful to figure out default vals
from tkinter import ttk
from collections.abc import Iterable
from typing import Literal

from virtualenv.config.convert import NoneType

from SwiftGUI import Literals, Color


class _DefaultOptionsMeta(type):

    def __new__(mcs, name, bases, namespace):
        # Remove NONE-values so they don't overwrite non-None-values of higher classes
        namespace = dict(filter(lambda a: a[1] is not None, namespace.items()))
        cls:"DEFAULT_OPTIONS_CLASS"|type = super().__new__(mcs, name, bases, namespace)

        prev = cls.__mro__[1]
        cls._dict = dict(cls.__dict__)
        if hasattr(prev,"_dict"):
            cls._dict.update(dict(prev.__dict__))

        cls.made_changes = True
        cls._persist_changes()

        return cls

    def __setattr__(self, key, value):
        if not key.startswith("_") and not key == "made_changes":
            self.made_changes = True

        super().__setattr__(key,value)

        if value is None:
            delattr(self,key)


class DEFAULT_OPTIONS_CLASS(metaclass=_DefaultOptionsMeta):
    """
    Derive from this class to create a "blank" global-options template.

    DON'T ADD ANY OPTIONS HERE!
    """

    _prev_dict:dict = None
    _prev_class_dict:dict = None
    @classmethod
    def _persist_changes(cls):
        """
        Refreshes the _dict if necessary
        :return:
        """
        cls._check_for_changes()
        if not cls.made_changes:
            return
        cls.made_changes = False

        collected = dict()
        for i in cls.__mro__[-1::-1]:
            collected.update(i.__dict__)

        cls._dict = dict(filter(lambda a: not a[0].startswith("_") and not a[0] in ["_dict","apply","single","persist_changes"], collected.items()))

    @classmethod
    def _check_for_changes(cls):
        """
        Check if any parent-class changed anything
        :return:
        """
        if cls.made_changes:
            return

        my_iter = iter(cls.__mro__[-3::-1])
        for i in my_iter:    # Check higher classes
            if i.made_changes:
                cls.made_changes = True
                break

        for i in my_iter:   # Set changes for all the other classes between you and changed
            i.made_changes = True

    @classmethod
    def apply(cls,apply_to:dict) -> dict:
        """
        Apply default configuration TO EVERY NONE-ELEMENT of apply_to

        :param apply_to: It will be changed AND returned
        :return: apply_to will be changed AND returned
        """
        cls._persist_changes()
        my_dict = cls._dict

        # Get keys with value None that are also in the global options
        items_change:Iterable[tuple] = filter(lambda a: a[1] is None and a[0] in my_dict , apply_to.items())

        for key,_ in items_change:
            apply_to[key] = my_dict[key]

        return apply_to

    @classmethod
    def single(cls,key:str,val:any,default:any=None) -> any:
        """
        val will be returned.
        If val is None, cls.key will be returned.
        If both are None, default will be returned.
        :param default:
        :param key: Name of attribute
        :param val: User-val
        :return:
        """
        cls._persist_changes()
        if not val is None:
            return val

        if hasattr(cls,key):
            return getattr(cls,key)

        return default

class Common(DEFAULT_OPTIONS_CLASS):
    cursor:Literals.cursor = None   # Find available cursors here (2025): https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
    takefocus:bool = True

class Text(Common):
    text:str = ""
    takefocus:bool = False
    underline:int = None
    justify:Literal["left","right","center"] = "center"
    background_color:Color|str = None
    text_color:Color|str = None
    #borderwidth:int = "5c" # Does not work

    fonttype:str = "Any"
    fontsize:int = 10
    font_bold:bool = False
    font_italic:bool = False
    font_underline:bool = False
    font_overstrike:bool = False

    padding:Literals.padding = 0
    width:int = None

class Frame(Common):
    takefocus = False
    padding:Literals.padding = 3
    relief:Literals.relief = "flat"
    #background = "blue"

