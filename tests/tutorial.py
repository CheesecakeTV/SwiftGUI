from typing import Hashable, Any
import SwiftGUI as sg

# Only for the typehint. You can leave these out
from SwiftGUI import ValueDict
from SwiftGUI.Compat import Self

sg.Themes.FourColors.TransgressionTown()
#sg.Examples.preview_all_elements()
#exit()

layout = [
    [
        my_frame := sg.LabelFrame(
            [],
            text= "Test"
        )
    ],[
        sg.Button(
            "Add row",
            key= "Add"
        )
    ]
]

w = sg.Window(layout)

for e,v in w:
    print(e,v)

    if e == "Add":
        my_frame.add_row([
            sg.T("New Row "),
            sg.Button("Hello", key= "Hello",)
        ])

