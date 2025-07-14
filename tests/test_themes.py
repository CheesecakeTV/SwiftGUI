import SwiftGUI as sg

sg.themes.Hacker()

layout = [
    [
        sg.T("Hallo Welt",padding=(150,0))
    ],[
        sg.HSep()
    ],[
        sg.Input("Some input")
    ],[
        sg.Input("Some disabled input...?",readonly=True)
    ],[
        sg.Button("And a button.")
    ],[
        sg.Check("Very cool?")
    ]
]

w = sg.Window(layout)

for e,v in w:
    print(e,v)
