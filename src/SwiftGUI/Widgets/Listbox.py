import tkinter as tk
import tkinter.font as font
from collections.abc import Iterable, Callable
from typing import Union

from SwiftGUI import ElementFlag, BaseWidget, GlobalOptions, Literals, Color


class Listbox(BaseWidget):
    _tk_widget_class: type = tk.Listbox  # Class of the connected widget
    tk_widget: tk.Listbox
    defaults = GlobalOptions.Listbox  # Default values (Will be applied to kw_args-dict and passed onto the tk_widget
    value: list

    _transfer_keys = {
        # "background_color_disabled": "disabledbackground",
        "background_color": "background",
        "text_color_disabled": "disabledforeground",
        "highlightbackground_color": "highlightbackground",
        # "selectbackground_color": "selectbackground",
        # "select_text_color": "selectforeground",
        # "pass_char":"show",
        "background_color_active": "activebackground",
        "text_color_active": "activeforeground",
        "text_color": "fg",
        "bitmap_position": "compound",
        "check_background_color": "selectcolor",
    }

    def __init__(
            self,
            default_list: Iterable[str] = None,
            key: any = None,
            default_event: bool = False,
            key_function: Callable | Iterable[Callable] = None,
            activestyle: Literals.activestyle = None,
            # fonttype: str = None,
            # fontsize: int = None,
            # font_bold: bool = None,
            # font_italic: bool = None,
            # font_underline: bool = None,
            # font_overstrike: bool = None,
            # readonly: bool = None,
            # # borderwidth:int = None,
            # #
            # bitmap: Literals.bitmap = None,
            # text_color_disabled: str | Color = None,
            # check_background_color: str | Color = None,
            # bitmap_position: Literals.compound = None,
            # background_color_active: str | Color = None,
            # text_color_active: str | Color = None,
            # check_type: Literals.indicatoron = None,
            # #
            # width: int = None,
            # height: int = None,
            # padx: int = None,
            # pady: int = None,
            # #
            # cursor: Literals.cursor = None,
            # takefocus: bool = None,
            # #
            # underline: int = None,
            # anchor: Literals.anchor = None,
            # justify: Literal["left", "right", "center"] = None,
            # background_color: str | Color = None,
            # overrelief: Literals.relief = None,
            # offrelief: Literals.relief = None,
            # text_color: str | Color = None,
            # relief: Literals.relief = None,
            # hilightbackground_color: str | Color = None,
            # highlightcolor: str | Color = None,
            tk_kwargs: dict = None,
    ):
        super().__init__(key, tk_kwargs=tk_kwargs)

        self._key_function = key_function
        self._list_elements = list(default_list)

        if tk_kwargs is None:
            tk_kwargs = dict()

        _tk_kwargs = {
            **tk_kwargs,
            "default_list": default_list,
            "width":100,
            "activestyle":activestyle,
            # "selectmode":tk.MULTIPLE, # Todo: Selectmode
            # "font_bold": font_bold,
            # "font_italic": font_italic,
            # "font_overstrike": font_overstrike,
            # "font_underline": font_underline,
            # "fontsize": fontsize,
            # "fonttype": fonttype,
            # "readonly": readonly,
            # "bitmap_position": bitmap_position,
            # "bitmap": bitmap,
            # "check_background_color": check_background_color,
            #
            # "check_type": check_type,
            # "cursor": cursor,
            # "underline": underline,
            # "justify": justify,
            # "background_color": background_color,
            # "highlightthickness": 5,
            # "highlightcolor": "purple",
            # "relief": relief,
            # "text_color": text_color,
            # "width": width,
            # "anchor": anchor,
            # "overrelief": overrelief,
            # "offrelief": offrelief,
            # "takefocus": takefocus,
            # "text_color_disabled": text_color_disabled,
            # "background_color_active": background_color_active,
            # "text_color_active": text_color_active,
            #
            # "height": height,
            # "padx": padx,
            # "pady": pady,
            # "text": text,
        }

        self._default_event = default_event

        # self.bind_event("<KeyRelease>",key=self.key,key_function=self._key_function)

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
            case "readonly":
                self._tk_kwargs["state"] = "disabled" if new_val else "normal"
            case _:  # Not a match
                return False

        return True

    def _apply_update(self):
        # If the font changed, apply them to self._tk_kwargs
        if self.has_flag(ElementFlag.UPDATE_FONT):
            self._update_font()

        super()._apply_update()  # Actually apply the update

    def append(self,element:str):
        """
        Append a single
        :param element:
        :return:
        """