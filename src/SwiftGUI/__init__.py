
loaded_addons: set[str] = set() # Contains all included SwiftGUI-addons.
# If you'd like your own addon officially included, create an issue on GitHub.

from . import Extras
from .Utilities.Images import file_from_b64, file_to_b64, image_to_tk_image

from . import Compat
from .Tools import clipboard_copy, clipboard_paste, remove_None_vals

from .Colors import Color,rgb
from .Fonts import *
from . import GlobalOptions, Literals, Tools, Debug
from .ElementFlags import ElementFlag

from .Events import Event
from .Base import BaseElement,BaseWidget,BaseWidgetContainer,ElementFlag,BaseWidgetTTK, BaseScrollbar
#from .KeyManager import Key,SEPARATOR,duplicate_warnings   # Todo: Make some decent key-manager

from .Widget_Elements.Scrollbar import Scrollbar, ScrollbarHorizontal
from .Widget_Elements.Text import Text
from .Widget_Elements.Button import Button
from .Widget_Elements.Checkbox import Checkbox
from .Widget_Elements.Frame import Frame
from .Widget_Elements.Input import Input
from SwiftGUI.Extended_Elements.Separator import VerticalSeparator,HorizontalSeparator
from SwiftGUI.Extended_Elements.Spacer import Spacer
from .Widget_Elements.Listbox import Listbox
from .Widget_Elements.TKContainer import TKContainer
from .Widget_Elements.TextField import TextField
from .Widget_Elements.Treeview import Treeview
from SwiftGUI.Extended_Elements.Table import Table
from .Widget_Elements.Notebook import Notebook
from .Widget_Elements.LabelFrame import LabelFrame
from .Widget_Elements.Radiobutton import Radiobutton, RadioGroup
from .Widget_Elements.Spinbox import Spinbox
from .Widget_Elements.Scale import Scale
from .Widget_Elements.Combobox import Combobox
from .Widget_Elements.Progressbar import Progressbar, ProgressbarVertical
from .Widget_Elements.GridFrame import GridFrame
from .Widget_Elements.Canvas import Canvas

from .Extended_Elements.FileBrowseButton import FileBrowseButton
from .Extended_Elements.ColorChooserButton import ColorChooserButton
from .Extended_Elements.TabFrame import TabFrame

from SwiftGUI.Extended_Elements.Image import Image
from SwiftGUI.Extended_Elements.ImageButton import ImageButton

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


from .Windows import Window, BaseKeyHandler, ttk_style, main_window, SubLayout, all_decorator_key_functions, SubWindow, close_all_windows, ValueDict, call_periodically

from . import KeyFunctions

from . import Themes
from .BasePopup import BasePopup, BasePopupNonblocking
from . import Popups
from . import Examples

from .Combined_Elements.BaseCombinedElement import BaseCombinedElement
from .Combined_Elements.Form import Form
from .Combined_Elements.MultistateButton import MultistateButton
from .Combined_Elements.Console import Console

from .Utilities.Threads import clipboard_observer

AnyElement = BaseElement | BaseWidget | Text | Button | Checkbox | Frame | Input | VerticalSeparator | HorizontalSeparator | Spacer | Form | Listbox | FileBrowseButton | ColorChooserButton | TKContainer | TextField | Treeview | Table | Notebook | LabelFrame | Radiobutton | Spinbox | Image | ImageButton | Scale | Combobox | Progressbar | Console

from .DecoratorKeys import attach_function_to_key

from . import Canvas_Elements

from . import Files

try:
    from SwiftGUI_Matplot import Matplot
    loaded_addons.add("Matplot")
except ImportError:
    Matplot: "Matplot" = Compat.ErrorThrower("To use sg.Matplot, SwiftGUI_Matplot must be installed!")


