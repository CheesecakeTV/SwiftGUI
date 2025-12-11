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
        super().__init__(key=key, tk_kwargs=tk_kwargs, expand=expand, expand_y=expand_y)

        self._contains = layout
        self._linked_background_elements = list()

        if self.defaults.single("background_color", background_color) and not apply_parent_background_color:
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
                    return True

                self.tk_widget.configure(background = new_val)

                for row in self._containing_row_frame_widgets:
                    row.configure(background=new_val)

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

    def add_row(self, row: Iterable[BaseElement], **insert_kwargs) -> Self:
        """
        Add a single row to the end of the frame
        """
        # line = tk.Frame(self._tk_widget,background="orange",relief="raised",borderwidth="3",border=3)
        # actual_line = tk.Frame(line,background="lightBlue",borderwidth=3,border=3,relief="raised")

        line = tk.Frame(self._tk_widget,relief="flat",background=self._background_color)  # This is the row
        actual_line = tk.Frame(line,background=self._background_color)    # This is where the actual elements are put in
        self._containing_row_frame_widgets.extend((line,actual_line))

        line_elem = BaseElement()
        line_elem._fake_tk_element = actual_line

        expand = False
        expand_y = False

        for k in row:
            k._init(line_elem,self.window)

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

        return self

    _containing_row_frame_widgets: list[tk.Frame]
    _background_color: str | Color
    def _init_containing(self):
        """
        Initialize all contained widgets.
        :return:
        """
        ins_kwargs_rows = self._insert_kwargs_rows

        for row in self._contains:
            self.add_row(row, **ins_kwargs_rows)
