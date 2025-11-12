import tkinter as tk

from SwiftGUI import BaseElement, ElementFlag, GlobalOptions, Color, Frame
from SwiftGUI.Extended_Elements.Separator import VerticalSeparator


class GridFrame(Frame):
    """
    Frame with .grid instead of .pack
    """
    defaults = GlobalOptions.GridFrame

    _containing_row_frame_widgets: list[tk.Frame]
    _background_color: str | Color
    def _init_containing(self):
        """
        Initialize all containing widgets
        :return:
        """
        #ins_kwargs_rows = self._insert_kwargs_rows.copy()

        for n,row in enumerate(self._contains):
            for k,elem in enumerate(row):

                #box = tk.Frame(self._tk_widget, relief="flat", background=self._background_color)  # This is the outer container
                actual_box = tk.Frame(self._tk_widget, background=self._background_color)  # This is where the actual elements are put in

                self._containing_row_frame_widgets.append(actual_box)

                box_elem = BaseElement()
                box_elem._fake_tk_element = actual_box

                elem._init(box_elem, self.window)

                expand = elem.has_flag(ElementFlag.EXPAND_ROW)
                expand_y = elem.has_flag(ElementFlag.EXPAND_VERTICALLY)

                sticky = ""

                if self._side == "left":
                    sticky += "w"
                elif self._side == "right":
                    sticky += "e"

                if expand:
                    sticky += "ew"
                elif expand_y or isinstance(elem, VerticalSeparator):   # I know this looks sketchy, but still probably the least painful way to implement...
                    sticky += "ns"

                actual_box.grid(row= n, column= k, sticky= sticky)

                if self._grab_anywhere_on_this:
                    #self.window.bind_grab_anywhere_to_element(box)
                    self.window.bind_grab_anywhere_to_element(actual_box)
