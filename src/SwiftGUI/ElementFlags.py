from enum import Enum

class ElementFlag(Enum):
    # Flags 0-100 might be used
    IS_CONTAINER = 1    # Element may contain other elements
    DONT_REGISTER_KEY = 2   # Element isn't registered into the window
    UPDATE_FONT = 3     # Font has to be updated
    IS_CREATED = 4  # Element was created by _init
    ENABLE_STANDARD_EVENT = 5   # If the standard-event should be enabled (capt. obvious...)

    # Flags 100-200 will never be used, so they are available for you to create custom flags
    # It's important to set an actual value for each flag so it can be saved/loaded correctly
