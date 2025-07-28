import tkinter.ttk as ttk
import tkinter.font as font
from collections.abc import Iterable, Callable
from typing import Literal, Any

from SwiftGUI import ElementFlag, BaseWidget, GlobalOptions, Literals, Color, BaseWidgetTTK


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

        if value is None:
            value = ""

        self.attached_table.tk_widget.set( # Change value in Treeview
            str(hash(self)),
            column=key,
            value=value,
        )
        # No need to refresh the whole tablerow (Hope this doesn't bite me in the butt later...)

    def __delitem__(self, key):
        super().__delitem__(key)
        self._refresh_my_tablerow()

    def __iadd__(self, other):
        super().__iadd__(other)
        self._refresh_my_tablerow()

    def __imul__(self, other):
        super().__imul__(other)
        self._refresh_my_tablerow()

    def __hash__(self):
        return self._id

    def append(self, __object):
        super().append(__object)
        self._refresh_my_tablerow()

    def extend(self, __iterable):
        super().extend(__iterable)
        self._refresh_my_tablerow()

    def insert(self, __index, __object):
        super().insert(__index, __object)
        self._refresh_my_tablerow()

    def pop(self, __index = -1):
        r = super().pop(__index)
        return r

    def remove(self, __value):
        super().remove(__value)
        self._refresh_my_tablerow()

    def clear(self):
        super().clear()
        self._refresh_my_tablerow()

    def sort(self, *, key = None, reverse = False):
        super().sort(key = key, reverse = reverse)
        self._refresh_my_tablerow()

    def _refresh_my_tablerow(self):
        """
        Refresh this row in the connected sg.Table
        :return:
        """
        self.attached_table @ self  # Refresh table (at me)

    def overwrite(self, new_vals: Iterable[Any]):
        """
        Basically replace this list with another but keeping its reference (id) intact
        :param new_vals: Guess.
        :return:
        """
        new_vals = tuple(new_vals)

        while len(self) < len(new_vals):
            super().append(None)

        while len(self) > len(new_vals):
            super().__delitem__(-1)

        for i in range(len(new_vals)):
            super().__setitem__(i, new_vals[i])

        self._refresh_my_tablerow()

    def __eq__(self, other):
        if isinstance(other,TableRow):  # Make comparisons a little quicker (hopefully)
            return hash(self) == hash(other)

        return super().__eq__(other)

