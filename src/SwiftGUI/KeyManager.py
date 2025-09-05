from SwiftGUI.Compat import Self

All_Keys:dict[str:"Key"] = dict()
SEPARATOR = "."
duplicate_warnings:bool = True  # Turn this off, if you know that there will be duplicates.

class Key:
    def __init__(self,key:str):
        self.key = key

    def __new__(cls, *args, **kwargs):
        key = args[0]

        if key in All_Keys:

            if duplicate_warnings:
                print(f"WARNING! Duplicate key: {key}")

            return All_Keys[key]

        temp = super().__new__(cls)
        All_Keys[key] = temp

        return temp

    # def __del__(self):
    #     if self.key in All_Keys:
    #         del All_Keys[self.key]

    def _add(self,other:Self|str,inverse:bool=False):
        try:
            if inverse:
                return Key(str(other) + SEPARATOR + str(self))

            return Key(str(self) + SEPARATOR + str(other))
        except AttributeError:
            return NotImplemented

    def __add__(self, other:Self|str):
        return self._add(other)

    def __radd__(self, other):
        return self._add(other,inverse=True)

    def __str__(self):
        return self.key

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __repr__(self):
        return str(self)

    def __contains__(self, item:Self|str):
        """
        Different way than comparing strings.
        Returns true, if self is any parent-key-group of item.
        :param item:
        :return:
        """
        return str(self) in str(item)

