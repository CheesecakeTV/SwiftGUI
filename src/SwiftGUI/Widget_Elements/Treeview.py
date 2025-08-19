import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as font
from collections.abc import Iterable, Callable
from typing import Literal, Any
from warnings import deprecated

from SwiftGUI import ElementFlag, BaseWidget, GlobalOptions, Literals, Color

class DictBidirect(dict):
    """
    Pretty class to have a dictionary and also an inverse one with much less CPU usage.
    Might get moved to a different file if I need this class for another issue.
    """
    rev:dict

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.rev = dict()

        for key,val in self.items():
            self.rev[val] = key

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.rev[value] = key

    def __delitem__(self, key):
        del self.rev[self[key]]
        super().__delitem__(key)

@deprecated("WIP, Treeview does work, but still a long way to go. Probably shouldn't use it atm...")
class Treeview(BaseWidget):
    tk_widget:ttk.Treeview
    _tk_widget:ttk.Treeview
    _tk_widget_class:type = ttk.Treeview # Class of the connected widget
    defaults = GlobalOptions.Treeview

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

    _element_tree: dict[str:[dict|Iterable[str]]]
    _headings: tuple

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
            expand_y: bool = None,
            tk_kwargs: dict[str:any]=None
    ):
        super().__init__(key=key,tk_kwargs=tk_kwargs,expand=expand)

        # if elements is None:
        #     elements = dict()
        self._element_tree = DictBidirect()

        self._headings = tuple(headings)
        self._headings_len = len(self._headings)

        if tk_kwargs is None:
            tk_kwargs = dict()

        self.update(
            columns = self._headings,
            **tk_kwargs,
            selectmode= "browse",
        )

        # if default_event:
        #     self.bind_event("<KeyRelease>",key=key,key_function=key_function)

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
            case "can_reset_value_changes":
                self.can_reset_value_changes = new_val
            case _:
                return False

        return True

    def _apply_update(self):
        # If the font changed, apply them to self._tk_kwargs
        if self.has_flag(ElementFlag.UPDATE_FONT):
            self._update_font()
            self.remove_flags(ElementFlag.UPDATE_FONT)

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

    def get_full_selection(self) -> dict | None:
        """
        Return the full selection-dict
        :return:
        """
        temp = self.selection
        if not temp:
            return None

        return self.tk_widget.item(self._element_tree[temp])

    def _get_value(self) -> tuple[str,...]:
        temp = self.get_full_selection()

        if temp is None:
            return ("",) * self._headings_len

        return tuple(temp["values"])

    def set_value(self,val:any):
        print("Warning!","It is not possible to set Values of sg.Treeview (yet)!")

    selection:tuple[str]

    @property
    def selection(self) -> tuple:
        temp = self.tk_widget.focus()
        if temp:
            return self._element_tree.rev[temp]
        return tuple()

    @selection.setter
    def selection(self, new_val):
        if not new_val:
            self.tk_widget.selection_set()
            self.tk_widget.focus("")
            return

        temp = self._element_tree[new_val]
        self.tk_widget.selection_set((temp,))
        self.tk_widget.focus(temp)

    def init_window_creation_done(self):
        """Don't touch!"""
        super().init_window_creation_done()

        if self._headings:
            headings = iter(self._headings)
            #self.tk_widget.heading("#0",text=next(headings))

            for h in headings:  # Deploy the remaining ones
                self.tk_widget.heading(h,text=h)

        # print(self.tk_widget.insert("","end",values=("Hallo","Welt")))
        # print(self.tk_widget.insert("I001","end",values=("Hallo","Welt")))

        # self.tk_widget["show"] = "headings"   # Removes first column

        self.insert((
            ("Hallo", "Welt"),
        ), name="Me!")
        self.insert((
            ("Hi", "Wel-d"),
        ), name="Another", parent="Me!")

        self.insert_subtree({
            "Hallo":{
                "":("Das","Funktioniert","Endlich :C"),
                "Nächste Ebene":("Hellow",),
                "Noch ein Eintrag":("Jaa",)
            }
        },name="Test!")
        print(self._element_tree)


    def insert(self,element: list[str]|tuple[str] | Any, name: str = "", parent: str|tuple[str] = None) -> tuple[str,...]:
        """
        Insert a single element (row) into the treeview.

        :param element: Element-values. Should be a list/tuple of strings that get displayed under the corresponding column
        :param name: Identifier. Gets displayed in the first (0-th) column
        :param parent: Set this to put the element "inside" another element
        :return: path to that element
        """
        if isinstance(parent,str):
            parent = (parent,)

        if parent:
            parent_obj = self._element_tree[parent]
            elem_path = parent + (name,)
        else:
            parent_obj = ""
            elem_path = (name,)

        if len(element) < self._headings_len:
            element += ("",) * (self._headings_len - len(element))

        self._element_tree[elem_path] = self.tk_widget.insert(parent_obj, text=name, index="end", values=element, open=True)
        return elem_path

    def insert_subtree(self,elements: dict|Iterable[Iterable[str]], name: str = None, parent: str|tuple[str|tuple,...] = tuple()) -> None:
        """
        Insert multiple elements or a subtree into the tree.

        You may insert the following as "elements":
        - A single element, like ("first_col", "second_col")
        - Multiple elements, like (("first_col", "second_col"), ("Second_elem1", "Second_elem2")
        - A dict, built like a folder hierarchy. Keys are the "folders", inside may be a different form of elements or another dict.
            - The dict key "" may contain a single of element that sets the values for this folder.

        example:

        elements = {
            "": ("folderinfo_col1", "folderinfo_col2"),
            "Subfolder": (
                ("File inside","Subfolder"),
                ("Another File inside","")
            )
            "Subtree": {
                "Subsubfolder": ("Single file","inside subsubfolder")
            }
        }

        :param name: First column
        :param elements: Row or sub-tree
        :param parent: Element-key where to add this. Separate "folders" using dots.
        :return:
        """
        if isinstance(parent,str):
            parent = (parent,)

        if isinstance(elements, dict):
            elements = (elements,)
        elif isinstance(elements[0], str):
            elements = (elements,)

        counter = 0
        for elem in elements:
            if isinstance(elem,dict):
                # Insert sub-tree
                values = tuple()
                if "" in elem.keys():
                    values = tuple(elem[""])

                self.insert(values,name,parent)

                for key,val in elem.items():
                    if not key:
                        continue
                    self.insert_subtree(val, name = key, parent = parent + (name,))

                continue    # Skip tuple insertion

            elem = tuple(elem)

            if not elem:
                continue

            if name is None:
                name = str(counter)
                counter += 1

            self.insert(elem, name=name, parent=parent)


