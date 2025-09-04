import tkinter as tk
from os import PathLike
from tkinter import filedialog as fd
from collections.abc import Iterable, Callable
from typing import Literal, Any

from SwiftGUI import GlobalOptions, Literals, Color
from SwiftGUI.Widget_Elements.Button import Button


class FileBrowseButton(Button):
    tk_widget:tk.Button
    _tk_widget_class:type = tk.Button # Class of the connected widget
    defaults = GlobalOptions.FileBrowseButton

    def __init__(
            # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/button.html

            self,
            # Add here
            text:str = "",
            /,
            key:Any = None,
            key_function:Callable|Iterable[Callable] = None,

            file_browse_type:Literals.file_browse_types = None, #{"defaultextension","parent","title"}
            file_browse_initial_dir: PathLike|str = None, # initialdir
            file_browse_filetypes: Literals.file_browse_filetypes = None, # filetypes
            file_browse_initial_file: str = None, # initialfile
            file_browse_title: str = None,  # title
            file_browse_save_defaultextension: str = None, # defaultextension
            # Todo: parent
            dont_change_on_abort: bool = None,

            borderwidth:int = None,

            bitmap:Literals.bitmap = None,
            disabled:bool = None,
            text_color_disabled: str | Color = None,
            background_color_active: str | Color = None,
            text_color_active: str | Color = None,

            width: int = None,
            height: int = None,
            padx:int = None,
            pady:int = None,

            cursor: Literals.cursor = None,
            takefocus: bool = None,

            underline: int = None,
            anchor: Literals.anchor = None,
            justify: Literal["left", "right", "center"] = None,
            background_color: str | Color = None,
            overrelief: Literals.relief = None,
            text_color: str | Color = None,

            relief: Literals.relief = None,

            repeatdelay:int = None,
            repeatinterval:int = None,

            # # Mixed options
            fonttype: str = None,
            fontsize: int = None,
            font_bold: bool = None,
            font_italic: bool = None,
            font_underline: bool = None,
            font_overstrike: bool = None,

            expand: bool = None,
            expand_y: bool = None,
            tk_kwargs: dict[str:Any] = None
    ):
        """
        A button that opens a filebrowser when pushed.

        :param text: Text the button displays
        :param key: (See docs for more details)
        :param key_function: (See docs for more details)

        :param file_browse_type: Type of filebrowser (e.g. getting a single file, saving a file, etc.)
        :param file_browse_initial_dir: Directory to start browsing in. "." to start in the working dir, ".." for the dir above.
        :param file_browse_filetypes: Possible types when reading files. Format like this: (("Description1":".extension1"), ("Description2":".extension2"))
        :param file_browse_initial_file: IT WON'T SELECT THE FILE, just put the filename inside the box on the bottom
        :param file_browse_title: Title of the file-browse-window
        :param file_browse_save_defaultextension: When saving, this extension will be added if the user doesn't provide an extension
        :param dont_change_on_abort: If True, the value will not change when the user cancels/closes the file-browse

        :param borderwidth: Border-Thickness in pixels. Default is 2
        :param bitmap: The are a couple of icons builtin. If you are using PyCharm, they should be suggested when pressing "ctrl+space"
        :param disabled: True, if this button should not be pressable
        :param text_color_disabled: Text color, if disabled = True
        :param background_color_active: Background color shown only when the button is held down
        :param text_color_active: Text color only shown when the button is held down
        :param width: Button-size in x-direction in text-characters
        :param height: Button-height in text-rows
        :param padx: Adds space to both sides not filled with text. Should not be combined with "width". The value is given in characters
        :param pady: Adds space to the top and bottom not filled with text. Should not be combined with "height". The value is given in rows
        :param cursor: How the cursor should look when hovering over this element.
        :param takefocus: True, if this element should be able to get focus (e.g. by pressing tab)
        :param underline: Underlines the single character at this index
        :param anchor: Specifies, where the text in this element should be placed (See docs for more details)
        :param justify: When the text is multiple rows long, this will specify where the new rows begin.
        :param background_color: Background-color for the non-pressed state
        :param overrelief: Relief when the mouse hovers over the element
        :param text_color: Text-color in non-pressed state
        :param relief: Relief in non-pressed state
        :param repeatdelay: How long to hold the button until repeation starts (doesn't work without "repeatinterval")
        :param repeatinterval: How long to wait between repetitions (doesn't work without "repeatdelay")
        :param fonttype: Use sg.font_windows. ... to select some fancy font. Personally, I like sg.font_windows.Small_Fonts
        :param fontsize: Size (height) of the font in pixels
        :param font_bold: True, if thicc text
        :param font_italic: True, if italic text
        :param font_underline: True, if the text should be underlined
        :param font_overstrike: True, if the text should be overstruck
        :param tk_kwargs: (Only if you know tkinter) Pass more kwargs directly to the tk-widget
        """
        if callable(key_function):
            key_function = (self._button_callback,key_function)
        elif key_function:
            key_function = (self._button_callback,*tuple(key_function))
        else:
            key_function = self._button_callback

        super().__init__(
            text,
            key=key,
            key_function=key_function,
            borderwidth=borderwidth,
            bitmap=bitmap,
            disabled=disabled,
            text_color_disabled=text_color_disabled,
            background_color_active=background_color_active,
            text_color_active=text_color_active,
            width=width,
            height=height,
            padx=padx,
            pady=pady,
            cursor=cursor,
            takefocus=takefocus,
            underline=underline,
            anchor=anchor,
            justify=justify,
            background_color=background_color,
            overrelief=overrelief,
            text_color=text_color,
            relief=relief,
            repeatdelay=repeatdelay,
            repeatinterval=repeatinterval,
            fonttype=fonttype,
            fontsize=fontsize,
            font_bold=font_bold,
            font_italic=font_italic,
            font_underline=font_underline,
            font_overstrike=font_overstrike,
            expand=expand,
            expand_y = expand_y,
            tk_kwargs=tk_kwargs,
        )

        self._file_function_kwargs = dict()

        self._update_initial(file_browse_type=file_browse_type, file_browse_initial_dir=file_browse_initial_dir,
                             file_browse_filetypes=file_browse_filetypes,
                             file_browse_initial_file=file_browse_initial_file, file_browse_title=file_browse_title,
                             file_browse_save_defaultextension=file_browse_save_defaultextension,
                             dont_change_on_abort=dont_change_on_abort)

    _prev_val:str|tuple[str] = None
    _file_function_wanted = None
    _dont_change_on_abort = None    # If the value should be unchanged if the user just closes the window
    def _button_callback(self):
        if self._file_function is None:
            return

        # Only provide arguments the file-function actually wants
        kwargs = self._file_function_kwargs
        offers = kwargs.fromkeys(kwargs.keys() & self._file_function_wanted)
        offers = {i:kwargs[i] for i in offers}

        # Call the file-dialogue
        temp = self._file_function(**offers)

        if self._dont_change_on_abort and not temp:
            return

        self._prev_val = temp
        return True # Refresh values for coming key_functions

    def _get_value(self) -> Any:
        return self._prev_val

    def set_value(self,val:Any):
        self._prev_val = val

    _file_function: Callable = None
    _file_function_kwargs: dict
    def _update_special_key(self,key:str,new_val:Any) -> bool|None:
        match key:
            case "file_browse_type":
                self._file_function = {
                    "open_single": fd.askopenfilename,
                    "open_multiple": fd.askopenfilenames,
                    "open_directory": fd.askdirectory,
                    "save_single": fd.asksaveasfilename,
                }[new_val]
                self._file_function_wanted = {
                    "open_single": {"defaultextension","filetypes","initialdir","initialfile","parent","title"},
                    "open_multiple": {"defaultextension","filetypes","initialdir","initialfile","parent","title"},
                    "open_directory": {"initialdir","mustexist","parent","title"},
                    "save_single": {"defaultextension","filetypes","initialdir","initialfile","parent","title"},
                }[new_val]

            case "file_browse_initial_dir":
                self._file_function_kwargs["initialdir"] = new_val
            case "file_browse_filetypes":
                self._file_function_kwargs["filetypes"] = new_val
            case "file_browse_initial_file":
                self._file_function_kwargs["initialfile"] = new_val
            case "dont_change_on_abort":
                self._dont_change_on_abort = new_val
            case "file_browse_title":
                self._file_function_kwargs["title"] = new_val
            case "file_browse_save_defaultextension":
                self._file_function_kwargs["file_browse_save_defaultextension"] = new_val
            case _:
                return super()._update_special_key(key, new_val)

        return True

    def _personal_init_inherit(self):
        pass    # Avoid creating a target variable for this button, so the text can be changed with .update(text="...")

