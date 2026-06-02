from typing import Callable


def _combine_events(*event_string: str, join_str: str = "-") -> str:
    """
    Combine multiple events into one.
    Useful for hotkeys and such
    :param event_string:
    :return:
    """
    event_string = map(str, event_string)
    return join_str.join(event_string)

def _event_modifier(modifier: str) -> Callable[[str, ], str]:
    """
    Create a function that adds a modifier to an event-string
    :param modifier:
    :return:
    """
    def foo(*event_string):
        return _combine_events(modifier, *event_string)
    return foo

class Event:
    """
    A class containing some useful event-strings.

    Find most available event-strings here, even though not all of them might work:
    https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/key-names.html
    """

    FocusIn = "FocusIn" # Element gained the focus
    FocusOut = "FocusOut"   # Element lost the focus

    ### Mouse ###
    MouseWheel = "MouseWheel"   # Scrolled with scroll wheel
    MouseMove = "Motion"    # Mouse has been moved

    MouseHoldAndMoveLeft = "B1-Motion"  # The mouse-button is held down and moved over this element
    MouseHoldAndMoveMiddle = "B2-Motion"
    MouseHoldAndMoveRight = "B3-Motion"

    MouseEnter = "Enter"    # Mouse starts hovering over the element
    MouseExit = "Leave"     # Mouse stopped hovering over the element

    ClickAny = "Button" # Any mousebutton clicked on this element
    ClickLeft = "Button-1"
    ClickMiddle = "Button-2"
    ClickRight = "Button-3"

    ClickDoubleAny = "Double-Button"
    ClickDoubleLeft = "Double-Button-1"
    ClickDoubleMiddle = "Double-Button-2"
    ClickDoubleRight = "Double-Button-3"

    ### Special keys ###
    KeyDelete = "Delete"
    KeyEnter = "Return"
    KeySpace = "space"
    KeyTab = "Tab"
    KeyEscape = "Escape"
    KeyPageDown = "Next"
    KeyPageUp = "Prior"
    KeyBackspace = "BackSpace"

    LeftShift = "Shift_L"
    LeftAlt = "Alt_L"
    LeftControl = "Control_L"
    RightShift = "Shift_R"
    RightAlt = "Alt_R"
    RightControl = "Control_R"

    ### Arrow-keys ###
    ArrowDown = "Down"
    ArrowLeft = "Left"
    ArrowUp = "Up"
    ArrowRight = "Right"

    ### Hotkeys ###
    Control_Q = "Control-q"     # Used for quitting applications in many software
    Control_C = "Control-c"
    Control_V = "Control-v"
    Control_X = "Control-x"
    Control_Enter = "Control-Return"
    Shift_Enter = "Shift-Return"

    ### Others ###
    AnyKey = "Any-KeyPress"

    ### Methods ###
    # You can use these methods like this: sg.Event.Control_("e")       # for ctrl+e
    # Or like this: sg.Event.Shift_(sg.Event.Enter)     # for Shift+Enter
    Control_ = _event_modifier("Control")
    Alt_ = _event_modifier("Alt")
    Shift_ = _event_modifier("Shift")   # Doesn't work with letters. For letters, pass the capital version instead of the normal letter.

    Double_ = _event_modifier("Double") # Same event twice in a row (like double-click)
    Triple_ = _event_modifier("Triple") # Same event 3 times in a row

    @classmethod
    def chain(cls, *events: str) -> str:
        """
        Triggers when these events are caused one after another
        :param events:
        :return:
        """
        events = map(lambda e: f"<{e}>", events)
        return "".join(events)

    @classmethod
    def string(cls, events: str) -> str:
        events = map(lambda e: f"<{e}>", events)
        return "".join(events)

