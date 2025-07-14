import SwiftGUI as sg
from SwiftGUI import Event, Color
import tkinter as tk
from tkinter import ttk

sg.GlobalOptions.Common_Textual.fontsize = 14
sg.themes.FacebookMom()

# sg.GlobalOptions.Common_Textual.reset_to_default()
# sg.GlobalOptions.Button.reset_to_default()


layout_left = [
    [
        sg.T("Hallo",key="TestText",width=25,anchor="center")
    ],[
        sg.HorizontalSeparator()
    ],[
        sg.HorizontalSeparator()
    ],[
        sg.Checkbox("Check me, mate!!!",key="Check!",default_event=True,key_function=lambda elem:elem.update(readonly=True))
    ], [
        sg.HorizontalSeparator()
    ], [
        sg.HorizontalSeparator()
    ], [
        sg.T("Welt",anchor="w")
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
        sg.Button("Hallo Welt-Button",key="Hallo Welt",disabled = False,height=2,text_color="red",repeatdelay=1000,repeatinterval=100,borderwidth=5),
        sg.In("Was geht", key="Input-Test", background_color="red", justify="right", text_color="green",
              default_event=True),
        sg.In("Was geht", key="Another-Input-Test",background_color=Color.AntiqueWhite2,readonly=True),
    ],[
        sg.Form(["Hallo","Welt","Das","Ist","Ein","Test"],key="Form")
    ],[
        sg.Button("Another button!",key="Another Button"),
        sg.Button("Another button!", key="Another Button")
    ],[
    ],[
        sg.Input("Haha", key_function=lambda elem: elem.set_value("Haha"), default_event=True)
    ],[
        sg.Button("This is a test!", key="TestButton", width=50, padx=50),
    ],[
        sg.Button("This is a test!", key="TestButton1", width=50, padx=50),
    ]
]

layout_right = [
    [
        sg.Button("I'm a button")
    ]
]

# s = ttk.Style()
# s.configure("TSeparator",background="green")

layout = [
    [
        sg.Frame(layout_left),
        sg.Spacer(width=150),
        sg.VerticalSeparator(),
        sg.Frame(layout_right),
    ],[
        sg.Spacer(height=50)
    ],[
        sg.Button("One button to rule them all!",relief="solid")
    ]
]

w = sg.Window(layout,alignment="left")
#w["Input-Test"].bind_event(Event.MouseEnter,key_function=sg.KeyFunctions.copy_value("TestText"))
w["Input-Test"].bind_event(Event.MouseEnter,key_function=sg.KeyFunctions.set_value_to("Mouse entered"))
w["Another-Input-Test"].bind_event(Event.MouseEnter,key_function=sg.KeyFunctions.copy_value_from("Input-Test"))

print("Start:",w.values)
print(w["IAM"].value)

for e,v in w:
    print(e,v)
    #w["Check!"].flash()
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


