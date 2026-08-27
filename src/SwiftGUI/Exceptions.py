
class ReuseError(Exception):
    """
    Called when an element was re-used (not implemented yet), or a popup opened more than once.
    """
    ...

class RowTypeError(TypeError):
    """
    Called when a layout-row is not a row
    """
    ...

