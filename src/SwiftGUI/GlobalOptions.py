#import tkinter as tk    # Not needed, but helpful to figure out default vals
#from tkinter import ttk
from collections.abc import Iterable
from os import PathLike
from typing import Literal, Union, Any, Callable

from SwiftGUI import Literals, Color, font_windows, Font, Extras
from SwiftGUI.Utilities.Images import file_from_b64
import SwiftGUI as sg

# Every option-class will be stored in here
all_option_classes:list[Union["_DefaultOptionsMeta",type]] = list()

# Those keys aren't an option
_ignore_keys = {"apply","reset_to_default","single","persist_changes","made_changes"}

"""
This code is written with performance as the main focus.
It's not clean, not beautiful, just efficient.
"""

class _DefaultOptionsMeta(type):

    def __new__(mcs, name, bases, namespace):
        _all_defaults = dict(filter(lambda a: a[1] is not None and not a[0].startswith("_") and not a[0] in _ignore_keys, namespace.items()))
        namespace["_all_defaults"] = _all_defaults

        cls:"DEFAULT_OPTIONS_CLASS"|type = super().__new__(mcs, name, bases, namespace)
        #cls._all_defaults = _all_defaults

        all_option_classes.append(cls)

        return cls

    def __setattr__(self, key, value):
        if key[0] == "_":
            super().__setattr__(key, value)
            return

        if value is None:
            # Remove the attribute from this class
            if key in self._provides:
                self._provides.remove(key)
            if key in self._up_to_date:
                self._up_to_date.remove(key)
        else:
            self._values[key] = value
            self._provides.add(key)
            self._up_to_date.add(key)

            if key in self._unavailable:
                self._unavailable.remove(key)

            for cl in self._subscriptions:
                if key in cl._unavailable:
                    cl._unavailable.remove(key)

        for cl in self._subscriptions:
            if key in cl._up_to_date and not key in cl._provides:   # Invalidate this key, if the class itself doesn't provide it too
                cl._up_to_date.remove(key)

    def __delattr__(self, item):
        self.__setattr__(item, None)

        #super().__setattr__(key, value)

    # Todo: __getattribute__ so you can use this like a normal class too

    _subscriptions: set["_DefaultOptionsMeta"]
    def _subscribe(cls, me: "_DefaultOptionsMeta"):
        """
        Subscribed classes will invalidate their value if parent-class value changes

        :param me:
        :return:
        """
        cls._subscriptions.add(me)

    def _update_what_you_need(cls, update_from: "_DefaultOptionsMeta"):
        """
        Update all keys that aren't up to date from "update_from".
        :param update_from: class to take the options from
        :return:
        """
        not_up_to_date = update_from._up_to_date.difference(cls._up_to_date)
        new_values = {key:update_from._values[key] for key in not_up_to_date}
        cls._values.update(new_values)
        cls._up_to_date.update(not_up_to_date)  # These values are now up to date

    _provides: set[str] = set()      # What values this class had defined. Don't overwrite these from superclasses!
    _values: dict[str: Any] = dict() # The actual, saved values
    _up_to_date: set[str] = set()    # What values are refreshed and can be used
    _unavailable: set[str] = set()   # All keys that weren't found before
    def reset_to_default(self):
        """
        Reset all configuration done to any options inside this class
        :return:
        """
        self._provides = set(self._all_defaults.keys())
        self._up_to_date = self._provides.copy()
        self._values = self._all_defaults.copy()
        self._unavailable = set()

    _superclasses: list["_DefaultOptionsMeta"] = list()
    def _fetch(self, keys: set):
        """
        Update the given keys from super-classes, if necessary.

        :param keys:
        :return:
        """
        for cl in self._superclasses:
            if not keys.difference(self._up_to_date):   # Done
                return

            self._update_what_you_need(cl)  # Fetch non-up-to-date values

    def single(self, key: str, val: Any = None, default: Any = None) -> Any:
        """
        val will be returned.
        If val is None, cls.key will be returned.
        If both are None, default will be returned.
        :param default:
        :param key: Name of attribute
        :param val: User-val
        :return:
        """
        if val is not None:
            return val

        if not key in self._up_to_date and not key in self._unavailable:
            self._fetch({key})

        if key in self._up_to_date:
            return self._values.get(key)
        else:
            return default

    def apply(self, apply_to: dict) -> dict:
        """
        Apply default configuration TO EVERY NONE-ELEMENT of apply_to

        :param apply_to: It will be changed AND returned
        :return: apply_to will be changed AND returned
        """
        none_vals = dict(filter(lambda a: a[1] is None, apply_to.items()))  # Get all None-vals

        needed_keys = set(none_vals.keys()).difference(
            self._up_to_date.union(self._unavailable)    # Ignore up_to_date and unavailable keys
        )

        if needed_keys:
            self._fetch(needed_keys)

        none_vals.update({
            key: self._values.get(key) for key in none_vals.keys() if key in self._up_to_date
        })
        apply_to.update(none_vals)

        return apply_to


