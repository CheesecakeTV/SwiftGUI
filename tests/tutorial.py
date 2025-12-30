import SwiftGUI as sg

sg.Themes.Thematic.Hacker()

layout = [
    [
        sg.Button(
            "New row",
            key= "NEW"
        )
    ]
]

w = sg.Window(layout)
window_frame = w.frame

for e,v in w:
    print(e,v)

    window_frame.add_row(   # Add...
        [   # ... This row
            sg.T("New Row! "),
            sg.Button(" I'm a button ")
        ]
    )

