import SwiftGUI as sg
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














class themes:
    """
    All available Themes
    """
    ...

