import sys
import io
from typing import Callable, Hashable, Literal, Any

import SwiftGUI as sg
from SwiftGUI.Compat import Self

Literals = sg.Literals
Color = sg.Color

class _Rerouter(io.StringIO):

    def __init__(
            self,
            route_where: Callable,
    ):
        """
        Ment to reroute writes to stdout, stderr and stdin
        :param route_where: This callable is called when the rerouter receives a write
        """
        self._route_where = route_where
        super().__init__()

    def write(self, s, /):
        self._route_where(s)
        return super().write(s)

    def readline(self, size = -1, /):
        return self._route_where()

class PythonConsole(sg.TextField):
    defaults = sg.GlobalOptions.PythonConsole

    def __init__(
            self,
            text: str = "",
            *,
            key: Hashable = None,
            #key_function: Callable | Iterable[Callable] = None,
            #default_event: bool = False,   # The console has no default event

            reroute_stdout: bool = True,
            reroute_stderr: bool = False,
            reroute_stdin: bool = True,

            scrollbar: bool = None,

            width: int = None,
            height: int = None,
            borderwidth: int = None,
            relief: Literals.relief = None,

            cursor: Literals.cursor = None,
            takefocus: bool = None,
            background_color: str | Color = None,

            text_color: str | Color = None,
            input_text_color: str | Color = None,
            error_text_color: str | Color = None,
            select_text_color: str | Color = None,
            highlightbackground_color: str | Color = None,
            selectbackground_color: str | Color = None,
            highlightcolor: str | Color = None,
            highlightthickness: int = None,
            insertbackground_color: str | Color = None,
            selectborderwidth: int = None,
            exportselection: bool = None,

            #readonly: bool = None,  # Set state to tk.Normal, or 'readonly'

            padx: int = None,
            pady: int = None,

            fonttype: str = None,
            fontsize: int = None,
            font_bold: bool = None,
            font_italic: bool = None,
            font_underline: bool = None,
            font_overstrike: bool = None,

            paragraph_spacing: int = None,
            paragraph_spacing_above: int = None,
            autoline_spacing: int = None,
            tabs: int = None,  # Size of tabs in characters
            wrap: Literals.wrap = None,

            undo: bool = None,
            can_reset_value_changes: bool = None,
            maxundo: int | Literal[-1] = None,

            expand: bool = None,
            expand_y: bool = None,
            tk_kwargs: dict[str, Any] = None
    ):
        """
        If you want to use print(...) and input(...) with your UI, this element should be used.
        Most of its options are the same as with sg.TextField.

        Important options:
            reroute_stdout (default True):
                If True, print(...) will "print" to this element now

            reroute_stderr (default False):
                If True, warnings and exceptions are printed on this element now

            reroute_stdin: bool = True,
        """

        super().__init__(
            text=text,
            key=key,
            default_event=False,
            #key_function=key_function,
            scrollbar=scrollbar,
            borderwidth = borderwidth,
            width = width,
            height = height,
            highlightbackground_color = highlightbackground_color,
            selectbackground_color = selectbackground_color,
            select_text_color = select_text_color,
            selectborderwidth = selectborderwidth,
            highlightcolor = highlightcolor,
            highlightthickness = highlightthickness,
            readonly = True,
            relief = relief,
            exportselection = exportselection,
            padx = padx,
            pady = pady,
            paragraph_spacing = paragraph_spacing,
            paragraph_spacing_above = paragraph_spacing_above,
            autoline_spacing = autoline_spacing,
            tabs = tabs,
            wrap = wrap,
            undo = undo,
            can_reset_value_changes = can_reset_value_changes,
            maxundo = maxundo,
            cursor = cursor,
            background_color = background_color,
            text_color = text_color,
            fonttype = fonttype,
            fontsize = fontsize,
            font_bold = font_bold,
            font_italic = font_italic,
            font_underline = font_underline,
            font_overstrike = font_overstrike,
            takefocus = takefocus,
            insertbackground_color = insertbackground_color,
            expand=expand,
            expand_y=expand_y,
            tk_kwargs=tk_kwargs,
        )

        self._update_initial(
            error_text_color = error_text_color,
            input_text_color = input_text_color,
        )

        self._default_stdout = sys.stdout
        self._reroute_stdout = reroute_stdout
        if reroute_stdout:
            sys.stdout = _Rerouter(self.write)

        self._default_stderr = sys.stderr
        self._reroute_stderr = reroute_stderr
        if reroute_stderr:
            sys.stderr = _Rerouter(self.write_error)

        self._default_stdin = sys.stdin
        self._reroute_stdin = reroute_stdin
        if reroute_stdin:
            sys.stdin = _Rerouter(self.get_input)

    def _update_special_key(self,key:str,new_val:Any) -> bool|None:
        match key:
            case "error_text_color":
                if new_val is None:
                    return True

                if self.window is None:
                    self.update_after_window_creation(error_text_color = new_val)
                    return True

                self.tk_widget.tag_config("error", foreground=new_val)

            case "input_text_color":
                if new_val is None:
                    return True

                if self.window is None:
                    self.update_after_window_creation(input_text_color = new_val)
                    return True

                self.tk_widget.tag_config("input", foreground=new_val)

            case _:
                return super()._update_special_key(key, new_val)

        return True

    _most_recent_line: str = "" # Stores the most recent text printed to the console until a newline is reached

    @sg.TextField._run_after_window_creation
    def write(self, s: str) -> Self:
        """
        Print something to this "console"
        :param s:
        :return:
        """
        if self._default_stdout is not None:
            self._default_stdout.write(s)

        if self._most_recent_line and self._most_recent_line[-1] == "\n":
            self._most_recent_line = ""

        self._most_recent_line += s

        self.append(s, add_newline=False)
        return self

    @sg.TextField._run_after_window_creation
    def write_error(self, s: str) -> Self:
        """
        Print something to this "console", but with (usually) red text
        :param s:
        :return:
        """
        self.append(s, add_newline=False, tags="error")

        if self._default_stderr is not None:
            self._default_stderr.write(s)

        return self

    @sg.TextField._run_after_window_creation
    def write_input(self, s:str) -> Self:
        """
        Simulates a user-entry.
        :param s:
        :return:
        """
        s += "\n"
        if s:
            self.append(s, add_newline=False, tags="input")

        if self._default_stdout is not None:
            self._default_stdout.write(s)

        return self

    def get_input(self) -> str:
        """
        Same as input(), but returns a new-line at the end
        :return:
        """
        ret = sg.Popups.get_text(text=self._most_recent_line.rstrip(), default="")
        self.write_input(ret)

        return ret + "\n"

    def init_window_creation_done(self):
        super().init_window_creation_done()
        self.tk_widget.bind("<Destroy>", self._handle_destruction, add=True)

    def to_json(self) -> None:
        return None

    def from_json(self, val: Any) -> sg.Compat.Self:
        return self

    def _handle_destruction(self, *_):
        """
        Called when this element is destroyed, aka the window closed.
        Resets the changes to sys.
        :param _:
        :return:
        """
        if self._reroute_stdout:
            sys.stdout = self._default_stdout

        if self._reroute_stdin:
            sys.stdin = self._default_stdin

        if self._reroute_stderr:
            sys.stderr = self._default_stderr

