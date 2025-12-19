import tkinter as tk
from collections.abc import Iterable
from typing import Any, Hashable

from SwiftGUI import BaseElement, ElementFlag, BaseWidgetContainer, GlobalOptions, Literals, Color, BaseWidget
from SwiftGUI.Compat import Self


class Frame(BaseWidgetContainer):
    """
    Copy this class ot create your own Widget
    """
    tk_widget: tk.Frame
    _tk_widget_class:type[tk.Frame] = tk.Frame # Class of the connected widget
    defaults = GlobalOptions.Frame

    _grab_anywhere_on_this = True

    _transfer_keys = {
        "background_color_disabled":"disabledbackground",
        "background_color_readonly":"readonlybackground",
        "background_color":"background",
        "text_color":"foreground",
        "text_color_disabled": "disabledforeground",
        "highlightbackground_color": "highlightbackground",
        "selectbackground_color": "selectbackground",
        "select_text_color": "selectforeground",
        "pass_char":"show",
    }

    def __init__(
            self,
            layout: Iterable[Iterable[BaseElement]],
            /,
            key: Hashable = None,
            alignment: Literals.alignment = None,
            expand: bool = False,
            expand_y: bool = False,
            background_color: str | Color = None,
            apply_parent_background_color: bool = None,
            pass_down_background_color: bool = None,
            borderwidth: int = None,
            cursor: Literals.cursor = None,
            highlightbackground_color: Color | str = None,
            highlightcolor: Color | str = None,
            highlightthickness: int = None,

            padx: int = None,
            pady: int = None,

            # width: int = None,
            # height: int = None,

            relief: Literals.relief = None,

            takefocus: bool = None,

            # Add here
            tk_kwargs: dict[str:Any]=None,
    ):
        self._containing_frames = list()
        self._containing_row_frames = list()
        self._containing_row_elements = list()

        super().__init__(key=key, tk_kwargs=tk_kwargs, expand=expand, expand_y=expand_y)

        self._contains: list[list[BaseElement]] = list(map(list, layout))
        self._linked_background_elements = list()

        if background_color and not apply_parent_background_color:
            apply_parent_background_color = False

        if tk_kwargs is None:
            tk_kwargs = dict()

        self._update_initial(background_color=background_color,
                             apply_parent_background_color=apply_parent_background_color,
                             pass_down_background_color=pass_down_background_color, borderwidth=borderwidth,
                             cursor=cursor, highlightbackground_color=highlightbackground_color,
                             highlightcolor=highlightcolor, highlightthickness=highlightthickness, padx=padx, pady=pady,
                             relief=relief, takefocus=takefocus, **tk_kwargs)

        #self._insert_kwargs["expand"] = self.defaults.single("expand",expand)

        self._side = self.defaults.single("alignment", alignment)
        self._insert_kwargs_rows.update({
            "side": self._side
        })

    def __len__(self) -> int:
        """How many rows are in the frame"""
        return len(self._containing_row_elements)

    def window_entry_point(self,root:tk.Tk|tk.Widget,window:BaseElement):
        """
        Starting point for the whole window, or part of the layout.
        Don't use this unless you overwrite the sg.Window class
        :param window: Window Element
        :param root: Window to put every element
        :return:
        """
        self.window = window
        self.window.add_flags(ElementFlag.IS_CREATED)
        self.add_flags(ElementFlag.IS_CONTAINER)
        self._init_widget(root)
        self.add_flags(ElementFlag.IS_CREATED)

    _linked_background_elements: list[BaseWidget]
    def link_background_color(self, *element: BaseWidget):
        """
        Link a tk-widget to the frame.
        When the frame's background-color is changed, the background-color of this widget is changed too
        :param element:
        :return:
        """
        self._linked_background_elements.extend(element)

    _background_color_initial: Color | str = None
    _pass_down_background_color: bool = False
    def _update_special_key(self,key:str,new_val:Any) -> bool|None:

        match key:
            case "apply_parent_background_color":
                if new_val:
                    self.add_flags(ElementFlag.APPLY_PARENT_BACKGROUND_COLOR)
                else:
                    self.remove_flags(ElementFlag.APPLY_PARENT_BACKGROUND_COLOR)
            
            case "pass_down_background_color":
                self._pass_down_background_color = new_val

            case "background_color":
                if not self.has_flag(ElementFlag.IS_CREATED):
                    self._background_color_initial = new_val
                    self._background_color = new_val
                    return True

                #self._background_color = new_val
                self.tk_widget.configure(background = new_val)

                faulty = list() # Faulty indexes that should be removed
                for n,row in enumerate(self._containing_frames):
                    try:
                        row.configure(background=new_val)
                    except tk.TclError:
                        faulty.append(n)

                # Remove faulty indexes
                for i in faulty[::-1]:
                    del self._containing_frames[i]

                for elem in self._linked_background_elements:
                    elem._update_initial(background_color=new_val)

                if self._pass_down_background_color:
                    for i in self._contains:
                        for elem in i:
                            if elem.has_flag(ElementFlag.APPLY_PARENT_BACKGROUND_COLOR):
                                elem._update_initial(background_color=new_val)
            case _:
                return super()._update_special_key(key, new_val)

        return True

    def init_window_creation_done(self):
        super().init_window_creation_done()
        if self._background_color_initial is not None:
            self._update_initial(background_color=self._background_color_initial)

    def add_element_to_row(self, element: BaseElement, row_number: int = -1, add_as_contained_element = True) -> Self:
        """
        Append a single element to a row

        :param element:
        :param row_number:
        :param add_as_contained_element: Leave this to True!
        :return:
        """
        if add_as_contained_element:
            self._contains[row_number].append(element)

        # BCP
        if self.has_flag(ElementFlag.IS_CREATED) and self._pass_down_background_color and element.has_flag(ElementFlag.APPLY_PARENT_BACKGROUND_COLOR):
            element._update_initial(background_color=self._background_color)

        element._init(self._containing_row_elements[row_number], self.window)

        return self

    def add_row(self, row: Iterable[BaseElement] = tuple(), add_as_contained_row: bool = True, **insert_kwargs) -> Self:
        """
        Add a single row to the end of the frame
        :param add_as_contained_row: Just leave it True.
        :param row:
        """
        # line = tk.Frame(self._tk_widget,background="orange",relief="raised",borderwidth="3",border=3)
        # actual_line = tk.Frame(line,background="lightBlue",borderwidth=3,border=3,relief="raised")
        if add_as_contained_row:
            row = list(row)
            self._contains.append(row)

        line = tk.Frame(self._tk_widget,relief="flat",background=self._background_color)  # This is the row
        actual_line = tk.Frame(line,background=self._background_color)    # This is where the actual elements are put in
        self._containing_frames.extend((line, actual_line)) # This might be redundant, but it is compatible with GridFrame, so...
        self._containing_row_frames.append(line)    # Store this line/row so it can be deleted later

        line_elem = BaseElement()
        line_elem._fake_tk_element = actual_line
        self._containing_row_elements.append(line_elem)

        expand = False
        expand_y = False

        for k in row:
            self.add_element_to_row(k, row_number=-1, add_as_contained_element=False)
            #k._init(line_elem,self.window)

            if not expand and k.has_flag(ElementFlag.EXPAND_ROW):
                expand = True

            if not expand_y and k.has_flag(ElementFlag.EXPAND_VERTICALLY):
                expand_y = True

        if expand and expand_y:
            insert_kwargs["fill"] = "both"
            insert_kwargs["expand"] = True
        elif expand:
            insert_kwargs["fill"] = "x"
            insert_kwargs["expand"] = True
        elif expand_y:
            insert_kwargs["fill"] = "y"
            insert_kwargs["expand"] = True
        else:
            insert_kwargs["fill"] = "none"
            insert_kwargs["expand"] = False

        if expand_y:
            line.pack(fill="both", expand=True)
        else:
            line.pack(fill="x")
        actual_line.pack(**insert_kwargs)

        if self._grab_anywhere_on_this:
            self.window.bind_grab_anywhere_to_element(line)
            self.window.bind_grab_anywhere_to_element(actual_line)

        # BCP
        if self.has_flag(ElementFlag.IS_CREATED) and self._pass_down_background_color:
            line.configure(bg=self._background_color_initial)
            actual_line.configure(bg=self._background_color_initial)

        return self

    def delete_row(self, row_number: int = -1) -> Self:
        """
        Truely delete a full row from the frame
        :param row_number: negative indexes are permitted
        :return:
        """

        for elem in self._contains[row_number]:
            if hasattr(elem, "delete"):
                elem.delete()

        self._containing_row_frames[row_number].destroy()
        del self._containing_row_elements[row_number]
        del self._contains[row_number]
        del self._containing_row_frames[row_number]

        return self

    _containing_frames: list[tk.Frame]  # All frames, including the "outer" rows
    _containing_row_elements: list[BaseElement]    # "Fake-elements" of the frame that contains the elements per row
    _background_color: str | Color
    def _init_containing(self):
        """
        Initialize all contained widgets.
        :return:
        """
        ins_kwargs_rows = self._insert_kwargs_rows

        for row in self._contains.copy():
            self.add_row(row, add_as_contained_row=False, **ins_kwargs_rows)

    def delete(self) -> Self:
        for row in self._contains:
            for elem in row:
                if hasattr(elem, "delete"):
                    elem.delete()

        super().delete()


