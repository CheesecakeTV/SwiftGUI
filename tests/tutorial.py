import SwiftGUI as sg
import numpy as np

sg.Themes.FourColors.SinCity()

layout = [
    [
        sg.Button(
            "Event",
            key= "Event"
        )
    ]
]

w = sg.Window(layout, padx=30, pady=30).init_timeout(key="Hi", seconds=0.5)
w.init_timeout("Ho")

for e,v in w:
    print(e,v)

