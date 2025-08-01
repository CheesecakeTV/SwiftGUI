import tkinter as tk
import tkinter.font as font
from collections.abc import Iterable, Callable
from typing import Self, Any

from SwiftGUI import ElementFlag, BaseWidget, GlobalOptions, Literals, Color


class Listbox(BaseWidget):
    _tk_widget_class: type = tk.Listbox  # Class of the connected widget
    tk_widget: tk.Listbox
    defaults = GlobalOptions.Listbox  # Default values (Will be applied to kw_args-dict and passed onto the tk_widget
    value: list

    _transfer_keys = {
        "background_color": "background",
        "text_color": "fg",
        "text_color_disabled": "disabledforeground",
        "highlightbackground_color": "highlightbackground",
        "text_color_selected": "selectforeground",
        "background_color_active": "activebackground",
        "text_color_active": "activeforeground",
        "background_color_selected": "selectbackground",
    }

    def __init__(
            self,
            default_list: Iterable[Any] = None,
            /,
            key: any = None,
            default_event: bool = False,
            key_function: Callable | Iterable[Callable] = None,
            activestyle: Literals.activestyle = None,
            fonttype: str = None,
            fontsize: int = None,
            font_bold: bool = None,
            font_italic: bool = None,
            font_underline: bool = None,
            font_overstrike: bool = None,
            disabled: bool = None,
            borderwidth:int = None,
            background_color: str | Color = None,
            background_color_selected: str | Color = None,
            selectborderwidth: int = None,
            text_color: str | Color = None,
            text_color_selected: str | Color = None,
            text_color_disabled: str | Color = None,
            selectmode: Literals.selectmode_single = None,
            width: int = None,
            height: int = None,
            cursor: Literals.cursor = None,
            takefocus: bool = None,
            relief: Literals.relief = None,
            highlightbackground_color: str | Color = None,
            highlightcolor: str | Color = None,
            highlightthickness: int = None,
            expand:bool = None,
            tk_kwargs: dict = None,
    ):
        super().__init__(key, tk_kwargs=tk_kwargs, expand=expand)

        self._key_function = key_function
        if default_list is None:
            default_list = list()
        self._list_elements = list(default_list)

        if tk_kwargs is None:
            tk_kwargs = dict()

        _tk_kwargs = {
            **tk_kwargs,
            "default_list": default_list,
            "activestyle":activestyle,
            "borderwidth":borderwidth,
            "font_bold": font_bold,
            "font_italic": font_italic,
            "font_overstrike": font_overstrike,
            "font_underline": font_underline,
            "fontsize": fontsize,
            "fonttype": fonttype,
            "disabled": disabled,
            "highlightbackground_color":highlightbackground_color,
            "highlightthickness":highlightthickness,
            "selectborderwidth":selectborderwidth,
            "cursor": cursor,
            "background_color": background_color,
            "text_color": text_color,
            "highlightcolor": highlightcolor,
            "relief": relief,
            "takefocus": takefocus,
            "text_color_disabled": text_color_disabled,
            "width": width,
            "height": height,
            "background_color_selected":background_color_selected,
            "text_color_selected":text_color_selected,
            "selectmode":selectmode,
            # "text": text,
        }

        if default_event:
            self.bind_event("<<ListboxSelect>>",key=key,key_function=key_function)

        self.update(**_tk_kwargs)

    def _personal_init_inherit(self):
        self._set_tk_target_variable(tk.StringVar, kwargs_key="listvariable", default_key="default_list")

        # if self._default_event:
        #     self._tk_kwargs["command"] = self.window.get_event_function(self, key=self.key,
        #                                                                 key_function=self._key_function, )

    list_elements:tuple

    @property
    def list_elements(self) -> tuple:
        """
        Elements this listbox contains
        :return:
        """
        return tuple(self._list_elements)

    @list_elements.setter
    def list_elements(self,new_val:Iterable):
        self._list_elements = list(new_val)
        super().set_value(new_val)

    @property
    def index(self) -> int | None:
        """
        Returnes the index of the selected row
        :return:
        """
        index = self.tk_widget.curselection()
        if index:
            return index[0]
        return None

    @index.setter
    def index(self, new_val:int):
        """
        Select a specified row
        :return:
        """
        self.tk_widget.selection_set(new_val)

    def get_index(self,default:int = -1) -> int:
        """
        Returns the index.
        If nothing is selected, returns default
        :return:
        """
        index = self.index
        if index is None:
            return default

        return index

    def _get_value(self) -> str:
        """
        Returns the selection.
        :return:
        """
        index = self.index
        if index:
            return self._list_elements[index]

        return ""

    def set_value(self, val: str | int):
        """
        Select a certain row.

        :param val: Either the index, or whatever element you want to select
        :return:
        """
        if val in self._list_elements:
            self.tk_widget.selection_set(self._list_elements.index(val))

    def _update_font(self):
        # self._tk_kwargs will be passed to tk_widget later
        self._tk_kwargs["font"] = font.Font(
            self.window.parent_tk_widget,
            family=self._fonttype,
            size=self._fontsize,
            weight="bold" if self._bold else "normal",
            slant="italic" if self._italic else "roman",
            underline=bool(self._underline),
            overstrike=bool(self._overstrike),
        )

    def _update_special_key(self, key: str, new_val: any) -> bool | None:
        # Fish out all special keys to process them seperately
        match key:
            case "fonttype":
                self._fonttype = self.defaults.single(key, new_val)
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "fontsize":
                self._fontsize = self.defaults.single(key, new_val)
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "font_bold":
                self._bold = self.defaults.single(key, new_val)
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "font_italic":
                self._italic = self.defaults.single(key, new_val)
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "font_underline":
                self._underline = self.defaults.single(key, new_val)
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "font_overstrike":
                self._overstrike = self.defaults.single(key, new_val)
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "disabled":
                self._tk_kwargs["state"] = "disabled" if new_val else "normal"
            case "selectmode":
                assert not new_val or new_val in ["single","browse"], "Invalid value for 'selectmode' in some Listbox element. Multi-Selection is not possible for normal Listboxe. Use ListboxMulti instead, if the class exists by now..."
                return False # Still handle this normally please
            case _:  # Not a match
                return False

        return True

    def _apply_update(self):
        # If the font changed, apply them to self._tk_kwargs
        if self.has_flag(ElementFlag.UPDATE_FONT):
            self._update_font()

        super()._apply_update()  # Actually apply the update

    def append(self,*element:str):
        """
        Append a single element
        :param element:
        :return:
        """
        self.tk_widget.insert(tk.END,*element)
        self._list_elements.extend(element)

    def append_front(self,*element:str):
        """
        Append to the beginning
        :param element:
        :return:
        """
        self.tk_widget.insert(0,*element)
        self._list_elements = list(element) + self._list_elements

    def delete_index(self,*index:int):
        """
        Delete some indexes from the list
        :param index:
        :return:
        """
        index = sorted(index,reverse=True)
        for i in index:
            self.tk_widget.delete(i)
            del self._list_elements[i]

    # Todo: Do that with del x[...]. Also for the setter and getter.
    def delete_element(self,*element:str):
        """
        Delete certain element(s) by their value
        :param element:
        :return:
        """
        element = self.get_all_indexes_of(*element)
        self.delete_index(*element)

    def index_of(self,value:str,default:int = None) -> int|None:
        """
        Returns the first index of a given string
        :param default: Returned if it doesn't contain the value
        :param value:
        :return:
        """
        if value in self._list_elements:
            return self._list_elements.index(value)

        return default

    def get_all_indexes_of(self,*value:str) -> tuple[int, ...]:
        """
        Returns all indexes of the passed value(s)
        :param value: Content of the searched row
        :return:
        """
        return tuple(n for n,v in enumerate(self._list_elements) if v in value)

    def color_row(
            self,
            row: int | str,
            background_color: Color | str = None,
            text_color: Color | str = None,
            background_color_selected: Color | str = None,
            text_color_selected: Color | str = None
    ) -> Self:
        """
        Change colors on a single row
        :param row:
        :param background_color:
        :param text_color:
        :param background_color_selected:
        :param text_color_selected:
        :return: The instance itself, so it can be called inline
        """
        self.color_rows(
            (row,),
            background_color=background_color,
            text_color=text_color,
            background_color_selected=background_color_selected,
            text_color_selected=text_color_selected
        )

        return self

    def color_rows(
            self,
            rows:Iterable[int|str],
            background_color:Color | str = None,
            text_color:Color | str = None,
            background_color_selected: Color|str = None,
            text_color_selected: Color|str = None
    ) -> Self:
        """
        Change colors on certain rows
        :param rows:
        :param background_color:
        :param text_color:
        :param background_color_selected:
        :param text_color_selected:
        :return: The instance itself, so it can be called inline
        """
        rows = set(rows)
        rows_str = set(filter(lambda a:isinstance(a,str),rows))  # Get all rows passed as a string
        rows = rows - rows_str  # Remove those strings
        rows_str = self.get_all_indexes_of(*rows_str)
        rows.update(rows_str)   # Add those indexes

        try:
            for i in rows:
                self.tk_widget.itemconfig(
                    i,
                    background=background_color,
                    foreground=text_color,
                    selectbackground=background_color_selected,
                    selectforeground=text_color_selected
                )
        except AttributeError:
            raise SyntaxError(f"You cannot change row-colors before creating the window. You probably tried to on some Listbox-element.")

        return self


    # def extend(self,elements:Iterable[str]):
    #     """
    #     Extend by a list instead of single elements
    #     :param elements:
    #     :return:
    #     """
    #     self.append(*elements)


