import SwiftGUI as sg



layout = [
    [
        sg.Multiline("Das ist ein Text",key="ML")
    ]
]



w = sg.Window(layout)
#w["ML"].value = "Hallo Welt!"

for e,v in w:
    print(e,v)
