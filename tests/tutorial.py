import SwiftGUI as sg
from pathlib import Path
import os

sg.Themes.FourColors.SinCity()

layout = [
    [
        sg.T("Hallo Welt"),
    ],[
        sg.Canvas(
            highlightbackground_color="red",
            key= "Canvas",
            default_event=True
        ).bind_event(
            "<Return>",
            key_function= lambda :print("Hi")
        )
    ],[
        sg.Scale(
            default_event=True,
            key= "Scale",
            expand= True,
        )
    ]
]

w = sg.Window(layout)

for e,v in w:
    print(e, v)
