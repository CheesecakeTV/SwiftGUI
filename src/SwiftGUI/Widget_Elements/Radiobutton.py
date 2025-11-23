import tkinter as tk
import tkinter.font as font
from collections.abc import Iterable, Callable
from typing import Literal, Any, Hashable
from SwiftGUI.Compat import Self

from SwiftGUI import ElementFlag, BaseWidget, GlobalOptions, Literals, Color

_radio_id:int = 1
_named_radio_groups: dict[Hashable, "RadioGroup"] = dict()  # All groups with an actual name instead of ids

class RadioGroup:
    """
    This is used to identify which radio-buttons belong together.
    """
    _name: Hashable = ""

    def __new__(cls, *args, **kwargs):
        if args:
            kwargs["name"] = args[0]

        name = kwargs.get("name")

        if name in _named_radio_groups:
            return _named_radio_groups[kwargs["name"]]

        global _radio_id

        new_instance = super().__new__(cls)
        new_instance._id = _radio_id
        _radio_id += 1

        if name is not None:
            _named_radio_groups[name] = new_instance

        new_instance.next_radio_value = -1   # Will be passed to the radio-button. If the tk-value is equal to this, radio is checked
        new_instance.tk_variable = tk.IntVar    # Passed to the radio-button

        return new_instance

    def __init__(self, name: Hashable = None):
        """
        Pass a name, if you want to grap an already existing Group.
        :param name:
        """
        tk_variable: type | tk.IntVar

        self._name = name
        self.next_radio_value += 1

    def __str__(self):
        return f"<RadioGroup\t{self._name=}\t{self._id=}>"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return self._id

    def __eq__(self, other):
        return hash(self) == hash(other)

class Radiobutton(BaseWidget):
    _tk_widget_class: type = tk.Radiobutton  # Class of the connected widget
    tk_widget: tk.Radiobutton
    defaults = GlobalOptions.Radiobutton  # Default values (Will be applied to kw_args-dict and passed onto the tk_widget
    value: bool

    _grab_anywhere_on_this = True

    _transfer_keys = {
        "background_color": "background",
        "text_color_disabled": "disabledforeground",
        "highlightbackground_color": "highlightbackground",
        "background_color_active": "activebackground",
        "text_color_active": "activeforeground",
        "text_color": "fg",
        "bitmap_position": "compound",
        "check_background_color": "selectcolor",
    }

    def __init__(
            self,
            text: str = None,
            /,
            group: Hashable | RadioGroup = None,

            key: Hashable = None,
            key_function: Callable | Iterable[Callable] = None,
            default_event: bool = False,

            default_value: bool = False,

            disabled: bool = None,

            background_color: str | Color = None,
            background_color_active: str | Color = None,
            apply_parent_background_color: bool = None,

            text_color: str | Color = None,
            text_color_disabled: str | Color = None,
            text_color_active: str | Color = None,

            borderwidth:int = None,

            bitmap: Literals.bitmap = None,
            bitmap_position: Literals.compound = None,

            check_background_color: str | Color = None,
            check_type: Literals.indicatoron = None,

            width: int = None,
            height: int = None,
            padx: int = None,
            pady: int = None,

            cursor: Literals.cursor = None,
            takefocus: bool = None,

            anchor: Literals.anchor = None,
            justify: Literal["left", "right", "center"] = None,

            relief: Literals.relief = None,
            overrelief: Literals.relief = None,
            offrelief: Literals.relief = None,

            fonttype: str = None,
            fontsize: int = None,
            font_bold: bool = None,
            font_italic: bool = None,
            font_underline: bool = None,
            font_overstrike: bool = None,
            underline: int = None,

            expand: bool = None,
            expand_y: bool = None,
            tk_kwargs: dict = None,
    ):
        super().__init__(key, tk_kwargs=tk_kwargs, expand=expand,expand_y=expand_y)

        self._key_function = key_function

        if tk_kwargs is None:
            tk_kwargs = dict()

        if self.defaults.single("background_color", background_color) and not apply_parent_background_color:
            apply_parent_background_color = False

        self._default_event = default_event

        if group is None:
            self._group = RadioGroup()
        else:
            self._group = RadioGroup(group)

        self._my_value = self._group.next_radio_value

        self._update_initial(variable=self._group.tk_variable, text=text, value=self._my_value, fonttype=fonttype,
                             fontsize=fontsize, font_bold=font_bold, font_italic=font_italic,
                             font_underline=font_underline, font_overstrike=font_overstrike, disabled=disabled,
                             borderwidth=borderwidth, bitmap=bitmap, text_color_disabled=text_color_disabled,
                             check_background_color=check_background_color, bitmap_position=bitmap_position,
                             background_color_active=background_color_active, text_color_active=text_color_active,
                             check_type=check_type, width=width, height=height, padx=padx, pady=pady, cursor=cursor,
                             takefocus=takefocus, underline=underline, anchor=anchor, justify=justify,
                             background_color=background_color,
                             apply_parent_background_color=apply_parent_background_color, overrelief=overrelief,
                             offrelief=offrelief, text_color=text_color, relief=relief, highlightthickness=0, **tk_kwargs)

        if default_value:
            self.select()

    def _personal_init_inherit(self):
        if not isinstance(self._group.tk_variable, tk.IntVar):
            self._group.tk_variable = self._group.tk_variable()

        self._assign_tk_target_variable(self._group.tk_variable, kwargs_key="variable")

        if self._default_event:
            self._tk_kwargs["command"] = self.window.get_event_function(self, key=self.key, key_function=self._key_function)

    def _get_value(self) -> bool:
        return self._group.tk_variable.get() == self._my_value  # Don't like it, but I need to ignore this warning...

    def set_value(self, val: bool):
        if val:
            self.select()
        else:
            self.deselect()

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

    def _update_special_key(self, key: str, new_val: Any) -> bool | None:
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
            case "check_type":
                self._tk_kwargs["indicatoron"] = int(new_val == "check")
            case "apply_parent_background_color":
                if new_val:
                    self.add_flags(ElementFlag.APPLY_PARENT_BACKGROUND_COLOR)
                else:
                    self.remove_flags(ElementFlag.APPLY_PARENT_BACKGROUND_COLOR)
            case _:  # Not a match
                return super()._update_special_key(key, new_val)

        return True

    def _apply_update(self):
        # If the font changed, apply them to self._tk_kwargs
        if self.has_flag(ElementFlag.UPDATE_FONT):
            self.remove_flags(ElementFlag.UPDATE_FONT)
            self._update_font()

        super()._apply_update()  # Actually apply the update

    @BaseWidget._run_after_window_creation
    def select(self) -> Self:
        """
        Select the button
        :return:
        """
        self.tk_widget.select()
        return self

    @BaseWidget._run_after_window_creation
    def deselect(self) -> Self:
        """
        Deselect the button
        :return:
        """
        self.tk_widget.deselect()
        return self

    def flash(self):
        """
        Flash the Element a couple of times
        :return:
        """
        self.tk_widget.flash()