class DEFAULT_OPTIONS_CLASS(metaclass=_DefaultOptionsMeta):
    """
    Derive from this class to create a "blank" global-options template.

    DON'T ADD ANY OPTIONS HERE!
    """

    def __init_subclass__(cls, **kwargs):
        cls.reset_to_default()

        cls._subscriptions = set()  # All classes deriving this class
        cls._superclasses = cls.__mro__[1:-2]
        for mc in cls._superclasses:
            mc._subscribe(cls)

# class Test(DEFAULT_OPTIONS_CLASS):
#     #hallo = "Welt"
#     ...
#
# class TestSub(Test):
#     wie_gehts = "Gut"
#
# Test.hallo = "Neu"
#
# print(Test.apply({"hallo":None}))
# print(TestSub.apply({"hallo":None}))
#
# Test.hallo = None
#
# print(Test.apply({"hallo":None}))
# print(TestSub.apply({"hallo":None}))
#
# exit()

class EMPTY(DEFAULT_OPTIONS_CLASS):
    """
    Use this class if no global options should be applied
    """
    pass

class Common(DEFAULT_OPTIONS_CLASS):
    """
    Every widget
    """
    cursor:Literals.cursor = None   # Find available cursors here (2025): https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
    takefocus:bool = True
    # expand:bool = False
    # expand_y: bool = False

    # These are reserves for now.
    # They don't work on windows.
    # If you want them included, tell me on GitHub.
    highlightthickness: int = 0
    highlightcolor: Color | str = None
    highlightbackground_color: str | Color = None

class Common_Background(DEFAULT_OPTIONS_CLASS):
    """
    Common background-color, mainly for pseudo-transparent elements
    """
    background_color: str | Color = "#F0F0F0"
    background_color_disabled: str | Color = None

class Common_Field_Background(DEFAULT_OPTIONS_CLASS):
    """
    Common background-color for fields with texts not covered by Common_Background
    """
    background_color: str | Color = None
    background_color_disabled: str | Color = None

class Common_Textual(DEFAULT_OPTIONS_CLASS):
    """
    Widgets with texts
    """
    fontsize:int = 10
    fonttype:str|Font = font_windows.xProto_Nerd_Font
    font_bold:bool = False
    font_italic:bool = False
    font_underline:bool = False
    font_overstrike:bool = False
    anchor:Literals.anchor = "w"
    text_color:Color|str = None
    text_color_disabled: str | Color = None

class Text(Common, Common_Textual, Common_Background):
    text:str = ""
    takefocus:bool = False
    underline:int = None
    justify:Literal["left","right","center"] = "left"
    #borderwidth:int = "5c" # Does not work
    apply_parent_background_color:bool = True

    padding:Literals.padding = 0
    width:int = None

class Scale(Common_Background, Common_Textual):
    default_value: int | float = None
    number_min: float = None
    number_max: float = None
    resolution: float = None
    showvalue: bool = None
    tickinterval: float = None
    width: int = None
    length: int = None
    sliderlength: int = None
    sliderrelief: Literals.relief = None
    orient: Literal["horizontal", "vertical"] = "horizontal"
    disabled: bool = None
    readonly: bool = None
    borderwidth: int = None
    label: str = None
    troughcolor: str | Color = None
    digits: int = None
    cursor: Literals.cursor = None
    takefocus: bool = None
    apply_parent_background_color: bool = True
    relief: Literals.relief = None
    highlightbackground_color: str | Color = None
    highlightcolor: str | Color = None
    highlightthickness: int = 0
    repeatdelay: int = None
    repeatinterval: int = None
    background_color_active: str | Color = None