class Table(BaseWidgetTTK):
    tk_widget:ttk.Treeview
    _tk_widget:ttk.Treeview
    _tk_widget_class:type = ttk.Treeview # Class of the connected widget
    defaults = GlobalOptions.Table

    _styletype:str = "Treeview"

    _transfer_keys = {
        # "background_color_disabled":"disabledbackground",
        "background_color":"background",
        # "text_color_disabled": "disabledforeground",
        "highlightbackground_color": "highlightbackground",
        "selectbackground_color": "selectbackground",
        "select_text_color": "selectforeground",
        # "pass_char":"show",
        "background_color_active" : "activebackground",
        "text_color_active" : "activeforeground",
        "text_color":"foreground",
    }

    _elements: list[TableRow[Any]]  # Elements the Table contains atm
    table_elements: tuple[TableRow[Any]]   # Prevent users from tampering with _elements...
    _element_dict: dict[int:TableRow[Any]] # Hash:Element ~ Elements as a dict to find them quicker

    _headings: tuple    # Column headings

    # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/ttk-Treeview.html
    def __init__(
            self,
            # Add here
            elements: Iterable[Iterable[Any]] = None,
            /,
            key: Any = None,
            key_function: Callable|Iterable[Callable] = None,
            default_event: bool = False,

            headings: Iterable[str] = ("Forgot to add headings?",),

            expand: bool = None,
            tk_kwargs: dict[str:any]=None
    ):
        super().__init__(key=key,tk_kwargs=tk_kwargs,expand=expand)

        self._elements = list()
        self._element_dict = dict()

        if elements is None:
            elements = list()
        self._elements_initial = elements

        self._headings = tuple(headings)
        self._headings_len = len(self._headings)

        if tk_kwargs is None:
            tk_kwargs = dict()

        self.update(
            columns = self._headings,
            **tk_kwargs,
            selectmode= "browse",
            #text_color = "red",
            #font = ("Heveteca",12)
        )

        if default_event:
            self.bind_event("<<TreeviewSelect>>",key=key,key_function=key_function)

    @property
    def table_elements(self):
        return tuple(self._elements)

    @table_elements.setter
    def table_elements(self, new_val):
        raise AttributeError("You tried to set table_elements directly on a sg.Table. Don't do that.\nsg.Table has a lot of functions you can use to change elements.")

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
            case "elements":
                self.overwrite_table(new_val)
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
        temp = self.index

        if temp is None:
            return None

        return self._element_dict[str(hash(self._elements[temp]))]

    def set_value(self,val:any):
        print("Warning!","It is not possible to set Values of sg.Table (yet)!")
        print("     use .index to set the selected item")

    def __getitem__(self, item: int):
        """
        Get the item at specified index
        :param item:
        :return:
        """
        return self._elements[item]

    def __setitem__(self, index: int, row: Iterable[Any]):
        """
        Overwrite the whole row at said position.
        :param index: Element to edit
        :param row: Values of the new row. WARNING! IF YOU PASS A TABLE-ROW, ITS REFERENCE WILL BE DETACHED!
        :return:
        """
        old_row = self._elements[index]

        if row is None: # No idea why this is necessary, but somehow it is...
            return

        old_row.overwrite(row)

    def __delitem__(self, index: int):
        """
        Remove an entire row from the list
        :param index:
        :return:
        """
        row = self._elements[index]
        del self._elements[index]

        iid = str(hash(row))
        del self._element_dict[iid]

        self.tk_widget.delete(iid)

    def __matmul__(self, other: TableRow):
        """
        Refresh some row.
        Don't use, it's just for me!
        :param other:
        :return:
        """
        tag = str(hash(other))
        if len(other) < self._headings_len:
            other = other + [""] * (self._headings_len - len(other))

        for n,val in zip(range(self._headings_len), other):
            self.tk_widget.set(tag, column=n, value=val)

    def index_of(self, item: TableRow | Iterable[Any]) -> int | None:
        """
        Finds the index of a given item.
        :param item: Can be an actual TableRow, or any iterable.
        :return:
        """
        if isinstance(item, TableRow):
            return self._element_dict.get(str(hash(item)))

        return self._elements.index(TableRow(self, item))

    def __len__(self):
        """Item-Count"""
        return len(self._elements)

    @property
    def index(self) -> int | None:
        """
        Selected row (index)
        :return:
        """
        temp = self.tk_widget.focus()

        if not temp:
            return None

        return self._elements.index(self._element_dict[temp])

    @index.setter
    def index(self, new_index: int):
        self.set_index(new_index)

    def set_index(self, new_index: int):
        """
        Select a specified row of the table

        Same as .index = new_index
        :param new_index: Index of the row to select
        :return:
        """
        if not new_index:
            self.tk_widget.selection_set()
            self.tk_widget.focus("")
            return

        temp = str(hash(self._elements[new_index]))
        self.tk_widget.selection_set(temp)
        self.tk_widget.focus(temp)

    def init_window_creation_done(self):
        """Don't touch!"""
        super().init_window_creation_done()

        if self._headings:
            headings = iter(self._headings)

            for n,h in enumerate(headings):
                self.tk_widget.heading(n,text=h)

        self.tk_widget["show"] = "headings"   # Removes first column

        self.insert_multiple(self._elements_initial,0)
        del self._elements_initial

    def insert(self,row: Iterable[Any], index: int) -> TableRow:
        """
        Append a single row to the Table.
        The returned object can be used to modify that row.
        :param index: Item will be added BEFORE this. Pass "end" for it to work like .append
        :param row: The element to add
        :return: Added element. You may edit this to edit the row itself.
        """
        row = TableRow(self,row)

        self._elements.insert(index, row)
        self._element_dict[str(hash(row))] = row
        self.tk_widget.insert("",index=index,values=row,iid=hash(row))

        return row

    def insert_multiple(self,rows:Iterable[Iterable[Any]], index: int) -> tuple[TableRow, ...]:
        """
        Insert multiple rows at once.
        They will be ordered like the list you pass, starting at the index you pass
        :param rows:
        :param index:
        :return: Tuple of all the rows you added
        """
        r = []
        for row in rows:
            r.append(self.insert(row,index))
            index += 1

        return tuple(r)

    def clear_whole_table(self):
        """
        Clear the whole table leaving it blank
        :return:
        """
        iids = map(str, map(hash, self._elements))

        self.tk_widget.delete(*iids)

        self._elements = list()
        self._element_dict = dict()

    def overwrite_table(self, new_table: Iterable[Iterable[Any]]):
        """
        Clear the whole table and replace its elements with a new table.
        :param new_table:
        :return:
        """
        self.clear_whole_table()
        self.insert_multiple(new_table, 0)

    def append(self,row: Iterable[Any]) -> TableRow:
        """
        Append a single row to the Table.
        The returned object can be used to modify that row.
        :param row:
        :return: Added element. You may edit this to edit the row itself.
        """
        row = TableRow(self,row)
        self._elements.append(row)
        self._element_dict[str(hash(row))] = row

        self.tk_widget.insert("",index = "end",values=row,iid=hash(row))
        return row

    def extend(self,rows: Iterable[Iterable[Any]]) -> tuple[TableRow,...]:
        """
        Append multiple rows at once (like extend)
        :param rows:
        :return: Tuple of all added elements
        """
        r = []
        for row in rows:
            r.append(self.append(row))

        return tuple(r)

    def move(self,from_index: int, to_index: int) -> None:
        """
        Move a row from one index to another.
        Pass negative values to index the last n elements like you do with lists.

        :param from_index:
        :param to_index: Item will have this index afterwards.
        :return:
        """
        row_from = self._elements[from_index]
        if to_index < 0:
            to_index = len(self) + to_index

        self.tk_widget.move(str(hash(row_from)), "", to_index)

        row_from = self._elements.pop(from_index)
        self._elements.insert(to_index, row_from)

    def move_up(self, index: int, n: int = 1):
        """
        Move one row up n places
        :param index: What row to move
        :param n: How many rows
        :return:
        """
        index_new = max(index - n, 0)
        self.move(index, index_new)

    def move_down(self, index: int, n: int = 1):
        """
        Move one row down n places
        :param index: What row to move
        :param n: How many rows
        :return:
        """
        index_new = min(index + n, len(self._elements) - 1)
        self.move(index, index_new)

    def swap(self, index1: int, index2: int):
        """
        Swap two rows

        :param index1:
        :param index2:
        :return:
        """
        if index1 == index2:
            return

        if index1 < 0:
            index1 = len(self._elements) + index1

        if index2 < 0:
            index2 = len(self._elements) + index2

        if index1 > index2: # Force index1 < index2
            index2, index1 = index1, index2

        self.move(index2, index1 + 1)
        self.move(index1, index2)

    def see(self, index: int = 0):
        """
        Scroll through the list to see a certain index.
        :param index: Row to view
        :return:
        """
        self.tk_widget.see(str(hash(self._elements[index])))


