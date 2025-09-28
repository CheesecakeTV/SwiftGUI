import tkinter.font as font
import tkinter.ttk as ttk
from typing import Literal, Any

from SwiftGUI import ElementFlag, BaseWidget, GlobalOptions, Literals, Color


class Text(BaseWidget):
    """
    Copy this class ot create your own Widget
    """
    _tk_widget_class:type = ttk.Label # Class of the connected widget
    defaults = GlobalOptions.Text   # Default values (Will be applied to kw_args-dict and passed onto the tk_widget

    _grab_anywhere_on_this = True

    _transfer_keys = {
        "background_color": "background",
        "text_color": "foreground",
    }

    def __init__(
            self,
            # Add here
            text:str = None,
            /,
            key:Any=None,
            width:int=None,

            cursor:Literals.cursor = None,
            takefocus:bool = None,

            anchor:Literals.anchor = None,
            justify:Literal["left","right","center"] = None,

            background_color:str|Color = None,
            text_color:str|Color = None,
            apply_parent_background_color:bool = None,

            # Mixed options
            fonttype:str = None,
            fontsize:int = None,
            font_bold:bool = None,
            font_italic:bool = None,
            font_underline:bool = None,
            font_overstrike:bool = None,

            relief:Literals.relief = None,
            padding:Literals.padding = None,
            underline:int = None,

            expand: bool = None,
            expand_y: bool = None,
            tk_kwargs:dict[str:Any]=None
    ):
        """

        :param text:
        :param key:
        :param width:
        :param cursor:
        :param takefocus:
        :param anchor:
        :param justify:
        :param background_color:
        :param text_color:
        :param apply_parent_background_color:
        :param fonttype:
        :param fontsize:
        :param font_bold:
        :param font_italic:
        :param font_underline:
        :param font_overstrike:
        :param relief:
        :param padding:
        :param underline:
        :param expand:
        :param expand_y:
        :param tk_kwargs:
        """

        super().__init__(key=key,tk_kwargs=tk_kwargs,expand=expand, expand_y = expand_y)

        if tk_kwargs is None:
            tk_kwargs = dict()

        if background_color and not apply_parent_background_color:
            apply_parent_background_color = False

        self._update_initial(
            text = text,
            cursor = cursor,
            takefocus = takefocus,
            underline = underline,
            justify = justify,
            background_color = background_color,
            #"borderwidth":borderwidth,
            relief = relief,
            text_color = text_color,
            padding = padding,
            width = width,
            # "wraplength":"1c" # Todo: integrate wraplength in a smart way
            fonttype = fonttype,
            fontsize = fontsize,
            font_bold = font_bold,
            font_italic = font_italic,
            font_underline = font_underline,
            font_overstrike = font_overstrike,
            anchor = anchor,
            apply_parent_background_color =  apply_parent_background_color,
            ** tk_kwargs,
        )

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

    def _update_special_key(self, key:str, new_val: Any) -> bool|None:
        # Fish out all special keys to process them seperately
        match key:
            case "text":
                self._text = new_val
                self.value = new_val
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
            case "apply_parent_background_color":
                if new_val:
                    self.add_flags(ElementFlag.APPLY_PARENT_BACKGROUND_COLOR)
                else:
                    self.remove_flags(ElementFlag.APPLY_PARENT_BACKGROUND_COLOR)
            case _: # Not a match
                return super()._update_special_key(key, new_val)

        return True

    def _apply_update(self):
        # If the font changed, apply them to self._tk_kwargs
        if self.has_flag(ElementFlag.UPDATE_FONT):
            self._update_font()
            self.remove_flags(ElementFlag.UPDATE_FONT)

        super()._apply_update() # Actually apply the update

    def _personal_init_inherit(self):
        self._set_tk_target_variable(default_value=self._text)
