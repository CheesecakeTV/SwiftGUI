import SwiftGUI as sg

sg.Themes.FourColors.Chocolate()

layout = [
    [
        sg.Button(
            "SwiftGUI",
            disabled= True,
            text_color_disabled= "#E0C097",
        )
    ]
]

w = sg.SubWindow(layout, padx= 50, pady= 50)

for e,v in w:
    print(e,v)
