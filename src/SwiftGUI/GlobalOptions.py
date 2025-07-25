#import tkinter as tk    # Not needed, but helpful to figure out default vals
#from tkinter import ttk
from collections.abc import Iterable
from os import PathLike
from typing import Literal, Union

from SwiftGUI import Literals, Color, font_windows, Font

# Every option-class will be stored in here
all_option_classes:list[Union["_DefaultOptionsMeta",type]] = list()

class _DefaultOptionsMeta(type):

    def __new__(mcs, name, bases, namespace):
        _all_defaults = dict(filter(lambda a: not a[0].startswith("_") and not a[0] in ["apply","reset_to_default","single","persist_changes"], namespace.items()))

        # Remove NONE-values so they don't overwrite non-None-values of higher classes
        namespace = dict(filter(lambda a: a[1] is not None, namespace.items()))
        cls:"DEFAULT_OPTIONS_CLASS"|type = super().__new__(mcs, name, bases, namespace)

        cls._all_defaults = _all_defaults # All attributes with None-Attributes

        prev = cls.__mro__[1]
        cls._dict = dict(cls.__dict__)
        cls._reset_all = False

        if hasattr(prev,"_dict"):
            cls._dict.update(dict(prev.__dict__))

        cls.made_changes = True
        cls._persist_changes()

        all_option_classes.append(cls)

        return cls

    def __setattr__(self, key, value):
        if not key.startswith("_") and not key == "made_changes":
            self.made_changes = True

        super().__setattr__(key,value)

        if value is None:
            delattr(self,key)

    def reset_to_default(self):
        """
        Reset all configuration done to any options inside this class
        :return:
        """
        # I know this is very inefficient, but it's not used that often.
        # Don't speed up a function that only runs once every program execution...
        for key,val in self._all_defaults.items():
            setattr(self,key,val)

class DEFAULT_OPTIONS_CLASS(metaclass=_DefaultOptionsMeta):
    """
    Derive from this class to create a "blank" global-options template.

    DON'T ADD ANY OPTIONS HERE!
    """

    _prev_dict:dict = None
    _prev_class_dict:dict = None

    @classmethod
    def _persist_changes(cls):
        """
        Refreshes the _dict if necessary
        :return:
        """
        cls._check_for_changes()
        if not cls.made_changes:
            return
        cls.made_changes = False

        collected = dict()
        for i in cls.__mro__[-1::-1]:
            collected.update(i.__dict__)

        cls._dict = dict(filter(lambda a: not a[0].startswith("_") and not a[0] in ["_dict","reset_to_default","apply","single","persist_changes"], collected.items()))

    @classmethod
    def _check_for_changes(cls):
        """
        Check if any parent-class changed anything
        :return:
        """
        if cls.made_changes:
            return

        my_iter = iter(cls.__mro__[-3::-1])
        for i in my_iter:    # Check higher classes
            if i.made_changes:
                cls.made_changes = True
                break

        for i in my_iter:   # Set changes for all the other classes between you and changed
            i.made_changes = True

    @classmethod
    def apply(cls,apply_to:dict) -> dict:
        """
        Apply default configuration TO EVERY NONE-ELEMENT of apply_to

        :param apply_to: It will be changed AND returned
        :return: apply_to will be changed AND returned
        """
        cls._persist_changes()
        my_dict = cls._dict

        # Get keys with value None that are also in the global options
        items_change:Iterable[tuple] = filter(lambda a: a[1] is None and a[0] in my_dict , apply_to.items())

        for key,_ in items_change:
            apply_to[key] = my_dict[key]

        return apply_to

    @classmethod
    def single(cls,key:str,val:any,default:any=None) -> any:
        """
        val will be returned.
        If val is None, cls.key will be returned.
        If both are None, default will be returned.
        :param default:
        :param key: Name of attribute
        :param val: User-val
        :return:
        """
        cls._persist_changes()
        if not val is None:
            return val

        if hasattr(cls,key):
            return getattr(cls,key)

        return default


class Common(DEFAULT_OPTIONS_CLASS):
    """
    Every widget
    """
    cursor:Literals.cursor = None   # Find available cursors here (2025): https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
    takefocus:bool = True
    expand:bool = False

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

class Text(Common, Common_Textual):
    text:str = ""
    takefocus:bool = False
    underline:int = None
    justify:Literal["left","right","center"] = "left"
    #borderwidth:int = "5c" # Does not work
    apply_parent_background_color:bool = True

    padding:Literals.padding = 0
    width:int = None

