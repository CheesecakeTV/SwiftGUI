from collections.abc import Iterable
from typing import Literal

class DEFAULT_OPTIONS_CLASS:

    _prev_dict:dict = None
    _prev_class_dict:dict = None
    @classmethod
    def dict(cls) -> dict:
        if cls._prev_class_dict == cls.__dict__:    # Save memory if no change was made since last call
            return cls._prev_dict

        cls._prev_dict = dict(filter(lambda a: not a[0].startswith("_") and not a[0] in ["dict","apply","single"], cls.__dict__.items()))
        cls._prev_class_dict = cls.__dict__.copy()

        return cls._prev_dict

    @classmethod
    def apply(cls,apply_to:dict) -> dict:
        """
        Apply default configuration TO EVERY NONE-ELEMENT of apply_to
        :param apply_to: It will be changed AND returned
        :return: apply_to will be changed AND returned
        """
        my_dict = cls.dict()

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
    ...

class Text(Common):
    text:str = ""

class Frame(Common):
    padding:int|tuple[int,int]|tuple[int,int,int,int] = 3
    relief:Literal["raised", "sunken", "flat", "ridge", "solid", "groove"] = "flat"
    #background = "blue"

