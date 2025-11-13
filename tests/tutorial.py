import SwiftGUI as sg

sg.Themes.FourColors.Emerald()

layout = [
    [
        sg.MultistateButton(
            ["Choice 1", "Choice 2", "Choice 3"],
            default_selection= "Choice 1",
            key= "Key",
        )
    ]
]

w = sg.Window(layout, padx=30, pady=30)

for e, v in w:
    print(e, v)

