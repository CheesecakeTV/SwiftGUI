import SwiftGUI as sg

@sg.attach_function_to_key("Button1")
def do_something():
    print("Button 1 was pressed")

@sg.attach_function_to_key("Button2")
def do_something_else(v):
    print("Button 2 was pressed.")
    v["Button2"] = "Pressed"

layout = [
    [
        sg.Button(" 1 ", key="Button1"),
        sg.Button(" 2 ", key="Button2"),
        sg.Button(" 3 ", key="Button3"),
    ],[
        sg.T("Hallo",padding=150)
    ]
]

w = sg.Window(layout)

for e,v in w:
    print("Loop:",e, v)

