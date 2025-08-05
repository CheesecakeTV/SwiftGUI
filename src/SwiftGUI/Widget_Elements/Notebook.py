import tkinter.ttk as ttk
from collections.abc import Iterable, Callable, Iterator
from functools import partial
from tkinter import font
from typing import Any, Self, Union

from SwiftGUI import ElementFlag, GlobalOptions, Literals, Color, BaseWidgetTTK, BaseElement, BaseWidgetContainer, \
    Frame, Event


class Notebook(BaseWidgetTTK):
    tk_widget:ttk.Notebook
    _tk_widget:ttk.Notebook
    _tk_widget_class:type = ttk.Notebook # Class of the connected widget
    #defaults = GlobalOptions.Table

    _styletype:str = "TNotebook"

    # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/ttk-Notebook.html
    def __init__(
            self,
            # Add here
            *tabs: Frame,

            tab_texts: dict[Any, str] = None,

            key: str = None,

            expand: bool = None,
            tk_kwargs: dict[str:any]=None
    ):
        super().__init__(key=key,tk_kwargs=tk_kwargs,expand=expand)

        self.add_flags(ElementFlag.IS_CONTAINER)    # So .init_containing is called

        self._elements: tuple[Frame, ...] = tabs
        self._element_keys: tuple[Any, ...] = tuple(map(lambda a:a.key, tabs))

        if tk_kwargs is None:
            tk_kwargs = dict()

        self._tab_texts = tab_texts

        self.update(
            **tk_kwargs,
            #tab_texts = tab_texts,
        )

        # if default_event:
        #     self.bind_event("<<TreeviewSelect>>",key=key,key_function=key_function)

    _tab_texts: dict[Any, str]
    def _update_special_key(self,key:str,new_val:any) -> bool|None:
        match key:
            case "tab_texts":
                self._tab_texts.update(new_val)
            case _:
                return False

        return True

    def _apply_update(self):
        # If the font changed, apply them to self._tk_kwargs
        # if self.has_flag(ElementFlag.UPDATE_FONT):
        #     self._update_font()

        super()._apply_update() # Actually apply the update

    def _personal_init(self):
        super()._personal_init()

    _font_size_multiplier: int = 1  # Size of a single character in pixels
    _font_size_multiplier_applied: int = 1  # Applied value so to catch changes
    def _update_font(self):
        ...
        # font_options = [
        #     self._fonttype,
        #     self._fontsize,
        # ]
        #
        # if self._bold:
        #     font_options.append("bold")
        #
        # if self._italic:
        #     font_options.append("italic")
        #
        # if self._underline:
        #     font_options.append("underline")
        #
        # if self._overstrike:
        #     font_options.append("overstrike")
        #
        # self._config_ttk_style(font=font_options)
        #
        # self._font_size_multiplier = font.Font(
        #     self.window.parent_tk_widget,
        #     family=self._fonttype,
        #     size=self._fontsize,
        #     weight="bold" if self._bold else "normal",
        #     slant="italic" if self._italic else "roman",
        #     underline=bool(self._underline),
        #     overstrike=bool(self._overstrike),
        # ).measure("X_") // 2
        # if self._col_width_requested and self._font_size_multiplier != self._font_size_multiplier_applied:
        #     self._font_size_multiplier_applied = self._font_size_multiplier
        #     self.update(column_width=self._col_width_requested)
        #
        # # And now for the headings
        # font_options = [
        #     self._fonttype_headings if self._fontsize_headings else self._fonttype,
        #     self._fontsize_headings if self._fontsize_headings else self._fontsize,
        # ]
        #
        # if self._bold_headings:
        #     font_options.append("bold")
        #
        # if self._italic_headings:
        #     font_options.append("italic")
        #
        # if self._underline_headings:
        #     font_options.append("underline")
        #
        # if self._overstrike_headings:
        #     font_options.append("overstrike")
        #
        # self._config_ttk_style("Heading",font=font_options)

    @property
    def index(self) -> int: # index of current tab
        return self.tk_widget.index("current")

    @index.setter
    def index(self, index: int):
        self.set_index(index)

    @BaseElement._run_after_window_creation
    def set_index(self, index: int):
        """
        Changes the active tab to a certain index.

        Same as .index = ...

        :param index:
        :return:
        """
        self.tk_widget.select(index)

    def _get_value(self) -> Any | None: # Key of current tab
        return self._element_keys[self.tk_widget.index("current")]

    @BaseElement._run_after_window_creation
    def set_value(self,val: Any):
        assert val in self._element_keys, "You tried to set the value of a Notebook (Tabview) to a key that doesn't exist. If you want to set an index, use .index instead"
        val = self._element_keys.index(val)
        self.tk_widget.select(val)

    def _init_containing(self):
        for tab in self._elements:
            tab._init(self, self.window)

            key = tab.key
            title = self._tab_texts.get(key, key)   # If the key is not in this dict, just use the key

            self.tk_widget.add(tab.tk_widget, text=str(title))

    def init_window_creation_done(self):
        """Don't touch!"""
        super().init_window_creation_done()

        self.tk_widget.bind("<<NotebookTabChanged>>", self._tab_change_callback)

    def _tab_change_callback(self, *_):
        """Called when the tab changes"""
        ...

    @BaseElement._run_after_window_creation
    def bind_event_to_tab(self, tab_key:str, key_extention:Union[str,any]=None, key:any=None, key_function:Callable|Iterable[Callable]=None) ->Self:
        """
        This event will be called when tab_key-tab is opened
        :param tab_key:
        :param key_extention:
        :param key:
        :param key_function:
        :return:
        """
        ...
