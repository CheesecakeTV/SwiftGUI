import SwiftGUI as sg

sg.Themes.FourColors.CocoaMilk()

layout = [
    [
        sg.ImageButton("Star.png",text= "right", compound="right", width=100, height=50),
        sg.ImageButton("Star.png", text="left", compound="left", width=100, height=50),
        sg.ImageButton("Star.png", text="bottom", compound="bottom", width=100, height=50),
        sg.ImageButton("Star.png", text="top", compound="top", width=100, height=50),
    ]
]

w = sg.Window(layout, padx=150, pady=50)

for e,v in w:
    print("Loop:", e, v)

