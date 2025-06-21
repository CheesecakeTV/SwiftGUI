from collections.abc import Iterable


class DEFAULT_OPTIONS_CLASS:

    _prev_dict:dict = None
    _prev_class_dict:dict = None
    @classmethod
    def dict(cls) -> dict:
        if cls._prev_class_dict == cls.__dict__:    # Save memory if no change was made since last call
            return cls._prev_dict

        cls._prev_dict = dict(filter(lambda a: not a[0].startswith("_") and not a[0] in ["dict","apply"], cls.__dict__.items()))
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


class GLOBAL_TEXT_OPTIONS(DEFAULT_OPTIONS_CLASS):
    text:str = ""


