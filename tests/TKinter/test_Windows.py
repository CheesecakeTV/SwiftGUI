import SwiftGUI_LeButch as sg
from SwiftGUI_LeButch import Event

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
    ],[
        sg.Button("Hallo Welt-Button",key="Hallo Welt",key_function=lambda :print("Yooo")),
        sg.In("Was geht",key="Input-Test")
    ],[
        sg.Form(["Hallo","Welt","Das","Ist","Ein","Test"],key="Form.")
    ]
]

w = sg.Window(layout)
w["Input-Test"].bind_event(Event.ClickDoubleLeft,key_function=lambda val:print("Input:",val),send_val=True)

while True:
    e = w.loop()
    print(e,w.values)

    if not w.exists:
        break





