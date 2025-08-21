import SwiftGUI as sg

### Global options ###

### Layout ###
left_tab = sg.TabFrame([
    [
        sg.Listbox(
            range(10)
        ),
    ]
], key= "left", fake_key= "Günther")

right_tab = sg.TabFrame([
    [sg.T("Smaller element")],
    [sg.Button("Another smaller element")],
    [sg.T("<-- sg.Listbox")]
], key= "right", fake_key= "Harald")

layout:list[list[sg.BaseElement]] = [
    [
        nb := sg.Notebook(
            left_tab,
            right_tab,
            default_event= True,
            key = "NB"
        )
    ]
]

w = sg.Window(layout)
nb.value = "Harald"

### Additional configurations/actions ###


### Main loop ###
for e,v in w:
    print(nb.value)

### After window was closed ###
