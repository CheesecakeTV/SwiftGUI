from collections.abc import Callable
from SwiftGUI_LeButch import BaseElement, Window


# Todo
### Some useful key-functions to use in your layout

### ATTENTION! send_wev has to be true for some of them!

def copy_value(to_key:any) -> Callable:
    """
    Copies the value to the specified key
    :param to_key: Element to copy to
    :return:
    """
    def fkt(w:Window,e,v,val=NotImplemented):
        if val is NotImplemented:
            val = v[e]

        w[to_key].set_value(val)

    return fkt
