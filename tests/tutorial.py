import SwiftGUI as sg

sg.Themes.FourColors.NeonDiamond()

layout = [
    [
        my_combo := sg.Combobox(
            ["", "Hello", "World", "Choice3", "Choice4", "Another choice"],
            can_change_text= True,
        )
    ]
]

w = sg.Window(layout, padx=30, pady=30)

my_combo.update(choices= ["New", "Choice"])

for e, v in w:
    print(e, v)

