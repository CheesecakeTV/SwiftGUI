import SwiftGUI as sg

sg.Themes.FourColors.Jungle()
#sg.Examples.preview_all_elements()

layout = [
    [
        sg.Combobox(
            range(15),
            key= "combo",
            default_event=True,
        )
    ]
]

w = sg.Window(layout)

for e,v in w:
    print(e,v)

