import SwiftGUI as sg

sg.Themes.FourColors.Chocolate()

layout = [
    [
        sg.Button(
            "SwiftGUI!",
            key= "Button",
            repeatdelay= 500,
            repeatinterval= 100,
        ),
    ]
]

w = sg.SubWindow(layout, padx= 50, pady= 50)

for e,v in w:
    print(e,v)
