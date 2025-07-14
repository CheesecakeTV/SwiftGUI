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
        pass

class FacebookMom(BaseTheme):
    def apply(self) -> None:
        go.Common_Textual.fonttype = font_windows.Comic_Sans_MS
        go.Common_Textual.fontsize = 14

        go.Button.fontsize = 12
        go.Button.font_bold = True
        go.Button.borderwidth = 3

        go.Input.background_color = Color.hot_pink
        go.Input.text_color = Color.dark_green
        go.Input.background_color_readonly = Color.orange_red

        go.Common.background_color = Color.light_goldenrod_yellow
        go.Button.background_color = Color.green2






class themes:
    """
    All available Themes
    """
    FacebookMom = FacebookMom

