import json
import SwiftGUI as sg

sg.Themes.FourColors.Teal()

def row(name):
    return [
        sg.T(name, width= 15, anchor= "center"),
        sg.Input(key= name, default_event= True)
    ]

layout = [
    *[row(i) for i in range(10)],
    [
        sg.Button("Save", key= "save"),
        sg.Button("Load", key= "load"),
    ]
]

w = sg.Window(layout)
saved = dict()

for e,v in w:
    print(e,v)

    if e == "save":
        saved = v.to_json()
        print("saved")

    if e == "load":
        v.from_json(saved)
        print("loaded")


