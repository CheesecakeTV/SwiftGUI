from typing import Literal

l1 = Literal["Hallo","Welt"]
l2 = Literal["Hello","World"]

class test_class:

    def __setitem__(self, key, value):
        ...

    # def __getitem__(self, item:Literal["Hallo","Welt"]):
    #     return "Hi"

    def __getitem__(self, item:Literal[l1,l2]):
        return "Hi"

# Conclusion: Typehints do work for set- and getitem when it is defined in getitem.

x = test_class()

x[""]
