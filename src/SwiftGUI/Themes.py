from SwiftGUI import GlobalOptions as go
from SwiftGUI import font_windows, Color
from abc import abstractmethod

class BaseTheme:
    """
    Inherit this to create your own theme
    """

    def __init__(self):
        self.apply()

    def __call__(self, *args, **kwargs):
        self.apply()

    @abstractmethod
    def apply(self) -> None:
        """
        Configurations belong in here
        :return:
        """
        raise NotImplementedError("You tried to apply BaseTheme. BaseTheme should not be applied, it is only to create more themes from.")

class FacebookMom(BaseTheme):
    def apply(self) -> None:
        #go.Common.background_color = Color.light_goldenrod_yellow
        go.Common_Background.background_color = Color.light_goldenrod_yellow

        go.Common_Textual.fonttype = font_windows.Comic_Sans_MS
        go.Common_Textual.fontsize = 16

        go.Button.fontsize = 12
        go.Button.font_bold = True
        go.Button.borderwidth = 3

        go.Input.background_color = Color.hot_pink
        go.Input.text_color = Color.dark_green
        go.Input.background_color_readonly = Color.orange_red

        go.Button.background_color = Color.green2

class Hacker(BaseTheme):

    def apply(self) -> None:
        go.Common_Textual.fonttype = font_windows.Fixedsys
        go.Common_Textual.text_color = "lime"

        go.Input.text_color = "black"
        go.Input.background_color = "lime"
        go.Input.background_color_readonly = Color.orange_red
        go.Input.selectbackground_color = Color.royal_blue
        go.Input.select_text_color = "black"

        go.Button.background_color_active = "lime"
        go.Button.text_color_active = "black"

        go.Checkbox.background_color_active = "lime"
        go.Checkbox.check_background_color = "black"

        go.Common_Background.background_color = "black"
        go.Common.background_color = "black"

        go.Listbox.highlightbackground_color = "lime"
        go.Listbox.highlightcolor = "lime"
        go.Listbox.text_color_selected = "black"
        go.Listbox.background_color_selected = "lime"

        go.Table.background_color_headings = "black"
        go.Table.text_color_headings = "lime"

        go.TextField.highlightbackground_color = "lime"

        go.Separator.color = "red"



class Themes:
    """
    All available Themes
    """
    BaseTheme = BaseTheme

    FacebookMom = FacebookMom
    Hacker = Hacker