class Input(Common,Common_Textual,Common_Field_Background):
    text: str = None
    width: int = None

    take_focus: bool = None

    justify: Literal["left", "right", "center"] = None
    # background_color_disabled: str | Color = None
    background_color_readonly: str | Color = None
    #text_color_disabled: str | Color = None
    readonly: bool = False
    selectbackground_color: str | Color = None
    select_text_color: str | Color = None
    selectborderwidth: int = None
    highlightthickness: int = None
    pass_char: str = None
    disabled: bool = None  # Set state to tk.Normal, or 'disabled'
    relief: Literals.relief = None
    exportselection: bool = None
    validate: Literals.validate = None
    validatecommand: callable = None
    insertbackground_color: str | Color = None
    #
    # Mixed options

class Button(Common,Common_Textual,Common_Field_Background):
    fontsize:int = 9
    anchor:Literals.anchor = "center"

    borderwidth: int = None

    bitmap: Literals.bitmap = None
    bitmap_position: Literals.compound = None
    disabled: bool = None
    text_color_disabled: str | Color = None
    background_color_active: str | Color = None
    text_color_active: str | Color = None

    width: int = None
    height: int = None
    padx: int = None
    pady: int = None

    underline: int = None
    justify: Literal["left", "right", "center"] = None
    overrelief: Literals.relief = None

    relief: Literals.relief = None

    repeatdelay: int = None
    repeatinterval: int = None


class MultistateButton(Button):
    can_deselect: bool = True

class Frame(Common, Common_Background):
    takefocus = False
    padding: Literals.padding = 3
    relief: Literals.relief = "flat"
    alignment: Literals.alignment = None
    apply_parent_background_color: bool = True
    pass_down_background_color: bool = True

    borderwidth: int = None
    highlightthickness: int = None

    padx: int = 2
    pady: int = 2

class GridFrame(Frame):
    ...

class Checkbox(Common, Common_Textual, Common_Background):
    default_value: bool = False
    disabled: bool = None
    apply_parent_background_color: bool = True
    borderwidth:int = None
    #
    check_background_color: str | Color = None
    bitmap_position: Literals.compound = None
    background_color_active: str | Color = None
    text_color_active: str | Color = None
    check_type: Literals.indicatoron = "check"
    #
    width: int = None
    height: int = None
    padx: int = None
    pady: int = None
    #
    #
    underline: int = None
    justify: Literal["left", "right", "center"] = None
    overrelief: Literals.relief = None
    offrelief: Literals.relief = None
    relief: Literals.relief = None
    # hilightbackground_color: str | Color = None

class Radiobutton(Checkbox):
    # hilightbackground_color: str | Color = None,
    # highlightthickness: int = None,
    ...

class Window(Common_Background):
    title = "SwiftGUI Window"
    titlebar: bool = True  # Titlebar visible
    resizeable_width: bool = False
    resizeable_height: bool = False
    fullscreen: bool = False
    transparency: Literals.transparency = 0  # 0-1, 1 meaning invisible
    size: int | tuple[int, int] = (None, None)
    position: tuple[int, int] = (None, None)  # Position on monitor # Todo: Center
    min_size: int | tuple[int, int] = (None, None)
    max_size: int | tuple[int, int] = (None, None)
    icon: str = file_from_b64(Extras.SwiftGUI.icon)
    keep_on_top: bool = False
    ttk_theme: str = "default"
    grab_anywhere: bool = False
    padx: int = 5
    pady: int = 5

class SubWindow(Window):
    ...

class Listbox(Common,Common_Textual,Common_Field_Background):
    no_selection_returns: Any = ""  # Returned when nothing is selected
    activestyle:Literals.activestyle = "none"
    default_list: Iterable[str] = None
    disabled: bool = None
    scrollbar: bool = True
    borderwidth: int = None
    background_color_active: str | Color = None
    selectborderwidth: int = None
    text_color_active: str | Color = None
    selectmode: Literals.selectmode_single = "browse"
    width: int = None
    height: int = None
    relief: Literals.relief = None
    highlightthickness: int = None

class Scrollbar(Scale):
    ...

class FileBrowseButton(Button):
    file_browse_type: Literals.file_browse_types = "open_single"
    file_browse_filetypes: Literals.file_browse_filetypes = (("All files","*"),)
    dont_change_on_abort: bool = False
    file_browse_initial_dir: PathLike | str = None  # initialdir
    file_browse_initial_file: str = None  # initialfile
    file_browse_title: str = None  # title
    file_browse_save_defaultextension: str = None  # defaultextension

class ColorChooserButton(Button):
    color_chooser_title: str = None

