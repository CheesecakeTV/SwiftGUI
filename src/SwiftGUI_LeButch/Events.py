import enum



class Event(enum.Enum):

    FocusIn = "FocusIn" # Keyboard focus
    FocusOut = "FocusOut"   #

    ### Mouse ###
    MouseWheel = "MouseWheel"

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


# <KeyPress>:
# Key on keyboard has been pressed down.
# <KeyRelease>:
# Key has been released.
# <ButtonPress>:
# A mouse button has been pressed.
# <ButtonRelease>:
# A mouse button has been released.
# <Motion>:
# Mouse has been moved.
# <Configure>:
# Widget has changed size or position.
