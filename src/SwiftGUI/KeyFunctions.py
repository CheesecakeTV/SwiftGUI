from collections.abc import Callable
from typing import Any


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

def set_value_to(new_value:any = "", elem_key:str = None) -> Callable:
    """
    Sets the value of an element.

    If you provide elem_key, that element will be changed.
    If not, the calling element will be changed.

    To clear the value of the calling element, just don't pass anything: set_value_to()

    :param elem_key: This element will be changed
    :param new_value: The element will be set to this value
    :return:
    """
    if elem_key:
        def temp(w):
            w[elem_key].value = new_value
    else:
        def temp(elem):
            elem.value = new_value

    return temp

def cycle_values(key:Any, *values:Any) -> Callable:
    """
    Every time this gets called, the next value is written to key
    IT WILL START AT THE SECOND VALUE, so it's a good idea to set the initial element-value as the first value.

    :param key: Element to change
    :param values: values you want to cycle
    :return:
    """
    n = 0
    val_len = len(values)

    assert val_len > 1, "You did not provide enough values for your cycle_values key-function"

    def temp(w):
        nonlocal n
        n += 1

        if n == val_len:
            n = 0

        w[key].value = values[n]

    return temp
