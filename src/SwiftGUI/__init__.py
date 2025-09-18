
from . import Compat
from .Tools import clipboard_copy, clipboard_paste, remove_None_vals

from .Colors import Color,rgb
from .Fonts import *
from . import GlobalOptions, Literals, Tools, Debug
from .ElementFlags import ElementFlag

from .Events import Event
from .Base import BaseElement,BaseWidget,BaseWidgetContainer,ElementFlag,BaseWidgetTTK, BaseScrollbar
#from .KeyManager import Key,SEPARATOR,duplicate_warnings   # Todo: Make some decent key-manager

from .Widget_Elements.Scrollbar import Scrollbar
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
from .Widget_Elements.Scale import Scale
from .Widget_Elements.Combobox import Combobox
from .Widget_Elements.Progressbar import Progressbar, ProgressbarVertical
from .Widget_Elements.GridFrame import GridFrame

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

Slider = Scale

Combo = Combobox


from .Windows import Window, BaseKeyHandler, ttk_style, main_window, SubLayout

from .Combined_Elements.BaseCombinedElement import BaseCombinedElement
from .Combined_Elements.Form import Form
from .Combined_Elements.MultistateButton import MultistateButton

#from .Extended_Elements.SubLayout import SubLayout

from . import KeyFunctions

from . import Themes
from . import Popups
from . import Examples

from .Utilities.Threads import clipboard_observer
from .Utilities.Images import file_from_b64, file_to_b64

AnyElement = BaseElement | BaseWidget | Text | Button | Checkbox | Frame | Input | VerticalSeparator | HorizontalSeparator | Spacer | Form | Listbox | FileBrowseButton | ColorChooserButton | TKContainer | TextField | Treeview | Table | Notebook | LabelFrame | Radiobutton | Spinbox | Image | ImageButton | Scale | Combobox | Progressbar
