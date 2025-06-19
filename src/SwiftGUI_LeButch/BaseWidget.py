from abc import abstractmethod
from tkinter import Widget,Frame

class BaseWidget:
    """
    Base for every Widget
    """

    @abstractmethod
    def tk_widget(self) -> Widget:
        """
        Returns the tkinter widget connected to this sg-widget
        :return:
        """
        ...

    def init_widget(self,container:Frame) -> None:
        """
        Initialize the widget to the container
        :return:
        """
        ...


