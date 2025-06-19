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
w["Input-Test"].bind_event("Button",key_function=lambda val:print(val),send_val=True)

while True:
    e = w.loop()
    print(e,w.values)

    if not w.exists:
        break





