import SwiftGUI as sg

sg.Themes.FourColors.Froggy()

main_layout = [
    [
        sg.Button(
            "Some Button",
            width= 30,
            height= 5,
            key= "Main Button",
        )
    ]
]

another_layout = [
    [
        sg.Input(key= "Input"),
        sg.Button("Button 1", key="B1"),
        sg.Button("Button 2", key="B2"),
        sg.Button("Button 3", key="B3"),
    ]
]

def sw_loop(e,v):
    # Some example-loop
    print("Button-press:", e)
    print("Input-value:", v["Input"])
    sw["Input"].value = e

w = sg.Window(main_layout)
sw = sg.SubWindow(another_layout, event_loop_function=sw_loop)

w.loop()

