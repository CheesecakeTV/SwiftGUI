import SwiftGUI as sg
from SwiftGUI import Event, Color
import tkinter as tk
from tkinter import ttk


sg.GlobalOptions.Common_Textual.fontsize = 10
sg.themes.Hacker()
#sg.GlobalOptions.reset_all_options()
#sg.themes.FacebookMom()


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
        sg.T("Amazing what you can accomplish\non a saturday",key="SomeText"),
        sg.Frame([
            [
                sg.T("I am",font_overstrike=True,key="IAM")
            ],[
                sg.T("Inside of another Frame!")
            ]
        ])
    ],[
        sg.Button("Hallo Welt-Button",key="Hallo Welt",disabled = False,height=2,text_color="red",repeatdelay=1000,repeatinterval=100,borderwidth=5),
        sg.In("Was geht", key="Input-Test", justify="right", text_color="green",
              default_event=True),
        sg.In("Was geht", key="Another-Input-Test",readonly=True),
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
        sg.Button("I'm a button",key_function=lambda :w.update(background_color = "red"))
    ],[
        sg.TKContainer(tk.Button, key="ContainerTest", expand=True, bg="red")
    ]
]

# s = ttk.Style()
# s.configure("TSeparator",background="green")

layout = [
    [
        the_frame := sg.Frame(layout_left),
        sg.Spacer(width=150),
        sg.VerticalSeparator(),
        sg.Frame(layout_right),
    ],[
        sg.Spacer(height=50)
    ],[
        sg.Button("One button to rule them all!",relief="solid")
    ],[
        sg.Listbox(["Hallo", "Welt"], key="List", default_event=True, height=5, expand=True)
    ]
]

w = sg.Window(layout,alignment="left")
w["ContainerTest"].update(text="blue")
#the_frame.update(background_color = "red")
#w.update(background_color="red")

w["List"].list_elements = ["Hi","Hi","Hallo", "Hi", "Welt", "World"]

w["List"].color_rows(["Hi"],background_color="gold")
w["List"].delete_element("Hi")

w["Input-Test"].bind_event(Event.MouseEnter,key_function=sg.KeyFunctions.set_value_to("Mouse entered"))
w["Another-Input-Test"].bind_event(Event.MouseEnter,key_function=sg.KeyFunctions.copy_value_from("Input-Test"))

print("Start:",w.values)

for e,v in w:
    print(e,v)
    w["List"].append_front(e)
    print(w["List"].list_elements)
    print(w["List"].find_index)
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