class TextField(Input):
    borderwidth: int = None
    scrollbar: bool = False
    height: int = None
    #insertbackground: str | Color = None
    readonly: bool = False  # Set state to tk.Normal, or 'readonly'
    padx: int = None
    pady: int = None

    # Text spacing
    paragraph_spacing: int = None
    paragraph_spacing_above: int = None
    autoline_spacing: int = None
    tabs: int = 4  # Size of tabs in characters
    wrap: Literals.wrap = "word"

    # undo-stack
    undo: bool = False
    can_reset_value_changes: bool = False
    maxundo: int | Literal[-1] = 1024 # -1 means infinite

class Treeview(Common_Field_Background):
    ...

class Table(Listbox):
    fonttype_headings: str = None
    fontsize_headings: int = None
    font_bold_headings: bool = None
    font_italic_headings: bool = None
    font_underline_headings: bool = None
    font_overstrike_headings: bool = None

    background_color_headings: str | Color = None
    background_color_active_headings: str | Color = Color.light_blue

    text_color_headings: str | Color = None
    text_color_active_headings: str | Color = None

    sort_col_by_click: bool = True
    takefocus:bool = False

    selectmode: Literals.selectmode_tree = "browse"
    padding: int | tuple[int, ...] = None


class Separator(Common_Background):
    color: str | Color = Color.light_grey
    weight: int = 2
    padding: int = 3

class SeparatorHorizontal(Separator):
    ...

class SeparatorVertical(Separator):
    ...

class Notebook(Common_Textual, Common_Background):
    borderwidth: int = 1
    event_on_backend_selection: bool = False
    apply_parent_background_color: bool = True
    takefocus: bool = False
    background_color_tabs: str | Color = None
    background_color_tabs_active: str | Color = None
    text_color_tabs: str | Color = None
    text_color_tabs_active: str | Color = None
    fonttype_tabs: str | Font = None
    fontsize_tabs: int = None
    font_bold_tabs: bool = None
    font_italic_tabs: bool = None
    font_underline_tabs: bool = None
    font_overstrike_tabs: bool = None
    padding: int | tuple[int, ...] = None
    width: int = None
    height: int = None
    cursor: Literals.cursor = None
    tabposition: Literals.tabposition = None
    expand: bool = None
    expand_y: bool = None

class LabelFrame(Frame, Common_Textual):
    relief: Literals.relief = "solid"
    labelanchor: Literals.tabposition = "nw"
    no_label: bool = False

class TabFrame(Frame):
    text: str = None

class Spinbox(Button, Input):
    default_value: float = None
    value_type: type = float
    cursor_button: Literals.cursor = None
    background_color_button: Color | str = None
    relief_button_down: Literals.relief = None
    relief_button_up: Literals.relief = None
    values: Iterable[float] = None
    wrap: bool = None
    number_format: str = None
    number_min: float = None
    number_max: float = None
    increment: float = None
    repeatdelay: int = 300
    repeatinterval: int = 50
    state: Literals.Spinbox_State = None

class Combobox(Button, Input):
    background_color_disabled: str | Color = None
    button_background_color = None
    button_background_color_active = None
    arrow_color = None
    arrow_color_active = None
    can_change_text: bool = False
    insertbackground: str | Color = None

class Image(Common_Background):
    height: int = None
    width: int = None
    apply_parent_background_color: bool = True

class Progressbar(Common_Field_Background):
    number_max: float = None
    cursor: Literals.cursor = None
    bar_color: str | Color = None
    takefocus: bool = None
    mode: Literals.progress_mode = "determinate"

class ImageButton(Button):
    compound: Literals.compound = "left"

class Console(TextField):
    input_prefix: str = " >>> "
    print_prefix: str = " "
    add_timestamp: bool = True
    scrollbar: bool = True

class Canvas(Common, Common_Field_Background):
    width: int = None
    height: int = None
    select_text_color: str | Color = None
    selectbackground_color: str | Color = None
    selectborderwidth: int = None
    borderwidth:int = None
    takefocus: bool = False
    apply_parent_background_color: bool = None
    highlightthickness: int = None
    confine: bool = None
    scrollregion: tuple[int, int, int, int] = None
    closeenough: int = None
    relief: Literals.relief = None

class Common_Canvas_Element(DEFAULT_OPTIONS_CLASS):
    color: str | sg.Color = None
    color_active: str | sg.Color = None
    color_disabled: str | sg.Color = None
    infill_color: str | sg.Color = ""
    infill_color_active: str | sg.Color = None
    infill_color_disabled: str | sg.Color = None
    state: sg.Literals.canv_elem_state = "normal"

