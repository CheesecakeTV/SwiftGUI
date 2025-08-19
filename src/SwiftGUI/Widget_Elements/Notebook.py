import tkinter.ttk as ttk
from collections.abc import Iterable, Callable
from typing import Any, Self

from SwiftGUI import ElementFlag, GlobalOptions, Literals, Color, BaseWidgetTTK, BaseElement, Frame, Font
from SwiftGUI.Widget_Elements.Spacer import Spacer


class Notebook(BaseWidgetTTK):
    tk_widget:ttk.Notebook
    _tk_widget:ttk.Notebook
    _tk_widget_class:type = ttk.Notebook # Class of the connected widget
    defaults = GlobalOptions.Notebook

    _styletype:str = "TNotebook"

    # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/ttk-Notebook.html
    def __init__(
            self,
            # Add here
            *tabs: Frame,

            default_event: bool = None,

            tab_texts: dict[Any, str] = None,

            key: str = None,
            key_function: Callable | Iterable[Callable] = None,

            background_color: str | Color = None,
            background_color_tabs: str | Color = None,
            background_color_tabs_active: str | Color = None,

            text_color_tabs: str | Color = None,
            text_color_tabs_active: str | Color = None,

            fonttype_tabs: str | Font = None,
            fontsize_tabs: int = None,
            font_bold_tabs: bool = None,
            font_italic_tabs: bool = None,
            font_underline_tabs: bool = None,
            font_overstrike_tabs: bool = None,

            apply_parent_background_color: bool = None,

            padding: int | tuple[int,...] = None,
            takefocus: bool = None,

            borderwidth: int = None,

            width: int = None,
            height: int = None,

            cursor: Literals.cursor = None,

            tabposition: Literals.tabposition = None,

            expand: bool = None,
            expand_y: bool = None,
            tk_kwargs: dict[str:Any]=None
    ):
        super().__init__(key=key,tk_kwargs=tk_kwargs,expand=expand, expand_y = expand_y)
        self._key_function = key_function

        self.add_flags(ElementFlag.IS_CONTAINER)    # So .init_containing is called
        self.add_flags(ElementFlag.APPLY_PARENT_BACKGROUND_COLOR)

        self._elements: tuple[Frame, ...] = tabs
        self._element_keys: tuple[Any, ...] = tuple(map(lambda a:a.key, tabs))

        self._tab_event_functions: list[Callable | None] = [None] * len(self._elements) # The functions that will be called when the corresponding tab is selected

        if background_color and not apply_parent_background_color:
            apply_parent_background_color = False

        if tk_kwargs is None:
            tk_kwargs = dict()

        self._tab_texts = tab_texts

        self._fonttype_tabs = None
        self._fontsize_tabs = None
        self._bold_tabs = None
        self._italic_tabs = None
        self._underline_tabs = None
        self._overstrike_tabs = None
        
        self.update(
            **tk_kwargs,
            #tab_texts = tab_texts,
            padding = padding,
            takefocus = takefocus,
            width = width,
            height = height,
            cursor = cursor,
            apply_parent_background_color = apply_parent_background_color,
            borderwidth = borderwidth,
            background_color = background_color,

            background_color_tabs = background_color_tabs,
            background_color_tabs_active = background_color_tabs_active,
            text_color_tabs = text_color_tabs,
            text_color_tabs_active = text_color_tabs_active,

            tabposition = tabposition,

            fonttype_tabs = fonttype_tabs,
            fontsize_tabs = fontsize_tabs,
            font_bold_tabs = font_bold_tabs,
            font_italic_tabs = font_italic_tabs,
            font_underline_tabs = font_underline_tabs,
            font_overstrike_tabs = font_overstrike_tabs,
        )


        self._default_event = default_event

        # Todo: These could be parameters too
        self._config_ttk_style(tabmargins = 0)


    def _update_font(self):

        # And now for the headings
        font_options = [
            self._fonttype_tabs,
            self._fontsize_tabs,
        ]

        if self._bold_tabs:
            font_options.append("bold")

        if self._italic_tabs:
            font_options.append("italic")

        if self._underline_tabs:
            font_options.append("underline")

        if self._overstrike_tabs:
            font_options.append("overstrike")

        self._config_ttk_style("Tab",font=font_options)

    _tab_texts: dict[Any, str]
    def _update_special_key(self,key:str,new_val:Any) -> bool|None:
        match key:
            case "tabposition":
                self._config_ttk_style(tabposition=new_val)
            case "apply_parent_background_color":
                if new_val:
                    self.add_flags(ElementFlag.APPLY_PARENT_BACKGROUND_COLOR)
                else:
                    self.remove_flags(ElementFlag.APPLY_PARENT_BACKGROUND_COLOR)
            case "tab_texts":
                self._tab_texts.update(new_val)
            case "background_color":
                self._config_ttk_style(background=new_val)
                #self._config_ttk_style(background=new_val, style_ext = "Tab")

                for tab in self._elements:
                    if tab.has_flag(ElementFlag.APPLY_PARENT_BACKGROUND_COLOR):
                        tab.update(background_color = new_val)

            case "background_color_tabs":
                self._map_ttk_style("Tab", background = [("!selected", new_val)])
            case "background_color_tabs_active":
                self._map_ttk_style("Tab", background = [("selected", new_val)])

            case "text_color_tabs":
                self._map_ttk_style("Tab", foreground=[("!selected", new_val)])
            case "text_color_tabs_active":
                self._map_ttk_style("Tab", foreground=[("selected", new_val)])

            case "fonttype_tabs":
                self._fonttype_tabs = self.defaults.single("fonttype", self.defaults.single(key,new_val))
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "fontsize_tabs":
                self._fontsize_tabs = self.defaults.single("fontsize", self.defaults.single(key,new_val))
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "font_bold_tabs":
                self._bold_tabs = self.defaults.single("font_bold", self.defaults.single(key,new_val))
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "font_italic_tabs":
                self._italic_tabs = self.defaults.single("font_italic", self.defaults.single(key,new_val))
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "font_underline_tabs":
                self._underline_tabs = self.defaults.single("font_underline", self.defaults.single(key,new_val))
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "font_overstrike_tabs":
                self._overstrike_tabs = self.defaults.single("font_overstrike", self.defaults.single(key,new_val))
                self.add_flags(ElementFlag.UPDATE_FONT)
            
            
            case "borderwidth":
                self._config_ttk_style(borderwidth=new_val)
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
        super()._personal_init()

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
            container = Frame(
                [[tab], [the_spacer := Spacer(expand_y=True)]],
                pass_down_background_color=False
            )
            container.link_background_color(the_spacer)
            container._init(self, self.window)

            tab.link_background_color(container)

            key = tab.key
            title = self._tab_texts.get(key, key)   # If the key is not in this dict, just use the key

            self.tk_widget.add(container.tk_widget, text=str(title))

    _default_event_callback_function: Callable = None
    def init_window_creation_done(self):
        """Don't touch!"""
        super().init_window_creation_done()

        self._default_event_callback_function = self.window.get_event_function(self, self.key, key_function=self._key_function)
        self.tk_widget.bind("<<NotebookTabChanged>>", self._tab_change_callback)

    def _tab_change_callback(self, *_):
        """Called when the tab changes"""
        index = self.index
        if self._tab_event_functions[index]:
            self._tab_event_functions[index]()
            return

        if self._default_event_callback_function:
            self._default_event_callback_function()

    @BaseElement._run_after_window_creation
    def bind_event_to_tab(self, tab_key:Any = None, tab_index:int = None, key_extention:str | Any=None, key:Any=None, key_function:Callable|Iterable[Callable]=None) ->Self:
        """
        This event will be called when tab_key-tab is opened.
        Keep in mind, that setting this disables the default event for that tab

        :param tab_index: Pass this to apply the event to the index-ths tab
        :param tab_key: Pass this to apply the event to the tab with this key
        :param key_extention:
        :param key:
        :param key_function:
        :return:
        """

        new_key = ""
        match (key_extention is not None,key is not None):
            case (True,True):
                new_key = key + key_extention
            case (False,True):
                new_key = key
            case (True,False):
                new_key = self.key + key_extention
            case (False,False):
                new_key = self.key
                assert new_key or key_function, f"You forgot to add either a key or key_function to this element... {self}"

        assert bool(tab_key) ^ bool(tab_index), f"You can only pass either tab_key, or tab_index to .bind_event_to_tab on Element {self}"

        if tab_key:
            tab_index = self._element_keys.index(tab_key)

        self._tab_event_functions[tab_index] = self.window.get_event_function(self, new_key, key_function=key_function)

        return self
