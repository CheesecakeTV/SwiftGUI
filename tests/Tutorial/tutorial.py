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
        my_table := sg.Table(
        [[i] for i in range(10)],
        key= "LB", default_event= True),
    ],
    [
        sg.Form(["Hello", "World", "Test"], key= "Form")
    ],
    [
        sg.Button("Save", key= "save"),
        sg.Button("Load", key= "load"),
    ]
]

def ev_loop(e,v):
    global saved
    v = w.value
    print(e,v)

    if e == "save":
        saved = v.to_json()
        print("saved", saved)

    if e == "load":
        #v.from_json(saved)
        #print("loaded")
        my_table.set_all_indexes((1, ))

w = sg.Window([[sg.SubLayout(layout, key="SL", event_loop_function=ev_loop)]])
saved = dict()

for e,v in w:
    ...