class Common_Canvas_Line(Common_Canvas_Element):
    width: float = 2
    width_active: float = None
    width_disabled: float = None
    dash: sg.Literals.canv_dash = None
    dashoffset: int = None
    dash_active: sg.Literals.canv_dash = None
    dash_disabled: sg.Literals.canv_dash = None

class Canvas_Line(Common_Canvas_Line):
    smooth: bool = None
    splinesteps: int = None
    stipple: sg.Literals.bitmap = None
    stippleoffset: str | tuple[float, float] = None
    stipple_active: sg.Literals.bitmap = None
    stipple_disabled: sg.Literals.bitmap = None
    arrow: sg.Literals.arrow = None
    arrowshape: tuple[float, float, float] = None
    capstyle: sg.Literals.capstyle = None
    joinstyle: sg.Literals.joinstyle = None

class Canvas_Arc(Common_Canvas_Line):
    style: sg.Literals.canv_arc_style = None
    start_angle: float = None
    extent_angle: float = None
    stipple: sg.Literals.bitmap = None
    stippleoffset: str | tuple[float, float] = None
    stipple_active: sg.Literals.bitmap = None
    stipple_disabled: sg.Literals.bitmap = None
    infillstipple: sg.Literals.bitmap = None
    infill_stippleoffset: str | tuple[float, float] = None
    infill_stipple_active: sg.Literals.bitmap = None
    infill_stipple_disabled: sg.Literals.bitmap = None

class Canvas_Bitmap(Common_Canvas_Element):
    bitmap: sg.Literals.bitmap = "question"
    bitmap_active: sg.Literals.bitmap = None
    bitmap_disabled: sg.Literals.bitmap = None
    anchor: sg.Literals.anchor = None
    background_color: sg.Color | str = None
    background_color_active: sg.Color | str = None
    background_color_disabled: sg.Color | str = None

class Canvas_Oval(Common_Canvas_Line):
    stipple: sg.Literals.bitmap = None
    stippleoffset: str | tuple[float, float] = None
    stipple_active: sg.Literals.bitmap = None
    stipple_disabled: sg.Literals.bitmap = None
    infillstipple: sg.Literals.bitmap = None
    infill_stippleoffset: str | tuple[float, float] = None
    infill_stipple_active: sg.Literals.bitmap = None
    infill_stipple_disabled: sg.Literals.bitmap = None

class Canvas_Polygon(Common_Canvas_Line):
    stipple: sg.Literals.bitmap = None
    stippleoffset: str | tuple[float, float] = None
    stipple_active: sg.Literals.bitmap = None
    stipple_disabled: sg.Literals.bitmap = None
    infillstipple: sg.Literals.bitmap = None
    infill_stippleoffset: str | tuple[float, float] = None
    infill_stipple_active: sg.Literals.bitmap = None
    infill_stipple_disabled: sg.Literals.bitmap = None
    smooth: bool = None
    splinesteps: int = None
    joinstyle: sg.Literals.joinstyle = "round"

class Canvas_Rectangle(Common_Canvas_Line):
    stipple: sg.Literals.bitmap = None
    stippleoffset: str | tuple[float, float] = None
    stipple_active: sg.Literals.bitmap = None
    stipple_disabled: sg.Literals.bitmap = None
    infillstipple: sg.Literals.bitmap = None
    infill_stippleoffset: str | tuple[float, float] = None
    infill_stipple_active: sg.Literals.bitmap = None
    infill_stipple_disabled: sg.Literals.bitmap = None

class Canvas_Text(Common_Canvas_Element, Common_Textual):
    width: float = None
    stipple: sg.Literals.bitmap = None
    stippleoffset: str | tuple[float, float] = None
    stipple_active: sg.Literals.bitmap = None
    stipple_disabled: sg.Literals.bitmap = None
    justify: Literal["left", "right", "center"] = None

class Canvas_Element(Common_Canvas_Element):
    anchor: sg.Literals.anchor = None

class Canvas_Image(Common_Canvas_Element, Image):
    image_width: int = None
    image_height: int = None
    anchor: sg.Literals.anchor = None

def reset_all_options():
    """
    Reset everything done to the global options on runtime.

    If you applied a theme, it is also reset, so you might want to reapply it.
    :return:
    """
    for cls in all_option_classes:
        cls.reset_to_default()

