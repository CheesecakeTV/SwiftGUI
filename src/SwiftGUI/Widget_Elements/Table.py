import tkinter
import tkinter.ttk as ttk
from collections.abc import Iterable, Callable, Iterator
from functools import partial
from tkinter import font
from typing import Any, Self

from SwiftGUI import ElementFlag, GlobalOptions, Literals, Color, BaseWidgetTTK, BaseElement


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
            default_event: bool = False,
            key_function: Callable|Iterable[Callable] = None,

            headings: Iterable[str] = ("Forgot to add headings?",),
            column_width: int | Iterable[int] = None,

            sort_col_by_click: bool = None,
            selectmode: Literals.selectmode_tree = None,
            scrollbar: bool = None,

            # Fonts
            fonttype: str = None,
            fontsize: int = None,
            font_bold: bool = None,
            font_italic: bool = None,
            font_underline: bool = None,
            font_overstrike: bool = None,

            fonttype_headings: str = None,
            fontsize_headings: int = None,
            font_bold_headings: bool = None,
            font_italic_headings: bool = None,
            font_underline_headings: bool = None,
            font_overstrike_headings: bool = None,

            background_color: str | Color = None,
            background_color_rows: str | Color = None,
            background_color_active_rows: str | Color = None,
            background_color_headings: str | Color = None,
            background_color_active_headings: str | Color = None,

            text_color: str | Color = None,
            text_color_active: str | Color = None,
            text_color_headings: str | Color = None,
            text_color_active_headings: str | Color = None,

            cursor: Literals.cursor = None,
            height: int = None,
            padding: int | tuple[int, ...] = None,

            takefocus: bool = None,
            expand: bool = None,
            expand_y: bool = None,
            tk_kwargs: dict[str:any]=None
    ):
        super().__init__(key=key,tk_kwargs=tk_kwargs,expand=expand, expand_y = expand_y)

        if self.defaults.single("scrollbar", scrollbar):
            self.add_flags(ElementFlag.HAS_SCROLLBAR_Y)

        self._elements = list()
        self._element_dict = dict()

        if elements is None:
            elements = list()
        self.insert_multiple(elements, 0)

        self._headings = tuple(headings)
        self._headings_len = len(self._headings)

        if tk_kwargs is None:
            tk_kwargs = dict()

        self.update(
            columns = self._headings,
            column_width = column_width,
            **tk_kwargs,
            selectmode = selectmode,

            background_color = background_color,

            background_color_rows = background_color_rows,
            background_color_active_rows = background_color_active_rows,

            background_color_headings = background_color_headings,
            background_color_active_headings = background_color_active_headings,

            text_color= text_color,
            text_color_active= text_color_active,
            text_color_headings= text_color_headings,
            text_color_active_headings = text_color_active_headings,

            fonttype = fonttype,
            fontsize = fontsize,
            font_bold = font_bold,
            font_italic = font_italic,
            font_underline = font_underline,
            font_overstrike = font_overstrike,

            fonttype_headings=fonttype_headings,
            fontsize_headings=fontsize_headings,
            font_bold_headings=font_bold_headings,
            font_italic_headings=font_italic_headings,
            font_underline_headings=font_underline_headings,
            font_overstrike_headings=font_overstrike_headings,

            sort_col_by_click=sort_col_by_click,
            takefocus=takefocus,

            # New ones
            height = height,
            cursor = cursor,
            padding = padding,

        )

        if default_event:
            self.bind_event("<<TreeviewSelect>>",key=key,key_function=key_function)

    _last_sort_direction: bool = None  # True, if sorted non-reversed, False if sorted reversed
    _last_sort_col: int = -1    # Col that got sorted last time
    def _col_click_callback(self, column: int, *_):
        """
        Gets called when a column is clicked
        :param column:
        :return:
        """
        if self._sort_col_by_click:
            if self._last_sort_col != column:
                self._last_sort_direction = True
                self._last_sort_col = column

            self._last_sort_direction = not self._last_sort_direction
            self.sort(
                column,
                empty_to_back=not self._last_sort_direction,
                reverse=self._last_sort_direction
            )

    @BaseElement._run_after_window_creation
    def resize_column(self, column: str | int, new_width: int) -> Self:
        """
        Resize a single column's width
        :param column: index of the column or its name
        :param new_width:
        :return:
        """
        if isinstance(column, str):
            assert column in self._headings, "You tried to resize a Table-Column that doesn't exist. Remember that column names are case-sensitive"
            column = self._headings.index(column)

        self.tk_widget.column(column, width= new_width * self._font_size_multiplier)
        return self

    @BaseElement._run_after_window_creation
    def sort(self, by_column:int | str = None, key: Callable = None, reverse: bool = False, empty_to_back: bool = True) -> Self:
        """
        Sort the whole table either:
        - The normal way (First column takes priority, then second, ...)
        - By a column (normal sort method on that column)
        - By a function (key) that gets passed the whole row
        - By a function (key) that gets passed only the value of the by_column-column

        :param empty_to_back: True, if empty (None or "") values should get the lowest priority. by_column MUST BE DEFINED!
        :param by_column: Pass a string (name of the column) or its index. If multiple columns have the same name, first one will be used.
        :param key: Key function. Same as .sort on lists. If you pass by_column, this function will receive ONLY THE VALUE OF THAT COLUMN
        :param reverse: True, if order should be reversed
        :return: sg.Table-Element for inline calls
        """
        if isinstance(by_column, str):
            assert by_column in self._headings, "You tried to sort a Table by a column that doesn't exist. Recheck your arguments, column-names are case-sensitive."
            by_column = self._headings.index(by_column)

        if not self._elements:
            return self

        if by_column is None and key is None:
            sort_fkt = lambda a:a   # Normal sort.

        elif by_column is None:
            sort_fkt = key

        elif key is None:
            sort_fkt = lambda a:a[by_column]

        else:
            sort_fkt = lambda a:key(a[by_column])

        if by_column is not None:
            def sort_fkt_final(a):
                if a[by_column] is None or a[by_column] == "":
                    return (empty_to_back,)  # 1 will be on the end

                return not empty_to_back, sort_fkt(a)   # 0 will be on the start
        else:
            sort_fkt_final = sort_fkt

        self._elements.sort(key= sort_fkt_final, reverse=reverse)

        iids = list(self._get_all_iids(self._elements))
        #self.tk_widget.detach(*iids)   # Not necessary and might clear selection. Just moving is more elegant
        for n,iid in enumerate(iids):
            self.tk_widget.move(iid, "", n)

        return self

    @staticmethod
    def _get_all_iids(elements: Iterable[TableRow]) -> Iterator[str]:
        """
        Returns a generator with all iids of the passed elements
        :param elements:
        :return:
        """
        return map(str, map(hash, elements))

    @property
    def table_elements(self):
        return tuple(self._elements)

    @table_elements.setter
    def table_elements(self, new_val):
        raise AttributeError("You tried to set table_elements directly on an sg.Table. If you want to replace the whole table, use .overwrite_table instead.\n"
                             "I highly recommend not overwriting the whole table though, sg.Table offers a lot of methods to change it.")

    def _update_special_key(self,key:str,new_val:any) -> bool|None:
        match key:
            case "column_width":
                if new_val is None:
                    return True

                if isinstance(new_val, int):
                    new_val = (new_val, ) * self._headings_len

                self._col_width_requested = new_val

                for n,val in enumerate(new_val):
                    self.resize_column(n, val)
            case "sort_col_by_click":
                self._sort_col_by_click = new_val
            case "readonly":
                self._tk_kwargs["state"] = "disabled" if new_val else "normal"

            case "text_color":
                self._map_ttk_style(foreground = [
                    ("!selected",new_val)]
                )
            case "text_color_headings":
                self._map_ttk_style(foreground=[
                    ("!pressed", new_val)]
                    , style_ext = "Heading")

            case "text_color_active":
                self._map_ttk_style(foreground = [
                    ("selected",new_val)]
                )
            case "text_color_active_headings":
                self._map_ttk_style(foreground=[
                    ("pressed", new_val)]
                    , style_ext = "Heading")

            case "background_color":
                self._config_ttk_style(fieldbackground=new_val)
            case "background_color_rows":
                self._map_ttk_style(background = [
                    ("!selected",new_val)]
                )
            case "background_color_active_rows":
                self._map_ttk_style(background = [
                    ("selected",new_val)]
                )

            case "background_color_headings":
                self._map_ttk_style(background=[
                    ("!pressed", new_val)]
                , style_ext="Heading")
            case "background_color_active_headings":
                self._map_ttk_style(background=[
                    ("pressed", new_val)]
                , style_ext = "Heading")

            case "fonttype":
                self._fonttype = self.defaults.single(key,new_val)
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "fontsize":
                self._fontsize = self.defaults.single(key,new_val)
                self.add_flags(ElementFlag.UPDATE_FONT)
                self._config_ttk_style(rowheight= new_val + 10)
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

            case "fonttype_headings":
                self._fonttype_headings = self.defaults.single(key,new_val)
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "fontsize_headings":
                self._fontsize_headings = self.defaults.single(key,new_val)
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "font_bold_headings":
                self._bold_headings = self.defaults.single(key,new_val)
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "font_italic_headings":
                self._italic_headings = self.defaults.single(key,new_val)
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "font_underline_headings":
                self._underline_headings = self.defaults.single(key,new_val)
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "font_overstrike_headings":
                self._overstrike_headings = self.defaults.single(key,new_val)
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
        super()._personal_init()

        if self.has_flag(ElementFlag.HAS_SCROLLBAR_Y):
            self.tk_widget.configure(yscrollcommand=self._tk_scrollbar_y.set)
            self._tk_scrollbar_y.configure(command=self.tk_widget.yview)

    _font_size_multiplier: int = 1  # Size of a single character in pixels
    _font_size_multiplier_applied: int = 1  # Applied value so to catch changes
    _col_width_requested: int | Iterable[int] = None    # What the user wants as col-width
    def _update_font(self):
        font_options = [
            self._fonttype,
            self._fontsize,
        ]

        if self._bold:
            font_options.append("bold")

        if self._italic:
            font_options.append("italic")

        if self._underline:
            font_options.append("underline")

        if self._overstrike:
            font_options.append("overstrike")

        self._config_ttk_style(font=font_options)

        self._font_size_multiplier = font.Font(
            self.window.parent_tk_widget,
            family=self._fonttype,
            size=self._fontsize,
            weight="bold" if self._bold else "normal",
            slant="italic" if self._italic else "roman",
            underline=bool(self._underline),
            overstrike=bool(self._overstrike),
        ).measure("X_") // 2
        if self._col_width_requested and self._font_size_multiplier != self._font_size_multiplier_applied:
            self._font_size_multiplier_applied = self._font_size_multiplier
            self.update(column_width=self._col_width_requested)

        # And now for the headings
        font_options = [
            self._fonttype_headings if self._fontsize_headings else self._fonttype,
            self._fontsize_headings if self._fontsize_headings else self._fontsize,
        ]

        if self._bold_headings:
            font_options.append("bold")

        if self._italic_headings:
            font_options.append("italic")

        if self._underline_headings:
            font_options.append("underline")

        if self._overstrike_headings:
            font_options.append("overstrike")

        self._config_ttk_style("Heading",font=font_options)

    def _get_value(self) -> TableRow[str,...] | None:
        temp = self.index

        if temp is None:
            return None

        return self._element_dict[str(hash(self._elements[temp]))]

    def set_value(self,val:any):
        print("Warning!","It is not possible to set Values of sg.Table (yet)!")
        print("     use .index to set the selected item")

    def __getitem__(self, item: int) -> TableRow:
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

    @property
    def all_indexes(self) -> tuple[int, ...]:
        """
        Returns a tuple of all selected indexes
        :return:
        """
        selections = self.tk_widget.selection()
        selections = map(self._element_dict.get, selections)
        selections = map(self._elements.index, selections)
        return tuple(selections)

    @all_indexes.setter
    def all_indexes(self, new_vals: Iterable[int]):
        """
        Select all the passed indexes
        :param new_vals:
        :return:
        """
        self.set_all_indexes(new_vals)

    def set_all_indexes(self, new_vals: Iterable[int]):
        """
        Select all the passed indexes
        :param new_vals:
        :return:
        """
        new_vals = tuple(new_vals)

        # if new_vals:  # No need, .value and .index don't work in extended mode anyways
        #     self.set_index(new_vals[0])
        # else:
        #     self.set_index(None)
        self.set_index(None)
        if not new_vals:
            return

        new_vals = map(self._elements.__getitem__, new_vals)
        new_vals = tuple(self._get_all_iids(new_vals))
        self.tk_widget.selection_add(new_vals)

    @property
    def all_values(self) -> tuple[TableRow, ...]:
        """
        Returns a tuple of all selected indexes
        :return:
        """
        selections = self.tk_widget.selection()
        selections = map(self._element_dict.get, selections)
        return tuple(selections)

    def set_index(self, new_index: int | None):
        """
        Select a specified row of the table

        Same as .index = new_index
        :param new_index: Index of the row to select. To clear the selection, pass None
        :return:
        """
        if new_index is None:
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
                self.tk_widget.heading(n,text=h,command=partial(self._col_click_callback, n))   # Set callback to always pass the col-ID

        self.tk_widget["show"] = "headings"   # Removes first column

        #self._map_ttk_style(background = [("selected", "blue")])

    def insert(self,row: Iterable[Any], index: int) -> TableRow:
        """
        Append a single row to the Table.
        The returned object can be used to modify that row.
        :param index: Item will be added BEFORE this. Pass "end" for it to work like .append
        :param row: The element to add
        :return: Added element. You may edit this to edit the row itself.
        """
        assert self._elements_before_filter is None, "You can not insert an element into a table while a filter is active. Use .reset_filter() to undo it, or .persist_filter() to keep the current table."

        row = TableRow(self,row)

        self._elements.insert(index, row)
        self._element_dict[str(hash(row))] = row
        self.tk_widget.insert("",index=index,values=row,iid=hash(row))

        return row

    @BaseElement._run_after_window_creation
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
        self.reset_filter()

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
        self.reset_filter()
        self.clear_whole_table()
        # self._default_elements = list(self.insert_multiple(new_table, 0))
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

        if self._elements_before_filter is not None:
            self._elements_before_filter.append(row)

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

    def move(self,from_index: int, to_index: int) -> Self:
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

        return self

    def move_up(self, index: int, n: int = 1) -> Self:
        """
        Move one row up n places
        :param index: What row to move
        :param n: How many rows
        :return:
        """
        index_new = max(index - n, 0)
        self.move(index, index_new)
        return self

    def move_down(self, index: int, n: int = 1) -> Self:
        """
        Move one row down n places
        :param index: What row to move
        :param n: How many rows
        :return:
        """
        index_new = min(index + n, len(self._elements) - 1)
        self.move(index, index_new)
        return self

    def swap(self, index1: int, index2: int) -> Self:
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
        return self

    @BaseElement._run_after_window_creation
    def see(self, index: int = 0) -> Self:
        """
        Scroll through the list to see a certain index.
        :param index: Row to view
        :return:
        """
        self.tk_widget.see(str(hash(self._elements[index])))
        return self

    @BaseElement._run_after_window_creation
    def see_selection(self) -> Self:
        """
        Scroll the table so the current selection is visible.
        If nothing is selected, this function does nothing.
        :return:
        """
        if self.all_indexes:
            self.see(self.all_indexes[0])
        elif self.index is not None:
            self.see(self.index)

        return self

    @property
    def filter_mode(self) -> bool:
        """
        Returns True, if the table is in filter-mode
        :return:
        """
        return bool(self._elements_before_filter)

    @filter_mode.setter
    def filter_mode(self, new_val: bool):
        if not new_val:
            self.reset_filter()

    _elements_before_filter: list[TableRow] | None = None   # When filter is applied, this saves the original state
    @BaseElement._run_after_window_creation
    def filter(self, key: Callable, by_column:int | str = None, only_remaining_rows:bool = False) -> Self:
        """
        Filter the whole table either:
        - If no by_column is passed, the function will be applied to the whole column
        - If by_column is passed, only the specified column will be passed to the filter-function (key)

        The previous state of the list is saved and can be restored using reset_filter().
        To apply the filter permanently, use persist_filter().

        :param only_remaining_rows: True, if only rows that are in the table right now should be filtered. False, if prior filters should be ignored.
        :param by_column: Pass a string (name of the column) or its index. If multiple columns have the same name, first one will be used.
        :param key: Key function. Truethy returns will be kept inside the list
        :return: sg.Table-Element for inline calls
        """
        if isinstance(by_column, str):
            assert by_column in self._headings, "You tried to filter a Table by a column that doesn't exist. Recheck your arguments, column-names are case-sensitive."
            by_column = self._headings.index(by_column)

        if not self._elements:
            return self

        if by_column is None:
            filter_fkt = key
        else:
            filter_fkt = lambda a:key(a[by_column])

        if self._elements_before_filter is None:
            self._elements_before_filter = self._elements.copy()

        if only_remaining_rows:
            filter_list = self._elements
        else:
            filter_list = self._elements_before_filter

        all_iids = set(self._get_all_iids(filter_list))

        self._elements = list(filter(filter_fkt, filter_list))

        iids_in = list(self._get_all_iids(self._elements))    # Elements to keep
        iids_out = all_iids.difference(set(iids_in)) # Elements to remove

        for n,iid in enumerate(iids_in):
            self.tk_widget.move(iid, "", n)

        self.tk_widget.detach(*iids_out)

        return self

    def reset_filter(self) -> Self:
        """
        Reset the filter-view to before it was filtered
        :return:
        """
        if not self._elements_before_filter:
            return self

        self._elements.clear()

        iids = list(self._get_all_iids(self._elements_before_filter))

        n = 0
        for iid, row in zip(iids, self._elements_before_filter):
            try:
                self.tk_widget.move(iid, "", n)
                self._elements.append(row)
                n += 1
            except tkinter.TclError:
                pass

        self._elements_before_filter = None

        return self

    @BaseElement._run_after_window_creation
    def persist_filter(self) -> Self:
        """
        Persist the filtered view so that it cannot be reset anymore
        :return:
        """
        all_iids = set(self._get_all_iids(self._elements_before_filter))
        iids_in = list(self._get_all_iids(self._elements))    # Elements to keep
        iids_out = all_iids.difference(set(iids_in)) # Elements to remove

        self.tk_widget.delete(*iids_out)
        self._elements_before_filter = None

        for iid in iids_out:
            del self._element_dict[iid]

        return self
