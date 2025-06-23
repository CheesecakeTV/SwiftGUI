import SwiftGUI as sg
from SwiftGUI import Event

layout = [
    [
        sg.Example(text="It does work!"),
        sg.T("Hallo",key="TestText")
    ],[
        sg.T("Welt")
    ],[
        sg.T("Amazing what you can accomplish\non a saturday",key="SomeText",text_color="green",background_color=sg.Color.SeaGreen1),
        sg.Frame([
            [
                sg.T("I am",font_overstrike=True,key="IAM",background_color="red")
            ],[
                sg.T("Inside of another Frame!")
            ]
        ])
    ],[
        sg.Button("Hallo Welt-Button",key="Hallo Welt"),
        sg.In("Was geht",key="Input-Test",background_color="red"),
        sg.In("Was geht", key="Another-Input-Test"),
    ],[
        sg.Form(["Hallo","Welt","Das","Ist","Ein","Test"],key="Form")
    ]
]

w = sg.Window(layout)
#w["Input-Test"].bind_event(Event.MouseEnter,key_function=sg.KeyFunctions.copy_value("TestText"))
w["Input-Test"].bind_event(Event.MouseEnter,key_function=sg.KeyFunctions.clear_str_value)
w["Another-Input-Test"].bind_event(Event.MouseEnter,key_function=sg.KeyFunctions.copy_value_from("Input-Test"))

print("Start:",w.values)
print(w["IAM"].value)

while True:
    e,v = w.loop()
    print(e,v)

    w["Input-Test"].value = e
    w["Input-Test"].update(background_color=sg.Color.gold)
    #w["SomeText"].value = "Funktioniert"

    w["SomeText"].update(background="red")
    w["IAM"].update(font_overstrike=False,background_color=None)

    if not w.exists:
        break

    if e == "Hallo Welt":
        w["Form"].clear_all_values()
        w["Form"].value = {"Hallo":"Welt","Test":"Tatsache"}


