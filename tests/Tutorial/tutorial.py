import SwiftGUI as sg

sg.Themes.FourColors.Emerald()

layout = [
    [
        table := sg.Table(
            (range(3) for _ in range(50)),
            headings=["Eins", "Zwei", "Dro"],
            column_width=(5,15,30),
            #hide_headings=True,
            #expand=True,
        )
    ]
]

w = sg.Window(layout)

for e,v in w:
    ...

