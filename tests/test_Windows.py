import SwiftGUI as sg
from SwiftGUI import Event, Color

sg.GlobalOptions.Common_Textual.fontsize = 14

layout = [
    [
        sg.T("Hallo",key="TestText",width=25,anchor="center")
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
        sg.Button("Hallo Welt-Button",key="Hallo Welt",disabled = False,text_color="red",repeatdelay=1000,repeatinterval=100),
        sg.In("Was geht",key="Input-Test",background_color="red",justify="right",text_color="green",enable_textchange_event=True),
        sg.In("Was geht", key="Another-Input-Test",background_color=Color.AntiqueWhite2,disabled=True),
    ],[
        sg.Form(["Hallo","Welt","Das","Ist","Ein","Test"],key="Form")
    ],[
        sg.Button("Another button!",key="Another Button")
    ],[
        sg.Input("Haha",key_function=lambda elem:elem.set_value("Haha"),enable_textchange_event=True)
    ]
]

w = sg.Window(layout)
#w["Input-Test"].bind_event(Event.MouseEnter,key_function=sg.KeyFunctions.copy_value("TestText"))
w["Input-Test"].bind_event(Event.MouseEnter,key_function=sg.KeyFunctions.clear_str_value)
w["Another-Input-Test"].bind_event(Event.MouseEnter,key_function=sg.KeyFunctions.copy_value_from("Input-Test"))

print("Start:",w.values)
print(w["IAM"].value)

for e,v in w:
    print(e,v)
    #w["Hallo Welt"].flash()

    #w["Input-Test"].value = e
    #w["Input-Test"].update(background_color=sg.Color.gold)
    #w["SomeText"].value = "Funktioniert"

    w["SomeText"].update(background="red")
    w["IAM"].update(font_overstrike=False,background_color=None)

    if not w.exists:
        break

    if e == "Another Button":
        w["Hallo Welt"].push_once()

    if e == "Hallo Welt":
        w["Form"].clear_all_values()
        w["Form"].value = {"Hallo":"Welt","Test":"Tatsache"}


