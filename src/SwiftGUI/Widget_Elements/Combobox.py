from tkinter import ttk, font
from typing import Any, Iterable, Callable

from SwiftGUI.Base import run_after_window_creation
from SwiftGUI.Compat import Self

from SwiftGUI import GlobalOptions, BaseWidgetTTK, Literals, Color, ElementFlag, Scrollbar

class Combobox(BaseWidgetTTK):
    tk_widget:ttk.Combobox
    _tk_widget:ttk.Combobox
    _tk_widget_class:type = ttk.Combobox # Class of the connected widget
    defaults = GlobalOptions.Combobox

    _styletype:str = "TCombobox"

    # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/ttk-Notebook.html
    def __init__(
            self,
            choices: Iterable[Any] = tuple(),
            /,
            key: Any = None,
            key_function: Callable | Iterable[Callable] = None,
            default_event: bool = None,

            default_value: str = None,

            cursor: Literals.cursor = None,
            insertbackground: str | Color = None,

            background_color: str | Color = None,
            background_color_disabled: str | Color = None,
            selectbackground_color: str | Color = None,

            text_color: str | Color = None,
            text_color_disabled: str | Color = None,
            select_text_color: str | Color = None,

            fonttype: str = None,
            fontsize: int = None,
            font_bold: bool = None,
            font_italic: bool = None,
            font_underline: bool = None,
            font_overstrike: bool = None,

            button_background_color= None,
            button_background_color_active= None,

            arrow_color= None,
            arrow_color_active= None,

            disabled: bool = None,
            can_change_text: bool = None,

            exportselection: bool = None,

            # Todo: validate,
            #  validatecommand,

            height: int = None,
            width: int = None,

            justify: Literals.left_center_right = None,

            takefocus: bool = None,

            # Add here
            expand: bool = None,
            expand_y: bool = None,
            tk_kwargs: dict[str:Any]=None
    ):
        super().__init__(key=key,tk_kwargs=tk_kwargs,expand=expand, expand_y = expand_y)

        choices = tuple(choices)
        if default_value is None and choices:
            default_value = choices[0]

        self._key_function = key_function

        self._default_event = default_event
        self._event_function = lambda *_:None   # Placeholder

        self._prev_value = default_value

        # Not a real element, just using it for the ttk-theme!
        # This is not the scrollbar shown in the combobox.
        self.scrollbar: Scrollbar = Scrollbar()

        self._update_initial(
            default_value = default_value,
            choices = choices,
            cursor = cursor,
            exportselection = exportselection,
            height = height,
            width = width,
            justify = justify,
            takefocus = takefocus,
            disabled = disabled,
            can_change_text = can_change_text,
            background_color = background_color,
            background_color_disabled = background_color_disabled,
            selectbackground_color = selectbackground_color,
            text_color = text_color,
            text_color_disabled = text_color_disabled,
            select_text_color = select_text_color,
            button_background_color = button_background_color,
            button_background_color_active= button_background_color_active,
            arrow_color = arrow_color,
            arrow_color_active= arrow_color_active,

            fonttype=fonttype,
            fontsize=fontsize,
            font_bold=font_bold,
            font_italic=font_italic,
            font_underline=font_underline,
            font_overstrike=font_overstrike,

            insertbackground = insertbackground,
        )

    @BaseWidgetTTK._run_after_window_creation
    def update_scrollbar_y(
            self,
            cursor: Literals.cursor = None,

            background_color: str | Color = None,
            background_color_active: str | Color = None,

            text_color: str | Color = None,
            text_color_active: str | Color = None,

            troughcolor: str | Color = None,
    ) -> Self:
        self.scrollbar.update(
            cursor = cursor,
            background_color = background_color,
            background_color_active = background_color_active,
            text_color = text_color,
            text_color_active = text_color_active,
            troughcolor = troughcolor,
        )
        return self

    def _update_special_key(self,key:str,new_val:Any) -> bool|None:
        if not self.window and key in ["background_color", "text_color", "selectbackground_color", "select_text_color"]:    # These can only be handled once the element exists
            self.update_after_window_creation(**{key: new_val})
            return True

        match key:
            case "choices":
                if new_val:
                    self._tk_kwargs["values"] = tuple(map(str, new_val))
                else:
                    self._tk_kwargs["values"] = tuple()

            case "insertbackground":
                self._config_ttk_style(insertcolor=new_val)

            case "arrow_color":
                self._map_ttk_style(arrowcolor=(("!pressed", new_val), ))
            case "arrow_color_active":
                self._map_ttk_style(arrowcolor=(("pressed", new_val), ))

            case "button_background_color":
                self._map_ttk_style(background=(("!pressed", new_val), ))
            case "button_background_color_active":
                self._map_ttk_style(background=(("pressed", new_val), ))

            case "background_color":
                if new_val is None:
                    return
                self._map_ttk_style(fieldbackground=(("!disabled", new_val), ))
                self.tk_widget.tk.eval(
                    f"[ttk::combobox::PopdownWindow {self.tk_widget}].f.l configure -background {new_val}")
                #self.window.root.option_add('*TCombobox*Listbox*Background', "red")
            case "background_color_disabled":
                self._map_ttk_style(fieldbackground=(("disabled", new_val), ))

            case "text_color":
                if new_val is None:
                    return
                self._map_ttk_style(foreground=(("!disabled", new_val),))
                self.tk_widget.tk.eval(
                    f"[ttk::combobox::PopdownWindow {self.tk_widget}].f.l configure -foreground {new_val}")
            case "text_color_disabled":
                self._map_ttk_style(foreground=(("disabled", new_val),))

            case "selectbackground_color":
                if new_val is None:
                    return
                self._config_ttk_style(selectbackground= new_val)
                self.tk_widget.tk.eval(
                    f"[ttk::combobox::PopdownWindow {self.tk_widget}].f.l configure -selectbackground {new_val}")
            case "select_text_color":
                if new_val is None:
                    return
                self._config_ttk_style(selectforeground= new_val)
                self.tk_widget.tk.eval(
                    f"[ttk::combobox::PopdownWindow {self.tk_widget}].f.l configure -selectforeground {new_val}")

            case "default_event":
                self._default_event = new_val

            case "fonttype":
                self._fonttype = self.defaults.single(key,new_val)
                self.add_flags(ElementFlag.UPDATE_FONT)
            case "fontsize":
                self._fontsize = self.defaults.single(key,new_val)
                self.add_flags(ElementFlag.UPDATE_FONT)
                self._config_ttk_style(arrowsize= new_val)
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

            case "disabled":
                if not self.window:
                    self.update_after_window_creation(disabled = new_val)
                    return True
                self.tk_widget.state(["disabled" if new_val else "!disabled"])

            case "can_change_text":
                if not self.window:
                    self.update_after_window_creation(can_change_text=new_val)
                    return True
                self.tk_widget.state(["!readonly" if new_val else "readonly"])

            case _:
                return super()._update_special_key(key, new_val)

        return True

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

        self.tk_widget.tk.eval(f"[ttk::combobox::PopdownWindow {self.tk_widget}].f.l configure -font {self._tk_kwargs['font']}")

    def _apply_update(self):
        # If the font changed, apply them to self._tk_kwargs
        if self.has_flag(ElementFlag.UPDATE_FONT):
            self._update_font()
            self.remove_flags(ElementFlag.UPDATE_FONT)

        super()._apply_update() # Actually apply the update

    _prev_value: str    # Value of last callback
    def _value_change_callback(self, *_):
        if self.value == self._prev_value:
            return

        self._prev_value = self.value

        if self._default_event:
            self._event_function()

    def set_value(self,val:Any):
        self._prev_value = val  # So no event gets called
        super().set_value(val)

    def _personal_init_inherit(self):
        self._event_function = self.window.get_event_function(self, self.key, self._key_function)
        self._set_tk_target_variable(default_key="default_value", kwargs_key= "textvariable")
        self._tk_target_value.trace_add("write", self._value_change_callback)

    def init_window_creation_done(self):
        super().init_window_creation_done()

        # Fake-initialize this widget
        self.scrollbar.window = self.window
        self.scrollbar.init_window_creation_done()
        frame_path = f"[ttk::combobox::PopdownWindow {self.tk_widget}].f"
        self.tk_widget.tk.eval(f"{frame_path}.sb configure -style {self.scrollbar.ttk_style}")

        # So not everything gets selected when chosing something from the drop-down
        self.tk_widget.bind("<<ComboboxSelected>>", lambda *_:self.tk_widget.selection_clear())

        # print(self.tk_widget.tk.eval(f"{frame_path}.sb configure -style {style}"))

        # root_style: ttk.Style = self.window.ttk_style
        # root_style.configure(style, background="red")

    @property
    def choices(self) -> tuple[str]:
        """
        Elements in the drop-down-menu
        :return:
        """
        return self.get_option("choices", tuple())

    @choices.setter
    def choices(self, new_val: Iterable[str]):
        """

        :param new_val:
        :return:
        """
        self.set_choices(new_val)

    @run_after_window_creation
    def set_choices(self, new_val: Iterable[str]) -> Self:
        """
        Change the elements in the drop-down-menu

        :param new_val:
        :return:
        """
        self.update(choices=new_val)
        return self
