from typing import Hashable, Any
import SwiftGUI as sg

# Only for the typehint. You can leave these out
from SwiftGUI import ValueDict
from SwiftGUI.Compat import Self

#sg.Themes.FourColors.TransgressionTown()
#sg.Examples.preview_all_elements()
#exit()

layout = [
    [
        my_frame := sg.Frame(
            [[sg.T("Hallo Welt", apply_parent_background_color= True)]],
        )
    ],[
        sg.Button(
            "Add row",
            key= "Add"
        ),
        sg.Button(
            "Delete",
            key_function= lambda: my_frame.delete()
        ),
        sg.Button(
            "EV",
            key= "EV"
        )
    ]
]

w = sg.Window(layout)

for e,v in w:
    print(e,v)

    if e == "Add":
        my_frame.add_row([
            sg.T("New Row "),
            sg.Button("Hello", key="Hello", key_function=lambda elem: elem.delete())
        ])
        my_frame.update(background_color= "red")

    if e == "EV":
        my_frame.update(background_color= "blue")

