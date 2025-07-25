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

@deprecated("WIP, doesn't work yet!")
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
            elements: dict = None,
            /,
            key: Any = None,
            key_function: Callable|Iterable[Callable] = None,
            default_event: bool = False,

            headings: Iterable[str] = ("Forgot to add headings?",),

            expand: bool = None,
            tk_kwargs: dict[str:any]=None
    ):
        super().__init__(key=key,tk_kwargs=tk_kwargs,expand=expand)

        if elements is None:
            elements = dict()
        self._element_tree = DictBidirect(elements)

        self._headings = tuple(headings)

        if tk_kwargs is None:
            tk_kwargs = dict()

        self.update(
            columns = self._headings[1:],
            **tk_kwargs
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

    def _get_value(self) -> any:
        ...

    def set_value(self,val:any):
        ...

    def init_window_creation_done(self):
        """Don't touch!"""
        super().init_window_creation_done()

        if self._headings:
            headings = iter(self._headings)
            self.tk_widget.heading("#0",text=next(headings))

            for h in headings:  # Deploy the remaining ones
                self.tk_widget.heading(h,text=h)

        # print(self.tk_widget.insert("","end",values=("Hallo","Welt")))
        # print(self.tk_widget.insert("I001","end",values=("Hallo","Welt")))

        # self.tk_widget["show"] = "headings"   # Removes first column

        # self.insert((
        #     ("Hallo", "Welt"),
        # ), name="Me!")
        # self.insert((
        #     ("Hi", "Wel-d"),
        # ), name="Another", parent="Me!")

        self.insert({
            "Hallo":{
                "":("Das","Funktioniert","Endlich :C"),
                "Nächste Ebene":("Hellow",),
                "Noch ein Eintrag":("Jaa",)
            }
        },name="Test!")
        print(self._element_tree)


    def _insert_single(self,element: tuple[str] | Any, name: str = None, parent: tuple[str] = None):
        """

        :param element:
        :param name:
        :param parent:
        :return:
        """
        if parent:
            parent_obj = self._element_tree[parent]
        else:
            parent_obj = ""

        elem_path = parent + (name,)

        self._element_tree[elem_path] = self.tk_widget.insert(parent_obj, text=name, index="end", values=element, open=True)

    def insert(self,elements: dict|Iterable[Iterable[str]], name: str = None, parent: str|tuple[str|tuple,...] = tuple()):
        """
        Insert a new element into the tree
        :param name: First column
        :param elements: Row or sub-tree
        :param parent: Element-key where to add this. Separate "folders" using dots.
        :return:
        """
        if isinstance(parent,str):
            parent = (parent,)

        if not elements:
            return

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

                self._insert_single(values,name,parent)

                for key,val in elem.items():
                    if not key:
                        continue
                    self.insert(val, name = key, parent = parent + (name,))

                continue    # Skip tuple insertion

            elem = tuple(elem)

            if not elem:
                continue

            if name is None:
                name = str(counter)
                counter += 1

            self._insert_single(elem, name=name, parent=parent)


