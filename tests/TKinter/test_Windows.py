#from SwiftGUI_LeButch import Windows as sg
import SwiftGUI_LeButch as sg


layout = [
    [
        sg.T("Hallo")
    ],[
        sg.T("Welt")
    ],[
        sg.T("Amazing what you can accomplish on a saturday"),
        sg.Frame([
            [
                sg.T("I am")
            ],[
                sg.T("Inside of another Frame!")
            ]
        ])
    ]
]


w = sg.Window(layout)
w.loop()
print(w.allElements)
