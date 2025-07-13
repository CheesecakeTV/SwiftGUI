
from .Colors import Color,rgb
from .Fonts import *
from . import GlobalOptions, Literals, Tools
from .ElementFlags import ElementFlag

from .Events import Event
from .Base import BaseElement,BaseWidget,BaseWidgetContainer,ElementFlag
#from .KeyManager import Key,SEPARATOR,duplicate_warnings   # Todo: Make some decent key-manager

from .Widgets.Text import Text
from .Widgets.Button import Button
from .Widgets.Checkbox import Checkbox
from .Widgets.Frame import Frame
from .Widgets.Input import Input
from .Widgets.Separator import VerticalSeparator,HorizontalSeparator
from .Widgets.Spacer import Spacer

from .WidgetsAdvanced.Form import Form

T = Text

In = Input
Entry = Input

HSep = HorizontalSeparator
VSep = VerticalSeparator

Check = Checkbox

Column = Frame

AnyElement = BaseElement | BaseWidget | Text | Button | Checkbox | Frame | Input | VerticalSeparator | HorizontalSeparator | Spacer | Form

from .Windows import Window

from . import KeyFunctions

from .Examples import preview_all_colors
from .Popups import popup

