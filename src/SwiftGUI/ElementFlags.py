from enum import Enum

class ElementFlag(Enum):
    # Flags 0-100 might be used
    IS_CONTAINER = 1    # Element may contain other elements
    DONT_REGISTER_KEY = 2   # Element isn't registered into the window
    UPDATE_FONT = 3     # Font has to be updated
    IS_CREATED = 4  # Element was created by _init
    EXPAND_ROW = 5  # The row this element is in should be expanded
    APPLY_PARENT_BACKGROUND_COLOR = 6   # Set, if the element should apply whatever background-color the parent has
    EXPAND_VERTICALLY = 7   # Expand the row this element is in vertically
    HAS_SCROLLBAR_Y = 8 # This widget should have a vertical (y-direction) scrollbar

    # Flags 100-200 will never be used, so they are available for you to create custom flags
    # It's important to set an actual value for each flag so it can be saved/loaded correctly
