import SwiftGUI_LeButch as sg
from SwiftGUI_LeButch import Event

layout = [
    [
        sg.T("Hallo",key="TestText")
    ],[
        sg.T("Welt")
    ],[
        sg.T("Amazing what you can accomplish\non a saturday",key="SomeText"),
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
        sg.Form(["Hallo","Welt","Das","Ist","Ein","Test"],key="Form")
    ]
]

w = sg.Window(layout)
w["Input-Test"].bind_event(Event.MouseEnter,send_wev=True,send_val=True,key_function=sg.KeyFunctions.copy_value("TestText"))
w["Input-Test"].bind_event(Event.MouseEnter,send_wev=True,send_val=True,key_function=sg.KeyFunctions.copy_value("TestText"))

print("Start:",w.values)

while True:
    e,v = w.loop()
    print(e,v)

    w["Input-Test"].value = e
    w["SomeText"].value = "Funktioniert"

    if not w.exists:
        break

    if e == "Hallo Welt":
        w["Form"].clear_all_values()
        w["Form"].value = {"Hallo":"Welt","Test":"Tatsache"}


