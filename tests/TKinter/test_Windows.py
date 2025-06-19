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
    ],[
        sg.Button("Hallo Welt-Button",key="Hallo Welt",key_function=lambda :print("Yooo")),
        sg.In("Was geht",key="Input-Test")
    ]
]


w = sg.Window(layout)

for i in range(5):
    e = w.loop()
    print("Loop:",e,w.values)

    if e is None:
        break





