
from .Tools import clipboard_copy, clipboard_paste, remove_None_vals

from .Colors import Color,rgb
from .Fonts import *
from . import GlobalOptions, Literals, Tools, Debug
from .ElementFlags import ElementFlag

from .Events import Event
from .Base import BaseElement,BaseWidget,BaseWidgetContainer,ElementFlag,BaseWidgetTTK,BaseCombinedElement
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
from .Widget_Elements.LabelFrame import LabelFrame
from .Widget_Elements.Radiobutton import Radiobutton, RadioGroup
from .Widget_Elements.Spinbox import Spinbox

from .Combined_Elements.Form import Form

from .Extended_Elements.FileBrowseButton import FileBrowseButton
from .Extended_Elements.ColorChooserButton import ColorChooserButton
from .Extended_Elements.TabFrame import TabFrame

from SwiftGUI.Widget_Elements.Image import Image
from SwiftGUI.Widget_Elements.ImageButton import ImageButton

T = Text
Label = Text

Radio = Radiobutton

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

Spin = Spinbox

AnyElement = BaseElement | BaseWidget | Text | Button | Checkbox | Frame | Input | VerticalSeparator | HorizontalSeparator | Spacer | Form | Listbox | FileBrowseButton | ColorChooserButton | TKContainer | TextField | Treeview | Table | Notebook | LabelFrame | Radiobutton | Spinbox | Image | ImageButton

from .Windows import Window

from . import KeyFunctions

from .Examples import preview_all_colors, preview_all_themes, preview_all_fonts_windows
from .Popups.Popups import popup
from .Popups.VirtualKeyboard import popup_virtual_keyboard

from .Themes import Themes

from .Utilities.Threads import clipboard_observer
from .Utilities.Images import file_from_b64, file_to_b64
