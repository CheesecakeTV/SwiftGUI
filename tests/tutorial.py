import SwiftGUI as sg

sg.Themes.FourColors.GarnetFlair()

layout = [
    [
        sg.Radiobutton("Choice 1", group=0, check_background_color="red"),
        sg.Radiobutton("Choice 2", group=0, check_background_color="blue"),
        sg.Radiobutton("Choice 3", group=0, check_background_color="green"),
        sg.Radiobutton("Choice 4", group=0, check_background_color="pink"),
    ]
]

w = sg.Window(layout, padx=30, pady=30)

for e, v in w:
    print(e, v)

