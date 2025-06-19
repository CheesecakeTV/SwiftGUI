import enum



class Event(enum.Enum):

    FocusIn = "FocusIn" # Keyboard focus
    FocusOut = "FocusOut"   #

    ### Mouse ###
    MouseWheel = "MouseWheel"   # Scrolled with scroll wheel
    MouseMove = "Motion"    # Mouse has been moved

    MouseEnter = "Enter"    # Mouse hovering over the event
    MouseExit = "Leave"     #

    MouseClickLeft = "Button-1"
    MouseClickMiddle = "Button-2"
    MouseClickRight = "Button-3"

    MouseDoubleClickLeft = "Double-Button-1"
    MouseDoubleClickMiddle = "Double-Button-2"
    MouseDoubleClickRight = "Double-Button-3"

    ### Special keys ###
    EnterKey = "Return" #