class Input(Common,Common_Textual):
    text: str = None
    width: int = None
    #
    # Standard-Tkinter options
    take_focus: bool = None
    #
    # Special Tkinter-options
    justify: Literal["left", "right", "center"] = None
    # background_color_disabled: str | Color = None
    background_color_readonly: str | Color = None
    text_color_disabled: str | Color = None
    highlightbackground_color: str | Color = None
    selectbackground_color: str | Color = None
    select_text_color: str | Color = None
    selectborderwidth: int = None
    highlightcolor: str | Color = None
    highlightthickness: int = None
    pass_char: str = None
    disabled: bool = None  # Set state to tk.Normal, or 'disabled'
    relief: Literals.relief = None
    exportselection: bool = None
    validate: Literals.validate = None
    validatecommand: callable = None
    #
    # Mixed options

class Button(Common,Common_Textual):
    fontsize:int = 9
    anchor:Literals.anchor = "center"

    borderwidth: int = None

    bitmap: Literals.bitmap = None
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

class Frame(Common):
    takefocus = False
    padding: Literals.padding = 3
    relief: Literals.relief = "flat"
    #background = "blue"
    alignment: Literals.alignment = None
    apply_parent_background_color: bool = True

class Checkbox(Common,Common_Textual):
    key: any = None
    default_value: bool = False
    readonly: bool = None
    apply_parent_background_color: bool = True
    # borderwidth:int = None
    #
    text_color_disabled: str | Color = None
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
    # highlightcolor: str | Color = None

class Window(DEFAULT_OPTIONS_CLASS):
    title = None
    background_color:Color|str = "#F0F0F0"
    titlebar: bool = True  # Titlebar visible
    resizeable_width = False
    resizeable_height = False
    fullscreen: bool = False
    transparency: Literals.transparency = 0  # 0-1, 1 meaning invisible
    size: tuple[int, int] = (None, None)
    position: tuple[int, int] = (None, None)  # Position on monitor # Todo: Center
    min_size: tuple[int, int] = (None, None)
    max_size: tuple[int, int] = (None, None)
    icon: str = None  # .ico file
    keep_on_top: bool = False

class Listbox(Common,Common_Textual):
    activestyle:Literals.activestyle = "none"
    default_list: Iterable[str] = None
    disabled: bool = None
    borderwidth: int = None
    background_color_selected: str | Color = None
    selectborderwidth: int = None
    text_color_selected: str | Color = None
    text_color_disabled: str | Color = None
    selectmode: Literals.selectmode_single = "browse"
    width: int = None
    height: int = None
    relief: Literals.relief = None
    highlightbackground_color: str | Color = None
    highlightcolor: str | Color = None
    highlightthickness: int = None

class FileBrowseButton(Button):
    file_browse_type: Literals.file_browse_types = "open_single"
    file_browse_filetypes: Literals.file_browse_filetypes = (("All files","*"),)
    dont_change_on_abort: bool = False
    file_browse_initial_dir: PathLike | str = None,  # initialdir
    file_browse_initial_file: str = None,  # initialfile
    file_browse_title: str = None,  # title
    file_browse_save_defaultextension: str = None,  # defaultextension

class ColorChooserButton(Button):
    color_chooser_title: str = None

class TextField(Common,Common_Textual):
    borderwidth: int = None
    width: int = None
    height: int = None
    insertbackground: str | Color = None
    highlightbackground_color: str | Color = None
    selectbackground_color: str | Color = None
    select_text_color: str | Color = None
    selectborderwidth: int = None
    highlightcolor: str | Color = None
    highlightthickness: int = None
    readonly: bool = False  # Set state to tk.Normal, or 'readonly'
    relief: Literals.relief = None
    exportselection: bool = False
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

class Treeview(DEFAULT_OPTIONS_CLASS):
    ...

def reset_all_options():
    """
    Reset everything done to the global options on runtime.

    If you applied a theme, it is also reset, so you might want to reapply it.
    :return:
    """
    for cls in all_option_classes:
        cls.reset_to_default()

def _make_dict_format_because_lazy(the_class:DEFAULT_OPTIONS_CLASS):
    """
    Use this to print a dict you can just copy instead of making everything yourself

    YOU HAVE TO REMOVE INHERITANCE OF BASE CLASS BEFORE USING THIS!
    Otherwise None-Values will be filtered out

    :param the_class:
    :return:
    """
    for key in the_class._all_defaults:
        if key in ("made_changes","apply","single","persist_changes","key","reset_to_default"):
            continue

        if key.startswith("_"):
            continue

        print(f'"{key}" : {key},')
