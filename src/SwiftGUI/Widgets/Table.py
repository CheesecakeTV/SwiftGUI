import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as font
from collections.abc import Iterable, Callable
from typing import Literal, Any
from warnings import deprecated

from SwiftGUI import ElementFlag, BaseWidget, GlobalOptions, Literals, Color

class TableRow(list):
    """
    A row in a Table-Object
    """
    attached_table:"Table" = None
    _id:int = -1    # This will count up to act as an unique hash for every row

    def __init__(self,my_table:"Table",iterable:Iterable = tuple()):
        super().__init__(iterable)
        self.attached_table = my_table

        TableRow._id += 1
        self._id = TableRow._id

    def __setitem__(self, key, value):
        super().__setitem__(key,value)
        self.refresh_my_tablerow()

    def __delitem__(self, key):
        super().__delitem__(key)
        self.refresh_my_tablerow()

    def __iadd__(self, other):
        super().__iadd__(other)
        self.refresh_my_tablerow()

    def __imul__(self, other):
        super().__imul__(other)
        self.refresh_my_tablerow()

    def __hash__(self):
        return self._id

    def refresh_my_tablerow(self):
        """
        Refresh this row in the connected sg.Table
        :return:
        """
        ...

class Table(BaseWidget):
    tk_widget:ttk.Treeview
    _tk_widget:ttk.Treeview
    _tk_widget_class:type = ttk.Treeview # Class of the connected widget
    defaults = GlobalOptions.Table

    _transfer_keys = {
        # # "background_color_disabled":"disabledbackground",
        # "background_color":"background",
        # # "text_color_disabled": "disabledforeground",
        # "highlightbackground_color": "highlightbackground",
        # "selectbackground_color": "selectbackground",
        # "select_text_color": "selectforeground",
        # # "pass_char":"show",
        # "background_color_active" : "activebackground",
        # "text_color_active" : "activeforeground",
        # "text_color":"fg",
    }

    elements: list[TableRow[Any]]  # Elements the Table contains atm
    _element_dict: dict[int:TableRow[Any]] # Hash:Element ~ Elements as a dict to find them quicker

    _headings: tuple    # Column headings

    def __init__(
            self,
            # Add here
            #elements: dict|Iterable[Iterable[str]] = None,
            /,
            key: Any = None,
            key_function: Callable|Iterable[Callable] = None,
            default_event: bool = False,

            headings: Iterable[str] = ("Forgot to add headings?",),

            expand: bool = None,
            tk_kwargs: dict[str:any]=None
    ):
        super().__init__(key=key,tk_kwargs=tk_kwargs,expand=expand)

        # if elements is None:
        #     elements = dict()
        self.elements = list()
        self._element_dict = dict()

        self._headings = tuple(headings)
        self._headings_len = len(self._headings)

        if tk_kwargs is None:
            tk_kwargs = dict()

        self.update(
            columns = self._headings,
            **tk_kwargs,
            selectmode= "browse",
        )

        if default_event:
            self.bind_event("<<TreeviewSelect>>",key=key,key_function=key_function)

    can_reset_value_changes = False
    def _update_special_key(self,key:str,new_val:any) -> bool|None:
        match key:

            case "readonly":
                self._tk_kwargs["state"] = "disabled" if new_val else "normal"
            case "fonttype":
                self._fonttype = self.defaults.single(key,new_val)
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "fontsize":
                self._fontsize = self.defaults.single(key,new_val)
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "font_bold":
                self._bold = self.defaults.single(key,new_val)
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "font_italic":
                self._italic = self.defaults.single(key,new_val)
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "font_underline":
                self._underline = self.defaults.single(key,new_val)
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "font_overstrike":
                self._overstrike = self.defaults.single(key,new_val)
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "text":
                self.value = new_val
            case "tabs":
                self._tabsize = new_val
                self.add_flags(ElementFlag.UPDATE_FONT)
            case _:
                return False

        return True

    def _apply_update(self):
        # If the font changed, apply them to self._tk_kwargs
        if self.has_flag(ElementFlag.UPDATE_FONT):
            self._update_font()

        super()._apply_update() # Actually apply the update

    def _personal_init(self):
        # self._tk_kwargs.update({
        #     "command": self.window.get_event_function(self, self.key, self._key_function)
        # })

        super()._personal_init()

    def _update_font(self):
        # self._tk_kwargs will be passed to tk_widget later
        temp = font.Font(
            self.window.parent_tk_widget,
            family=self._fonttype,
            size=self._fontsize,
            weight="bold" if self._bold else "normal",
            slant="italic" if self._italic else "roman",
            underline=bool(self._underline),
            overstrike=bool(self._overstrike),
        )
        self._tk_kwargs["font"] = temp

        if self._tabsize is not None:
            self._tk_kwargs["tabs"] = self._tabsize * temp.measure(" ")

    def _get_value(self) -> TableRow[str,...] | None:
        temp = self.selection

        if temp is None:
            return None

        return self._element_dict[str(temp)]

    def set_value(self,val:any):
        print("Warning!","It is not possible to set Values of sg.Treeview (yet)!")

    selection:tuple[str]

    @property
    def selection(self) -> int | None:
        """
        Selected row (index)
        :return:
        """
        temp = self.tk_widget.focus()

        if temp:
            return int(temp)

        return None

    @selection.setter
    def selection(self, new_val: int):
        if not new_val:
            self.tk_widget.selection_set()
            self.tk_widget.focus("")
            return

        temp = str(hash(self.elements[new_val]))
        self.tk_widget.selection_set(temp)
        self.tk_widget.focus(temp)

    def init_window_creation_done(self):
        """Don't touch!"""
        super().init_window_creation_done()

        if self._headings:
            headings = iter(self._headings)

            for h in headings:  # Deploy the remaining ones
                self.tk_widget.heading(h,text=h)

        self.tk_widget["show"] = "headings"   # Removes first column

    def append(self,row: Iterable[Any]) -> TableRow:
        """
        Append a single row to the Table.
        The returned object can be used to modify that row.
        :param row:
        :return:
        """
        row = TableRow(self,row)
        self.elements.append(row)
        self._element_dict[str(hash(row))] = row

        type(self.tk_widget.insert("","end",values=row,iid=hash(row)))

        return row


