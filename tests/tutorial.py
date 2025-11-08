import SwiftGUI as sg

sg.Themes.FourColors.Jungle()
#sg.Examples.preview_all_elements()

layout = [
    [
        sg.Combobox(
            range(15),
            key= "combo",
            default_event=True,
        ),
        sg.Combobox(
            range(15),
            key="combo1",
            default_event=True,
        ).update_scrollbar_y(background_color= "red"),
    ]
]

w = sg.Window(layout)

for e,v in w:
    print(e,v)

