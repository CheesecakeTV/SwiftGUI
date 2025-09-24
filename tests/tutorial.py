import SwiftGUI as sg

sg.Themes.FourColors.Froggy()

main_layout = [
    [
        sg.Button(
            "Some Button",
            width= 30,
            height= 5,
        )
    ]
]

another_layout = [
    [
        sg.Button(
            "Another Button",
            width= 30,
            height= 5,
            key= "test",
        )
    ]
]

w = sg.Window(main_layout)
sw = sg.SubWindow(another_layout)

print(sw.loop_close())

for e,v in w:
    print(e,v)

