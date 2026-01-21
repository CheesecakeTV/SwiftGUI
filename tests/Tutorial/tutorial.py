import SwiftGUI as sg

sg.Themes.FourColors.Emerald()

layout = [
    [
        sg.In(highlightcolor="orange", highlightbackground_color="red"),
    ],[
        sg.In(),
    ],[
        sg.T("Test")
    ]
]

w = sg.Window(layout)

for e,v in w:
    ...


