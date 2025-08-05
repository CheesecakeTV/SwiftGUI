
from .Colors import Color,rgb
from .Fonts import *
from . import GlobalOptions, Literals, Tools
from .ElementFlags import ElementFlag

from .Events import Event
from .Base import BaseElement,BaseWidget,BaseWidgetContainer,ElementFlag,BaseWidgetTTK
#from .KeyManager import Key,SEPARATOR,duplicate_warnings   # Todo: Make some decent key-manager

from .Widget_Elements.Text import Text
from .Widget_Elements.Button import Button
from .Widget_Elements.Checkbox import Checkbox
from .Widget_Elements.Frame import Frame
from .Widget_Elements.Input import Input
from .Widget_Elements.Separator import VerticalSeparator,HorizontalSeparator
from .Widget_Elements.Spacer import Spacer
from .Widget_Elements.Listbox import Listbox
from .Widget_Elements.TKContainer import TKContainer
from .Widget_Elements.TextField import TextField
from .Widget_Elements.Treeview import Treeview
from .Widget_Elements.Table import Table
from .Widget_Elements.Notebook import Notebook

from .Combined_Elements.Form import Form

from .Extended_Elements.FileBrowseButton import FileBrowseButton
from .Extended_Elements.ColorChooserButton import ColorChooserButton

T = Text
Label = Text

In = Input
Entry = Input

HSep = HorizontalSeparator
VSep = VerticalSeparator

Check = Checkbox
Checkbutton = Checkbox

Column = Frame

S = Spacer

TKWidget = TKContainer

Multiline = TextField

TabView = Notebook

AnyElement = BaseElement | BaseWidget | Text | Button | Checkbox | Frame | Input | VerticalSeparator | HorizontalSeparator | Spacer | Form | Listbox | FileBrowseButton | ColorChooserButton | TKContainer | TextField | Treeview | Table | Notebook

from .Windows import Window

from . import KeyFunctions

from .Examples import preview_all_colors, preview_all_themes, preview_all_fonts_windows
from .Popups import popup

from .Themes import Themes
