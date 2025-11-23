from SwiftGUI import GlobalOptions as go
from SwiftGUI import font_windows, Color

from SwiftGUI.Themes._BaseTheme import BaseTheme

class BaseThematic(BaseTheme):
    suffix = "Thematic"

class FacebookMom(BaseThematic):
    def apply(self) -> None:
        #go.Common.background_color = Color.light_goldenrod_yellow
        go.Common_Background.background_color = Color.light_goldenrod_yellow
        go.Common_Field_Background.background_color = Color.hot_pink
        go.Common_Field_Background.background_color_disabled = Color.orange_red

        go.Common_Textual.fonttype = font_windows.Comic_Sans_MS
        go.Common_Textual.fontsize = 16
        go.Common_Textual.text_color = Color.navy

        go.Button.fontsize = 12
        go.Button.font_bold = True
        go.Button.borderwidth = 3
        go.Button.background_color = Color.plum1

        go.Spinbox.background_color_button = Color.plum1

        go.Input.text_color = Color.dark_green

        go.Checkbox.text_color = Color.DeepPink4

        go.Separator.color = Color.turquoise4

        go.Listbox.background_color_active = Color.SeaGreen1
        go.Listbox.text_color_active = Color.RoyalBlue1

        go.Notebook.background_color_tabs = Color.khaki1

        go.Table.background_color_headings = Color.khaki1

        go.Combobox.selectbackground_color = Color.DeepPink4

        go.Scale.troughcolor = "green"

        go.Progressbar.bar_color = Color.LightSalmon2

        #go.Button.background_color = Color.green2

class Hacker(BaseThematic):

    def apply(self) -> None:
        lime = "lime"
        black = "black"
        red = Color.orange_red

        go.Common_Field_Background.background_color = black
        go.Common_Field_Background.background_color_disabled = black

        go.Common_Textual.fonttype = font_windows.Fixedsys
        go.Common_Textual.text_color = lime
        go.Common_Textual.text_color_disabled = red

        go.Input.text_color = lime
        go.Input.background_color_readonly = black
        go.Input.selectbackground_color = red
        go.Input.insertbackground_color = lime
        go.Input.select_text_color = black
        go.Input.background_color_readonly = black

        go.Button.background_color_active = lime
        go.Button.text_color_active = black

        go.Checkbox.background_color_active = lime
        go.Checkbox.check_background_color = black

        go.Common_Background.background_color = black
        go.Common.background_color = black

        go.Listbox.highlightbackground_color = lime
        go.Listbox.highlightcolor = lime
        go.Listbox.text_color_active = black
        go.Listbox.background_color_active = lime

        go.Table.background_color_headings = black
        go.Table.text_color_headings = lime

        go.TextField.highlightbackground_color = lime

        go.Separator.color = red

        go.Combobox.button_background_color = black
        go.Combobox.arrow_color = lime
        go.Combobox.arrow_color_active = black
        go.Combobox.button_background_color_active = lime
        go.Combobox.selectbackground_color = lime

        go.Scale.troughcolor = black
        go.Scale.background_color_active = lime

        go.Spinbox.background_color_button = black

        go.Progressbar.bar_color = red

        go.Notebook.background_color_tabs = black
        go.Notebook.text_color_tabs = lime
        go.Notebook.text_color_tabs_active = red

        go.Table.text_color_headings = red
        go.Table.text_color_active_headings = black
        go.Table.background_color_headings = black
        go.Table.background_color_active_headings = red

        go.Canvas.highlightbackground_color = black

        go.Scrollbar.background_color = lime
        go.Scrollbar.text_color = black

        go.Common_Canvas_Element.color = red
        go.Canvas_Text.color = lime


