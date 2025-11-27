from typing import Hashable, Any, Callable
import SwiftGUI as sg
import json
import pathlib

sg.Themes.FourColors.TransgressionTown()

layout = [
    [
        sg.Spinbox(
            range(1, 101),
            key= "Spin",
            default_event= True,
        )
    ]
]

w = sg.SubWindow(layout)

for e,v in w:
    print(e,v)
