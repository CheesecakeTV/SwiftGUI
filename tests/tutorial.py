import SwiftGUI as sg
import SwiftGUI.Canvas_Elements as sgc

sg.Themes.FourColors.RoyalBlue()
sg.Examples.preview_all_elements()
exit()

canv = sg.Canvas(
    sgc.Line(  # Add an element directly
        (10, 10),
        (50, 30),
        (50, 10),
        (70, 30),
        width= 5,
    )
)

layout = [
    [
        canv
    ]
]

w = sg.Window(layout)

for e,v in w:
    print(e, v)
