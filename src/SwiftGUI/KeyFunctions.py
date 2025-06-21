from collections.abc import Callable
from SwiftGUI import BaseElement, Window

### HOW TO CREATE KEY-FUNCTION ###
#
# Just create a function, but don't add any parameters except:
# w     - Window (useful for changing elements)
# e     - Event (Event-key, if you set any)
# v     - Values (All values as a dict)
# val   - Value (Value of the event-element)
# elem  - Element (Element that caused the event)
#
# Just set all of these parameters you need, they will be filled in accordingly.
# Their order doesn't matter.

### Some useful key-functions to use in your layout.


def copy_value_to(to_key:any) -> Callable:
    """
    Copies the value to the specified key
    :param to_key: Element-key to copy to
    :return:
    """
    def fkt(w,val):
        w[to_key].set_value(val)

    return fkt

def copy_value_from(from_key:any) -> Callable:
    """
    Copies the value from the specified key to the calling element
    :param from_key: Element-key to copy from
    :return:
    """
    def fkt(v,elem):
        elem.value = v[from_key]

    return fkt

def clear_str_value(elem:BaseElement):
    """
    Clears the value of the element to an empty string
    :return:
    """
    elem.value = ""
