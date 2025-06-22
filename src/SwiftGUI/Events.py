import enum

class Event(enum.Enum):

    FocusIn = "FocusIn" # Element got focus in layout
    FocusOut = "FocusOut"   #

    ### Mouse ###
    MouseWheel = "MouseWheel"   # Scrolled with scroll wheel
    MouseMove = "Motion"    # Mouse has been moved

    MouseEnter = "Enter"    # Mouse hovering over the event
    MouseExit = "Leave"     #

    ClickAny = "Button"
    ClickLeft = "Button-1"
    ClickMiddle = "Button-2"
    ClickRight = "Button-3"

    ClickDoubleAny = "Double-Button"
    ClickDoubleLeft = "Double-Button-1"
    ClickDoubleMiddle = "Double-Button-2"
    ClickDoubleRight = "Double-Button-3"

    ### Special keys ###
    KeyEnter = "Return"
    KeySpace = "Space"
    KeyShift = "Shift"
    KeyAlt = "Alt"
    KeyControl = "Control"

    ### Combinations ###
    Control_Enter = "Control-Return"
    Shift_Enter = "Shift-Return"


