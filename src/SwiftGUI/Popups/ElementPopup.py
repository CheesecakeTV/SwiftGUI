import SwiftGUI as sg

class ElementPopup(sg.BasePopup):
    """
    Opens a single element in its own blocking window
    """
    def __init__(self, element: sg.BaseElement, **kwargs):
        layout = [[element]]

        if hasattr(element, "done_method"):
            element.done_method = self.done

        super().__init__(layout=layout, **kwargs)

class ElementPopupNonblocking(sg.BasePopupNonblocking):
    """
    Opens a single element in its own window
    """
    def __init__(self, element: sg.BaseElement, **kwargs):
        layout = [[element]]

        super().__init__(layout=layout, **kwargs)

        if hasattr(element, "done_method"):
            element.done_method = lambda _: self.w.close() # This needs to "destroy" an argument, that's why lambda


