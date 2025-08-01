import tkinter as tk
import tkinter.font as font
from collections.abc import Iterable, Callable
from typing import Literal, Any

from SwiftGUI import ElementFlag, BaseWidget, GlobalOptions, Literals, Color


class TextField(BaseWidget):
    tk_widget:tk.Text
    _tk_widget:tk.Text
    _tk_widget_class:type = tk.Text # Class of the connected widget
    defaults = GlobalOptions.TextField

    _transfer_keys = {
        # "background_color_disabled":"disabledbackground",
        "background_color":"background",
        # "text_color_disabled": "disabledforeground",
        "highlightbackground_color": "highlightbackground",
        "selectbackground_color": "selectbackground",
        "select_text_color": "selectforeground",
        # "pass_char":"show",
        "background_color_active" : "activebackground",
        "text_color_active" : "activeforeground",
        "text_color":"fg",
        "paragraph_spacing_above": "spacing1",
        "autoline_spacing": "spacing2",
        "paragraph_spacing": "spacing3",
    }

    # Todo: There are a ton of additional methods and options to add
    # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/text.html
    def __init__(
            self,
            # Add here
            text:str = None,
            /,
            key: Any = None,
            key_function: Callable|Iterable[Callable] = None,
            borderwidth: int = None,
            width: int=None,
            height: int = None,
            default_event:bool = False,
            cursor:Literals.cursor = None,
            takefocus:bool = None,
            background_color:str|Color = None,
            insertbackground: str|Color = None,
            text_color: str|Color = None,
            highlightbackground_color:str|Color = None,
            selectbackground_color:str|Color = None,
            select_text_color:str|Color = None,
            selectborderwidth:int = None,
            highlightcolor:str|Color = None,
            highlightthickness:int = None,
            readonly: bool = None,   # Set state to tk.Normal, or 'readonly'
            relief: Literals.relief = None,
            exportselection:bool = None,
            padx: int = None,
            pady: int = None,

            # Font
            fonttype:str = None,
            fontsize:int = None,
            font_bold:bool = None,
            font_italic:bool = None,
            font_underline:bool = None,
            font_overstrike:bool = None,

            # Text spacing
            paragraph_spacing: int = None,
            paragraph_spacing_above: int = None,
            autoline_spacing: int = None,
            tabs: int = None,   # Size of tabs in characters
            wrap: Literals.wrap = None,

            # undo-stack
            undo: bool = None,
            can_reset_value_changes: bool = None,
            maxundo: int | Literal[-1] = None,

            expand: bool = None,
            tk_kwargs: dict[str:any]=None
    ):
        """
        An Input-Element with multiple rows

        :param text:
        :param key: See docs for more details
        :param key_function: See docs for more details
        :param borderwidth: Thickness of the border around the element
        :param width: Width in characters
        :param height: Height in rows
        :param default_event: True, to throw an event when a key is lifted up (text changed is included)
        :param cursor: Type of cursor when the cursor hovers over this element
        :param takefocus: True, if you want to be able to select this element by pressing "tab"
        :param background_color:
        :param insertbackground: Color of the text-cursor
        :param text_color: font-color
        :param highlightcolor: Color of the outer border (highlightthickness must be > 0) when in focus
        :param highlightbackground_color: Color of the outer border (highlightthickness must be > 0) when not in focus
        :param selectbackground_color: Color behind text that is selected
        :param select_text_color: Text-Color of text that is selected
        :param selectborderwidth: (Might not work on Windows or Mac) Size of the border around selected text
        :param highlightthickness: Thickness of the outer border that displays if this element is selected
        :param readonly: True, if this widget should not accept any input or changes
        :param relief: 3d-shape of this element
        :param exportselection: True, if selected text should be automatically copied to clipboard. (Might not work on Windows)
        :param padx: Space left and right of the text-box. Increase this to 5-10, to make it look a bit better.
        :param pady: Space on top and bottom of the text-box. Increase this to 5-10, to make it look a bit better.
        :param fonttype: Type of font. See sg.font_windows for available fonts on Windows
        :param fontsize: Size (height) of the font in pixels
        :param font_bold: Bold text
        :param font_italic: Italic text
        :param font_underline: Underlined text
        :param font_overstrike: Overstrucken text
        :param paragraph_spacing: Adds some space after a paragraph (When the user presses enter)
        :param paragraph_spacing_above: Adds some space BEFORE a paragraph. I wouldn't use this, because the whole text starts a bit lower then.
        :param autoline_spacing: When a line is full, the next one begins automatically. This option adds some space for these "auto-linebreaks".
        :param tabs: Pressing tab aligns text vertically. This option sets the maximum width of a single "tab".
        :param wrap: When a line is full, the next one begins automatically. Set to "none" if you want to disable this behavior. Set to "word" (default) to break lines at new words. Set to "char" to break lines, but ignore words.
        :param undo: True (default), if you want to enable "Ctrl+z" (undo) and "Ctrl+y" (redo).
        :param can_reset_value_changes: True, if the user should also be able to undo changes made by the program. Default is False.
        :param maxundo: How many changes should be recorded so they can be undone.
        :param expand: True, if this widget should span over the whole row.
        :param tk_kwargs: Additional kwargs for the tk_widget. Don't use it if you don't know tkinter.
        """
        super().__init__(key=key,tk_kwargs=tk_kwargs,expand=expand)

        if tk_kwargs is None:
            tk_kwargs = dict()

        _tk_kwargs = {
            **tk_kwargs,
            "borderwidth": borderwidth,
            "width": width,
            "height": height,
            "insertbackground": insertbackground,
            "highlightbackground_color": highlightbackground_color,
            "selectbackground_color": selectbackground_color,
            "select_text_color": select_text_color,
            "selectborderwidth": selectborderwidth,
            "highlightcolor": highlightcolor,
            "highlightthickness": highlightthickness,
            "readonly": readonly,
            "relief": relief,
            "exportselection": exportselection,
            "padx": padx,
            "pady": pady,
            "paragraph_spacing": paragraph_spacing,
            "paragraph_spacing_above": paragraph_spacing_above,
            "autoline_spacing": autoline_spacing,
            "tabs": tabs,
            "wrap": wrap,
            "undo": undo,
            "can_reset_value_changes": can_reset_value_changes,
            "maxundo": maxundo,
            "cursor":cursor,
            "background_color":background_color,
            "text_color":text_color,
            "fonttype":fonttype,
            "fontsize":fontsize,
            "font_bold":font_bold,
            "font_italic":font_italic,
            "font_underline":font_underline,
            "font_overstrike":font_overstrike,
            "takefocus":takefocus,
        }
        self.update(**_tk_kwargs)

        self._key_function = key_function
        self._initial_text = text

        # self._tabsize = self.defaults.single("tabs",tabs,4)

        if default_event:
            self.bind_event("<KeyRelease>",key=key,key_function=key_function)

    _can_reset_value_changes = False
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
                self._can_reset_value_changes = new_val
            case _:
                return False

        return True

    def _apply_update(self):
        # If the font changed, apply them to self._tk_kwargs
        if self.has_flag(ElementFlag.UPDATE_FONT):
            self._update_font()

        super()._apply_update() # Actually apply the update

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
        return self.tk_widget.get("1.0","end")[:-1]

    def set_value(self,val:any):
        self.tk_widget.delete("1.0","end")
        self.tk_widget.insert("1.0",val)

        if self._can_reset_value_changes:
            self.tk_widget.edit_reset()

    def init_window_creation_done(self):
        super().init_window_creation_done()
        self.value = self._initial_text
        del self._initial_text
